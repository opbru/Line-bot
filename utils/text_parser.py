import re
from typing import Tuple, Optional

class TextParser:
    """文字解析器，用於解析使用者輸入的記帳指令"""

    @staticmethod
    def parse_expense_command(text: str) -> Optional[Tuple[str, float, Optional[str]]]:
        """
        解析記帳指令
        輸入格式: "類別 金額 [描述]"
        返回: (類別, 金額, 描述) 或 None
        """
        # 移除前後空白
        text = text.strip()

        # 嘗試不同的解析模式
        patterns = [
            # 模式1: 類別 金額 描述
            r'^(.+?)\s+(\d+(?:\.\d+)?)\s+(.+)$',
            # 模式2: 類別 金額（無描述）
            r'^(.+?)\s+(\d+(?:\.\d+)?)$',
        ]

        for pattern in patterns:
            match = re.match(pattern, text)
            if match:
                groups = match.groups()
                category = groups[0].strip()
                amount = float(groups[1])
                description = groups[2].strip() if len(groups) > 2 else None

                return (category, amount, description)

        return None

    @staticmethod
    def parse_delete_command(text: str) -> Optional[int]:
        """
        解析刪除指令
        輸入格式: "刪除第N筆" 或 "刪除 N"
        返回: 索引（從0開始）或 None
        """
        patterns = [
            r'刪除第\s*(\d+)\s*筆',
            r'刪除\s*(\d+)',
            r'delete\s*(\d+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                # 使用者輸入是從1開始，轉換為從0開始的索引
                index = int(match.group(1)) - 1
                return index if index >= 0 else None

        return None

    @staticmethod
    def is_query_command(text: str) -> bool:
        """判斷是否為查帳指令"""
        query_keywords = ['查帳', '查詢', '最近', 'recent', 'list', '清單']
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in query_keywords)

    @staticmethod
    def is_summary_command(text: str) -> bool:
        """判斷是否為統計指令"""
        summary_keywords = ['本週總結', '週總結', '統計', 'summary', '本周總結', '周總結']
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in summary_keywords)

