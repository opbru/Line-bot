import json
import urllib.parse
from typing import List, Tuple
from datetime import datetime

class ChartGenerator:
    """使用 QuickChart.io API 生成圖表"""

    @staticmethod
    def generate_weekly_bar_chart(expenses_data: List[Tuple[str, float, int]],
                                  start_date: datetime,
                                  end_date: datetime) -> str:
        """
        生成週支出長條圖
        返回: 圖表的 URL
        """
        if not expenses_data:
            return None

        # 準備資料
        categories = [data[0] for data in expenses_data]
        amounts = [float(data[1]) for data in expenses_data]

        # 建立 Chart.js 配置
        chart_config = {
            "type": "bar",
            "data": {
                "labels": categories,
                "datasets": [{
                    "label": "支出金額 (NTD)",
                    "data": amounts,
                    "backgroundColor": [
                        "rgba(255, 99, 132, 0.8)",
                        "rgba(54, 162, 235, 0.8)",
                        "rgba(255, 206, 86, 0.8)",
                        "rgba(75, 192, 192, 0.8)",
                        "rgba(153, 102, 255, 0.8)",
                        "rgba(255, 159, 64, 0.8)"
                    ],
                    "borderColor": [
                        "rgba(255, 99, 132, 1)",
                        "rgba(54, 162, 235, 1)",
                        "rgba(255, 206, 86, 1)",
                        "rgba(75, 192, 192, 1)",
                        "rgba(153, 102, 255, 1)",
                        "rgba(255, 159, 64, 1)"
                    ],
                    "borderWidth": 1
                }]
            },
            "options": {
                "responsive": True,
                "plugins": {
                    "legend": {
                        "display": False
                    },
                    "title": {
                        "display": True,
                        "text": f"週支出統計 ({start_date.strftime('%m/%d')} - {end_date.strftime('%m/%d')})",
                        "font": {
                            "size": 16
                        }
                    }
                },
                "scales": {
                    "y": {
                        "beginAtZero": True,
                        "ticks": {
                            "callback": "function(value) { return '$' + value.toLocaleString(); }"
                        }
                    }
                }
            }
        }

        # 轉換為 JSON 並編碼
        chart_json = json.dumps(chart_config)
        encoded_config = urllib.parse.quote(chart_json)

        # 生成 QuickChart URL
        chart_url = f"https://quickchart.io/chart?c={encoded_config}&width=500&height=300&backgroundColor=white"

        return chart_url

    @staticmethod
    def generate_pie_chart(expenses_data: List[Tuple[str, float, int]],
                          total_amount: float) -> str:
        """
        生成支出分類圓餅圖
        返回: 圖表的 URL
        """
        if not expenses_data:
            return None

        categories = [data[0] for data in expenses_data]
        amounts = [float(data[1]) for data in expenses_data]

        # 建立 Chart.js 配置
        chart_config = {
            "type": "pie",
            "data": {
                "labels": categories,
                "datasets": [{
                    "data": amounts,
                    "backgroundColor": [
                        "#FF6384",
                        "#36A2EB",
                        "#FFCE56",
                        "#4BC0C0",
                        "#9966FF",
                        "#FF9F40"
                    ]
                }]
            },
            "options": {
                "responsive": True,
                "plugins": {
                    "legend": {
                        "position": "bottom"
                    },
                    "title": {
                        "display": True,
                        "text": f"支出分佈 (總計: ${total_amount:,.0f})",
                        "font": {
                            "size": 16
                        }
                    },
                    "tooltip": {
                        "callbacks": {
                            "label": "function(context) { return context.label + ': $' + context.parsed.toLocaleString() + ' (' + (context.parsed / context.dataset._meta[0].total * 100).toFixed(1) + '%)'; }"
                        }
                    }
                }
            }
        }

        # 轉換為 JSON 並編碼
        chart_json = json.dumps(chart_config)
        encoded_config = urllib.parse.quote(chart_json)

        # 生成 QuickChart URL
        chart_url = f"https://quickchart.io/chart?c={encoded_config}&width=500&height=400&backgroundColor=white"

        return chart_url