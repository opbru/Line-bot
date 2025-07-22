# utils/category_classifier.py
from typing import Dict, List

class CategoryClassifier:
    """簡易的類別分類器，使用關鍵字匹配"""

    # 預定義的類別和關鍵字對應
    CATEGORY_KEYWORDS = {
        '飲食': ['早餐', '午餐', '晚餐', '宵夜', '飲料', '咖啡', '茶', '食物', '吃', '喝',
                '麥當勞', '肯德基', '星巴克', '便當', '麵', '飯', '餐廳', '外送'],
        '交通': ['公車', '捷運', '計程車', 'uber', '高鐵', '火車', '機車', '加油', '停車費',
                '交通', '車資', 'youbike', '悠遊卡'],
        '購物': ['買', '購物', '網購', '商店', '百貨', '衣服', '鞋子', '包包', '3c', '書',
                '文具', '禮物', '生活用品'],
        '娛樂': ['電影', '唱歌', 'ktv', '遊戲', '旅遊', '展覽', '演唱會', '健身房', '運動'],
        '生活': ['水電', '電費', '水費', '瓦斯', '網路', '電話費', '房租', '管理費', '保險'],
        '醫療': ['看醫生', '醫院', '診所', '藥', '健保', '掛號費', '醫療'],
        '教育': ['課程', '補習', '學費', '書籍', '線上課程', '研討會', '講座'],
        '其他': []  # 預設類別
    }

    # 類別別名對應
    CATEGORY_ALIASES = {
        '早餐': '飲食',
        '午餐': '飲食',
        '晚餐': '飲食',
        '宵夜': '飲食',
        '飲料': '飲食',
        '咖啡': '飲食',
        '捷運': '交通',
        '公車': '交通',
        'uber': '交通',
        '計程車': '交通',
        '電影': '娛樂',
        '房租': '生活',
    }

    @classmethod
    def classify(cls, text: str) -> str:
        """
        根據文字內容分類
        如果文字本身就是已知的類別名稱，直接返回
        否則根據關鍵字匹配分類
        """
        text_lower = text.lower()

        # 檢查是否為別名
        if text in cls.CATEGORY_ALIASES:
            return cls.CATEGORY_ALIASES[text]

        # 檢查是否為已知類別
        if text in cls.CATEGORY_KEYWORDS:
            return text

        # 根據關鍵字匹配
        for category, keywords in cls.CATEGORY_KEYWORDS.items():
            if any(keyword in text_lower for keyword in keywords):
                return category

        # 如果沒有匹配到，返回原始文字作為類別
        return text

    @classmethod
    def get_category_emoji(cls, category: str) -> str:
        """取得類別對應的表情符號"""
        emoji_map = {
            '飲食': '🍽️',
            '交通': '🚗',
            '購物': '🛍️',
            '娛樂': '🎮',
            '生活': '🏠',
            '醫療': '🏥',
            '教育': '📚',
            '其他': '📌'
        }
        return emoji_map.get(category, '💰')