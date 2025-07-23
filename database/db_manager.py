import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine, desc, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from .models import Base, User, Expense
from utils.timezone_helper import get_taipei_time

class DatabaseManager:
    def __init__(self, database_url=None):
        if database_url is None:
            database_url = os.getenv('DATABASE_URL', 'sqlite:///accounting.db')

        # 修正 Railway PostgreSQL URL 格式
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)

        print(f"Connecting to database: {database_url.split('@')[0]}...")  # 不顯示密碼

        try:
            # 建立引擎
            if 'postgresql' in database_url:
                # PostgreSQL 設定
                self.engine = create_engine(
                    database_url,
                    pool_size=5,
                    pool_pre_ping=True,
                    echo=False
                )
            else:
                # SQLite 設定
                self.engine = create_engine(
                    database_url,
                    connect_args={"check_same_thread": False},
                    echo=False
                )

            Base.metadata.create_all(self.engine)

            # 建立 Session
            Session = sessionmaker(bind=self.engine)
            self.session = Session()

            print("Database connected successfully!")

        except Exception as e:
            print(f"Database connection error: {e}")
            raise e

    def get_or_create_user(self, line_user_id, display_name=None):
        """取得或建立使用者"""
        user = self.session.query(User).filter_by(line_user_id=line_user_id).first()

        if not user:
            user = User(line_user_id=line_user_id, display_name=display_name)
            self.session.add(user)
            self.session.commit()

        return user

    def add_expense(self, line_user_id, category, amount, description=None):
        """新增支出記錄"""
        user = self.get_or_create_user(line_user_id)

        expense = Expense(
            user_id=user.id,
            category=category,
            amount=amount,
            description=description
        )

        self.session.add(expense)
        self.session.commit()

        return expense

    def get_recent_expenses(self, line_user_id, limit=5):
        """取得最近的支出記錄"""
        user = self.get_or_create_user(line_user_id)

        expenses = self.session.query(Expense)\
            .filter_by(user_id=user.id)\
            .order_by(desc(Expense.created_at))\
            .limit(limit)\
            .all()

        return expenses

    def delete_expense(self, line_user_id, expense_index):
        """刪除指定的支出記錄（按照時間倒序的索引）"""
        user = self.get_or_create_user(line_user_id)

        expenses = self.session.query(Expense)\
            .filter_by(user_id=user.id)\
            .order_by(desc(Expense.created_at))\
            .all()

        if 0 <= expense_index < len(expenses):
            expense_to_delete = expenses[expense_index]
            self.session.delete(expense_to_delete)
            self.session.commit()
            return True

        return False

    def get_weekly_summary(self, line_user_id):
        """取得本週支出統計"""
        user = self.get_or_create_user(line_user_id)

        # 計算本週的開始日期（週一）
        today = get_taipei_time()
        start_of_week = today - timedelta(days=today.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

        # 查詢本週的支出，按類別分組
        weekly_expenses = self.session.query(
            Expense.category,
            func.sum(Expense.amount).label('total_amount'),
            func.count(Expense.id).label('count')
        ).filter(
            and_(
                Expense.user_id == user.id,
                Expense.created_at >= start_of_week
            )
        ).group_by(Expense.category).all()

        # 計算總金額
        total_amount = sum(expense.total_amount for expense in weekly_expenses)

        return {
            'expenses_by_category': weekly_expenses,
            'total_amount': total_amount,
            'start_date': start_of_week,
            'end_date': today
        }

    def get_user_total_expenses(self, line_user_id):
        """取得使用者的總支出"""
        user = self.get_or_create_user(line_user_id)

        total = self.session.query(func.sum(Expense.amount))\
            .filter_by(user_id=user.id)\
            .scalar()

        return total or 0

    def close(self):
        """關閉資料庫連線"""
        self.session.close()