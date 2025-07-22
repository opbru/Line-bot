from datetime import datetime
from typing import List, Dict, Any

class FlexMessageBuilder:
    """Flex Message 建構器"""

    @staticmethod
    def create_expense_list(expenses: List[Any], user_name: str = "使用者") -> Dict:
        """建立支出清單的 Flex Message"""

        # 建立內容項目
        contents = []

        # 標題
        contents.append({
            "type": "text",
            "text": f"💰 {user_name}的最近支出",
            "weight": "bold",
            "size": "xl",
            "margin": "md"
        })

        contents.append({
            "type": "separator",
            "margin": "xl"
        })

        # 支出項目
        for i, expense in enumerate(expenses):
            # 時間和類別
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "margin": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": f"#{i+1}",
                        "size": "sm",
                        "color": "#555555",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": expense.created_at.strftime("%m/%d %H:%M"),
                        "size": "sm",
                        "color": "#999999",
                        "flex": 3
                    },
                    {
                        "type": "text",
                        "text": expense.category,
                        "size": "sm",
                        "color": "#111111",
                        "flex": 2,
                        "align": "end"
                    }
                ]
            })

            # 金額和描述
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "margin": "sm",
                "contents": [
                    {
                        "type": "text",
                        "text": expense.description or "-",
                        "size": "xs",
                        "color": "#999999",
                        "flex": 4
                    },
                    {
                        "type": "text",
                        "text": f"${expense.amount:,.0f}",
                        "size": "sm",
                        "color": "#FF5555",
                        "flex": 2,
                        "align": "end",
                        "weight": "bold"
                    }
                ]
            })

            # 分隔線（最後一項不加）
            if i < len(expenses) - 1:
                contents.append({
                    "type": "separator",
                    "margin": "md"
                })

        # 建立 Flex Message
        flex_message = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents
            }
        }

        return flex_message

    @staticmethod
    def create_weekly_summary(summary_data: Dict, has_chart: bool = False) -> Dict:
        """建立週總結的 Flex Message"""

        contents = []

        # 標題
        contents.append({
            "type": "text",
            "text": "📊 本週支出總結",
            "weight": "bold",
            "size": "xl",
            "margin": "md"
        })

        # 日期範圍
        start_date = summary_data['start_date'].strftime("%Y/%m/%d")
        end_date = summary_data['end_date'].strftime("%Y/%m/%d")
        contents.append({
            "type": "text",
            "text": f"{start_date} - {end_date}",
            "size": "sm",
            "color": "#999999",
            "margin": "sm"
        })

        contents.append({
            "type": "separator",
            "margin": "xl"
        })

        # 各類別支出
        for expense in summary_data['expenses_by_category']:
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "margin": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": expense.category,
                        "size": "sm",
                        "flex": 3
                    },
                    {
                        "type": "text",
                        "text": f"{expense.count} 筆",
                        "size": "xs",
                        "color": "#999999",
                        "flex": 2,
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": f"${expense.total_amount:,.0f}",
                        "size": "sm",
                        "color": "#FF5555",
                        "flex": 3,
                        "align": "end",
                        "weight": "bold"
                    }
                ]
            })

        # 總計
        contents.append({
            "type": "separator",
            "margin": "xl"
        })

        contents.append({
            "type": "box",
            "layout": "horizontal",
            "margin": "lg",
            "contents": [
                {
                    "type": "text",
                    "text": "總計",
                    "size": "md",
                    "weight": "bold",
                    "flex": 3
                },
                {
                    "type": "text",
                    "text": f"${summary_data['total_amount']:,.0f}",
                    "size": "lg",
                    "color": "#FF3333",
                    "flex": 3,
                    "align": "end",
                    "weight": "bold"
                }
            ]
        })

        # 如果有圖表，加入查看按鈕
        if has_chart:
            contents.append({
                "type": "button",
                "style": "primary",
                "height": "sm",
                "margin": "xl",
                "action": {
                    "type": "message",
                    "label": "查看圖表",
                    "text": "顯示圖表"
                }
            })

        # 建立 Flex Message
        flex_message = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents
            }
        }

        return flex_message

    @staticmethod
    def create_success_message(action: str, details: Dict) -> Dict:
        """建立成功訊息的 Flex Message"""

        emoji_map = {
            'add': '✅',
            'delete': '🗑️',
            'error': '❌'
        }

        title_map = {
            'add': '新增成功',
            'delete': '刪除成功',
            'error': '操作失敗'
        }

        contents = [
            {
                "type": "text",
                "text": f"{emoji_map.get(action, '📌')} {title_map.get(action, '操作完成')}",
                "weight": "bold",
                "size": "lg",
                "margin": "md"
            }
        ]

        # 根據不同操作加入詳細資訊
        if action == 'add' and 'expense' in details:
            expense = details['expense']
            contents.extend([
                {
                    "type": "separator",
                    "margin": "md"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "md",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "類別：",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 2
                                },
                                {
                                    "type": "text",
                                    "text": expense.category,
                                    "size": "sm",
                                    "flex": 3
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "margin": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "金額：",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 2
                                },
                                {
                                    "type": "text",
                                    "text": f"${expense.amount:,.0f}",
                                    "size": "sm",
                                    "color": "#FF5555",
                                    "weight": "bold",
                                    "flex": 3
                                }
                            ]
                        }
                    ]
                }
            ])

            if expense.description:
                contents[-1]["contents"].append({
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "sm",
                    "contents": [
                        {
                            "type": "text",
                            "text": "備註：",
                            "size": "sm",
                            "color": "#555555",
                            "flex": 2
                        },
                        {
                            "type": "text",
                            "text": expense.description,
                            "size": "sm",
                            "flex": 3,
                            "wrap": True
                        }
                    ]
                })

        elif action == 'delete':
            contents.append({
                "type": "text",
                "text": "已成功刪除指定的支出記錄",
                "size": "sm",
                "color": "#666666",
                "margin": "md",
                "wrap": True
            })

        elif action == 'error' and 'message' in details:
            contents.append({
                "type": "text",
                "text": details['message'],
                "size": "sm",
                "color": "#FF3333",
                "margin": "md",
                "wrap": True
            })

        # 建立 Flex Message
        flex_message = {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents
            }
        }

        return flex_message

    @staticmethod
    def create_help_message() -> Dict:
        """建立說明訊息的 Flex Message"""

        contents = [
            {
                "type": "text",
                "text": "📖 記帳小幫手使用說明",
                "weight": "bold",
                "size": "xl",
                "margin": "md"
            },
            {
                "type": "separator",
                "margin": "xl"
            },
            {
                "type": "text",
                "text": "📝 新增支出",
                "weight": "bold",
                "size": "md",
                "margin": "lg",
                "color": "#1E90FF"
            },
            {
                "type": "text",
                "text": "輸入格式：類別 金額 [備註]",
                "size": "sm",
                "margin": "sm",
                "wrap": True
            },
            {
                "type": "text",
                "text": "範例：早餐 65\n範例：交通 30 搭公車",
                "size": "xs",
                "color": "#666666",
                "margin": "sm",
                "wrap": True
            },
            {
                "type": "text",
                "text": "🔍 查詢記錄",
                "weight": "bold",
                "size": "md",
                "margin": "lg",
                "color": "#1E90FF"
            },
            {
                "type": "text",
                "text": "輸入：查帳",
                "size": "sm",
                "margin": "sm"
            },
            {
                "type": "text",
                "text": "🗑️ 刪除記錄",
                "weight": "bold",
                "size": "md",
                "margin": "lg",
                "color": "#1E90FF"
            },
            {
                "type": "text",
                "text": "輸入格式：刪除第N筆",
                "size": "sm",
                "margin": "sm"
            },
            {
                "type": "text",
                "text": "範例：刪除第1筆",
                "size": "xs",
                "color": "#666666",
                "margin": "sm"
            },
            {
                "type": "text",
                "text": "📊 週統計",
                "weight": "bold",
                "size": "md",
                "margin": "lg",
                "color": "#1E90FF"
            },
            {
                "type": "text",
                "text": "輸入：本週總結",
                "size": "sm",
                "margin": "sm"
            },
            {
                "type": "separator",
                "margin": "xl"
            },
            {
                "type": "text",
                "text": "💡 支援的類別：飲食、交通、購物、娛樂、生活、醫療、教育等",
                "size": "xs",
                "color": "#999999",
                "margin": "md",
                "wrap": True
            }
        ]

        # 建立 Flex Message
        flex_message = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents
            }
        }

        return flex_message