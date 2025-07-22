from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    FlexSendMessage, ImageSendMessage
)
from database.db_manager import DatabaseManager
from utils.text_parser import TextParser
from utils.category_classifier import CategoryClassifier
from utils.chart_generator import ChartGenerator
from bot.flex_messages import FlexMessageBuilder
from linebot.models import ImageSendMessage
import os

class MessageHandler:
    """處理 LINE Bot 訊息的主要類別"""

    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        self.db = DatabaseManager()
        self.parser = TextParser()
        self.classifier = CategoryClassifier()
        self.chart_gen = ChartGenerator()
        self.flex_builder = FlexMessageBuilder()

    def handle_text_message(self, event: MessageEvent):
        """處理文字訊息"""
        text = event.message.text.strip()
        user_id = event.source.user_id

        # 取得使用者名稱
        try:
            profile = self.line_bot_api.get_profile(user_id)
            user_name = profile.display_name
        except:
            user_name = "使用者"

        # 處理說明指令
        if text.lower() in ['help', '說明', '幫助', '使用說明', '/help']:
            self._send_help_message(event)
            return

        # 處理查帳指令
        if self.parser.is_query_command(text):
            self._handle_query_command(event, user_id, user_name)
            return

        # 處理統計指令
        if self.parser.is_summary_command(text):
            self._handle_summary_command(event, user_id)
            return

        # 處理刪除指令
        delete_index = self.parser.parse_delete_command(text)
        if delete_index is not None:
            self._handle_delete_command(event, user_id, delete_index)
            return

        # 處理顯示圖表指令
        if text in ['顯示圖表', '查看圖表', '圖表']:
            self._handle_show_chart(event, user_id)
            return

        # 嘗試解析為記帳指令
        expense_data = self.parser.parse_expense_command(text)
        if expense_data:
            self._handle_expense_command(event, user_id, expense_data)
            return

        # 無法識別的指令
        self._send_error_message(event, "無法識別您的指令，請輸入「說明」查看使用方法。")

    def _handle_expense_command(self, event, user_id, expense_data):
        """處理新增支出指令"""
        category_raw, amount, description = expense_data

        # 使用分類器自動分類
        category = self.classifier.classify(category_raw)

        # 新增到資料庫
        try:
            expense = self.db.add_expense(
                line_user_id=user_id,
                category=category,
                amount=amount,
                description=description
            )

            # 回傳成功訊息
            flex_message = self.flex_builder.create_success_message(
                'add',
                {'expense': expense}
            )

            self.line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text="新增成功",
                    contents=flex_message
                )
            )

        except Exception as e:
            self._send_error_message(event, f"新增失敗：{str(e)}")

    def _handle_query_command(self, event, user_id, user_name):
        """處理查詢指令"""
        try:
            expenses = self.db.get_recent_expenses(user_id, limit=5)

            if not expenses:
                self.line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="您還沒有任何支出記錄。")
                )
                return

            # 建立 Flex Message
            flex_message = self.flex_builder.create_expense_list(expenses, user_name)

            self.line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text="最近支出清單",
                    contents=flex_message
                )
            )

        except Exception as e:
            self._send_error_message(event, f"查詢失敗：{str(e)}")

    def _handle_summary_command(self, event, user_id):
        """處理統計指令"""
        try:
            summary = self.db.get_weekly_summary(user_id)

            if not summary['expenses_by_category']:
                self.line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="本週還沒有任何支出記錄。")
                )
                return

            # 建立 Flex Message
            flex_message = self.flex_builder.create_weekly_summary(summary, has_chart=True)

            self.line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text="本週支出統計",
                    contents=flex_message
                )
            )

        except Exception as e:
            self._send_error_message(event, f"統計失敗：{str(e)}")

    def _handle_delete_command(self, event, user_id, delete_index):
        """處理刪除指令"""
        try:
            success = self.db.delete_expense(user_id, delete_index)

            if success:
                flex_message = self.flex_builder.create_success_message('delete', {})
                self.line_bot_api.reply_message(
                    event.reply_token,
                    FlexSendMessage(
                        alt_text="刪除成功",
                        contents=flex_message
                    )
                )
            else:
                self._send_error_message(event, "找不到指定的支出記錄，請確認編號是否正確。")

        except Exception as e:
            self._send_error_message(event, f"刪除失敗：{str(e)}")

    def _handle_show_chart(self, event, user_id):
        """處理顯示圖表指令"""
        try:
            summary = self.db.get_weekly_summary(user_id)

            if not summary['expenses_by_category']:
                self.line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="本週還沒有任何支出記錄，無法生成圖表。")
                )
                return

            # 生成圖表 URL
            chart_url = self.chart_gen.generate_weekly_bar_chart(
                summary['expenses_by_category'],
                summary['start_date'],
                summary['end_date']
            )

            if chart_url:
                # 發送圖片訊息
                from linebot.models import ImageSendMessage
                self.line_bot_api.reply_message(
                    event.reply_token,
                    ImageSendMessage(
                        original_content_url=chart_url,
                        preview_image_url=chart_url
                    )
                )
            else:
                self.line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="❌ 生成圖表失敗，請稍後再試")
                )

        except Exception as e:
            self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"❌ 顯示圖表失敗：{str(e)}")
            )

    def _send_help_message(self, event):
        """發送說明訊息"""
        flex_message = self.flex_builder.create_help_message()
        self.line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="使用說明",
                contents=flex_message
            )
        )

    def _send_error_message(self, event, error_message):
        """發送錯誤訊息"""
        flex_message = self.flex_builder.create_success_message(
            'error',
            {'message': error_message}
        )
        self.line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="錯誤",
                contents=flex_message
            )
        )