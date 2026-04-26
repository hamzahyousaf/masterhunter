# zambeel_agent.py
class ZambeelScraper:
    def __init__(self):
        self.name = "Zambeel Agent"
    
    def get_trending_products(self):
        return [
            {"name": "Portable Neck Fan", "price": 48, "category": "cooling"},
            {"name": "Vegetable Chopper", "price": 35, "category": "kitchen"},
            {"name": "Ice Maker Machine", "price": 78, "category": "cooling"}
        ]
    
    def get_formatted_for_master(self):
        products = self.get_trending_products()
        return [{"id": f"zmb_{i}", "name": p["name"], "price": p["price"], "zambeel_price": p["price"]} 
                for i, p in enumerate(products)]
