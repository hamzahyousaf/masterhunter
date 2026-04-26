# google_trends_checker.py - Seasonal Demand Checker

import json
from datetime import datetime

class GoogleTrendsAgent:
    def __init__(self):
        self.name = "Google Trends Agent"
        print(f"✅ {self.name} initialized")
    
    def get_seasonal_demand(self, product_name):
        """Check if product has seasonal demand (summer)"""
        
        # Summer cooling products (May-August in UAE)
        summer_products = [
            "ice maker", "neck fan", "portable fan", "cooling", 
            "cold brew", "ice crusher", "cooling pad"
        ]
        
        for keyword in summer_products:
            if keyword in product_name.lower():
                return True, "summer"
        
        return False, "regular"
    
    def get_uae_trends(self):
        """Get current UAE trends"""
        
        # This would use Google Trends API in real implementation
        uae_trends = {
            "current_season": "summer_preparation",
            "hot_categories": ["cooling_gadgets", "kitchen_appliances"],
            "rising_searches": [
                "ice maker UAE",
                "portable fan UAE", 
                "vegetable chopper"
            ],
            "timestamp": datetime.now().isoformat()
        }
        
        return uae_trends


if __name__ == "__main__":
    agent = GoogleTrendsAgent()
    trends = agent.get_uae_trends()
    print(f"📊 UAE Trends: {trends}")
