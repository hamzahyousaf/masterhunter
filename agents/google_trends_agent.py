# google_trends_agent.py - REAL DATA VERSION
from pytrends.request import TrendReq
import pandas as pd
from datetime import datetime

class GoogleTrendsAgent:
    def __init__(self):
        self.name = "Google Trends Agent (Real)"
        self.pytrends = TrendReq(hl='en-US', timeout=10)
    
    def get_uae_trends(self):
        """Get real trending searches in UAE"""
        try:
            # Get trending searches in UAE
            trending = self.pytrends.trending_searches(pn='united_arab_emirates')
            
            # Get top 10 trending
            top_trends = trending.head(10).values.flatten().tolist()
            
            # Detect categories based on keywords
            categories = self._detect_categories(top_trends)
            
            return {
                "current_season": self._detect_season(),
                "hot_categories": categories,
                "rising_searches": top_trends[:5],
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"⚠️ Google Trends error: {e}")
            return self._get_fallback_data()
    
    def _detect_categories(self, trends):
        categories = []
        kitchen_keywords = ['recipe', 'cook', 'kitchen', 'food', 'meal', 'dinner', 'chopper', 'blender']
        cooling_keywords = ['fan', 'cool', 'ac', 'ice', 'summer', 'cold', 'freeze']
        
        for trend in trends:
            trend_lower = str(trend).lower()
            if any(k in trend_lower for k in kitchen_keywords):
                categories.append("kitchen_gadgets")
            if any(k in trend_lower for k in cooling_keywords):
                categories.append("cooling_gadgets")
        
        return list(set(categories)) or ["general"]
    
    def _detect_season(self):
        month = datetime.now().month
        if 5 <= month <= 9:
            return "summer"
        elif 10 <= month <= 11:
            return "autumn"
        else:
            return "winter"
    
    def _get_fallback_data(self):
        return {
            "current_season": "summer",
            "hot_categories": ["cooling_gadgets", "kitchen_appliances"],
            "rising_searches": ["ice maker", "portable fan", "vegetable chopper"],
            "timestamp": datetime.now().isoformat()
        }
