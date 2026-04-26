# tiktok_agent.py
class TikTokViralAgent:
    def __init__(self):
        self.name = "TikTok Agent"
    
    def get_viral_products(self):
        return [
            {"name": "Ice Maker", "tiktok_views": 5200000, "category": "cooling"},
            {"name": "Neck Fan", "tiktok_views": 3800000, "category": "cooling"},
            {"name": "Vegetable Chopper", "tiktok_views": 4500000, "category": "kitchen"}
        ]
    
    def get_formatted_for_master(self):
        products = self.get_viral_products()
        return [{"id": f"tt_{i}", "name": p["name"], "tiktok_views": p["tiktok_views"]} 
                for i, p in enumerate(products)]
