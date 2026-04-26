# aliexpress_agent.py
class AliExpressScraper:
    def __init__(self):
        self.name = "AliExpress Agent"
    
    def get_hot_products(self):
        return [
            {"name": "Electric Ice Crusher", "price": 68, "margin": 45, "aliexpress_hot": True, "category": "cooling"},
            {"name": "Cold Brew Coffee Maker", "price": 83, "margin": 50, "aliexpress_hot": True, "category": "cooling"},
            {"name": "Portable Blender", "price": 59, "margin": 40, "aliexpress_hot": True, "category": "kitchen"}
        ]
    
    def get_formatted_for_master(self):
        products = self.get_hot_products()
        return [{"id": f"ae_{i}", "name": p["name"], "price": p["price"], "margin": p["margin"], "aliexpress_hot": True} 
                for i, p in enumerate(products)]
