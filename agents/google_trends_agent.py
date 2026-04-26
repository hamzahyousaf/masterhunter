# google_trends_agent.py
class GoogleTrendsAgent:
    def __init__(self):
        self.name = "Google Trends Agent"
    
    def get_uae_trends(self):
        return {
            "current_season": "summer",
            "hot_categories": ["cooling_gadgets", "kitchen_appliances"],
            "rising_searches": ["ice maker UAE", "portable fan UAE", "vegetable chopper"]
        }
