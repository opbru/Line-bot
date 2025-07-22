import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import pandas as pd
from datetime import datetime
import os
from typing import List, Tuple
import io
import base64

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']  # 在雲端環境使用
plt.rcParams['axes.unicode_minus'] = False

class ChartGenerator:
    """圖表生成器"""

    @staticmethod
    def generate_weekly_bar_chart(expenses_data: List[Tuple[str, float, int]],
                                  start_date: datetime,
                                  end_date: datetime) -> str:
        """
        生成週支出長條圖
        返回: 圖片的base64編碼字串
        """
        # 準備資料
        if not expenses_data:
            return None

        categories = [data[0] for data in expenses_data]
        amounts = [data[1] for data in expenses_data]

        # 建立圖表
        plt.figure(figsize=(10, 6))

        # 使用顏色調色板
        colors = sns.color_palette("husl", len(categories))

        # 繪製長條圖
        bars = plt.bar(categories, amounts, color=colors)

        # 在長條上顯示數值
        for bar, amount in zip(bars, amounts):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'${amount:,.0f}',
                    ha='center', va='bottom')

        # 設定標題和標籤
        plt.title(f'Weekly Expenses Summary\n{start_date.strftime("%Y-%m-%d")} - {end_date.strftime("%Y-%m-%d")}',
                 fontsize=16, pad=20)
        plt.xlabel('Category', fontsize=12)
        plt.ylabel('Amount (NTD)', fontsize=12)

        # 設定y軸格式
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

        # 旋轉x軸標籤
        plt.xticks(rotation=45, ha='right')

        # 調整布局
        plt.tight_layout()

        # 儲存到記憶體並轉換為base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()

        return image_base64

    @staticmethod
    def generate_pie_chart(expenses_data: List[Tuple[str, float, int]],
                          total_amount: float) -> str:
        """
        生成支出分類圓餅圖
        返回: 圖片的base64編碼字串
        """
        if not expenses_data:
            return None

        categories = [data[0] for data in expenses_data]
        amounts = [data[1] for data in expenses_data]

        # 建立圖表
        plt.figure(figsize=(10, 8))

        # 使用顏色調色板
        colors = sns.color_palette("husl", len(categories))

        # 繪製圓餅圖
        wedges, texts, autotexts = plt.pie(amounts,
                                           labels=categories,
                                           colors=colors,
                                           autopct='%1.1f%%',
                                           startangle=90)

        # 設定標題
        plt.title(f'Expense Distribution\nTotal: ${total_amount:,.0f}',
                 fontsize=16, pad=20)

        # 確保圓形
        plt.axis('equal')

        # 調整文字大小
        for text in texts:
            text.set_fontsize(12)
        for autotext in autotexts:
            autotext.set_fontsize(10)
            autotext.set_color('white')
            autotext.set_weight('bold')

        # 儲存到記憶體並轉換為base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()

        return image_base64