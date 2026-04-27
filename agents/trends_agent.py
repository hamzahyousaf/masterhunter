# trends_agent.py - Amazon Trends via trendsmcp
from amazon_trends_api import TrendsMcpClient
import os

class TrendsAgent:
    def __init__(self):
        self.name = "Amazon Trends Agent"
        # YAHAN APNI API KEY DALO
        self.client = TrendsMcpClient(api_key="tmcp_live_mjpie2keav57683j120689suqr76furm")
    
    def get_trending_products(self, limit=10):
        """Get trending products from Amazon"""
        try:
            trending = self.client.get_top_trends(type="Amazon", limit=limit)
            
            products = []
            for item in trending:
                keyword = item.get('keyword', '')
                products.append({
                    'name': keyword,
                    'source': 'amazon_trends',
                    'trend_score': item.get('score', 50),
                    'price': self._estimate_price(keyword),
                    'margin': 40,
                    'growth': self._get_growth(keyword)
                })
            return products
        except Exception as e:
            print(f"⚠️ Trends API error: {e}")
            return self._get_mock_products()
    
    def _estimate_price(self, keyword):
        """Estimate price based on product type"""
        if 'air fryer' in keyword.lower():
            return 120
        elif 'ice maker' in keyword.lower():
            return 78
        elif 'chopper' in keyword.lower():
            return 35
        else:
            return 50
    
    def _get_growth(self, keyword):
        try:
            growth = self.client.get_growth(keyword=keyword, percent_growth=["1M"])
            return growth.get('1M', 0)
        except:
            return 0
    
    def _get_mock_products(self):
        return [
            {"name": "Air Fryer", "trend_score": 85, "price": 120, "margin": 45},
            {"name": "Ice Maker Machine", "trend_score": 78, "price": 78, "margin": 48},
            {"name": "Vegetable Chopper", "trend_score": 72, "price": 35, "margin": 42},
            {"name": "Portable Blender", "trend_score": 68, "price": 59, "margin": 40},
            {"name": "Cold Brew Maker", "trend_score": 65, "price": 83, "margin": 50}
        ]
    
    def get_formatted_for_master(self):
        products = self.get_trending_products()
        return [{
            'id': f"tr_{i}",
            'name': p['name'],
            'price': p.get('price', 50),
            'margin': p.get('margin', 40),
            'trend_score': p.get('trend_score', 50),
            'amazon_trend': True
        } for i, p in enumerate(products)]
