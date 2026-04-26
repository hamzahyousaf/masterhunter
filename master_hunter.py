# master_product_hunter/master_hunter.py
import json
import os
import time

SCORING_WEIGHTS = {
    "zambeel_available": 20, "price_range": 15, "margin": 15,
    "tiktok_viral": 12, "aliexpress_hot": 10, "season_demand": 10,
    "problem_solving": 10, "competition": 8
}
MIN_PRICE = 20
MAX_PRICE = 80
MIN_MARGIN = 40
TIKTOK_WEIGHT = 6
TOP_LIMIT = 5

class MasterProductHunter:
    def __init__(self):
        self.name = "Master Product Hunter"
        self.weights = SCORING_WEIGHTS.copy()
        self.learning_memory = self.load_memory()
        self.products = []
        print(f"✅ {self.name} initialized")
    
    def load_memory(self):
        if os.path.exists("learning_memory.json"):
            with open("learning_memory.json", "r") as f:
                return json.load(f)
        return {"feedbacks": [], "total": 0}
    
    def save_memory(self):
        with open("learning_memory.json", "w") as f:
            json.dump(self.learning_memory, f, indent=2)
    
    def add_products_batch(self, products):
        self.products.extend(products)
    
    def score_product(self, p):
        score = 0
        factors = []
        
        if p.get('zambeel_price') and MIN_PRICE <= p['zambeel_price'] <= MAX_PRICE:
            score += self.weights["zambeel_available"]
            factors.append("zambeel_available")
        
        if MIN_PRICE <= p.get('price', 0) <= MAX_PRICE:
            score += self.weights["price_range"]
            factors.append("price_range")
        
        if p.get('margin', 0) >= MIN_MARGIN:
            score += self.weights["margin"]
            factors.append("margin")
        
        views = p.get('tiktok_views', 0)
        if views > 1000000:
            score += TIKTOK_WEIGHT
            factors.append("tiktok_viral")
        elif views > 500000:
            score += TIKTOK_WEIGHT * 0.7
            factors.append("tiktok_viral")
        
        if p.get('aliexpress_hot'):
            score += self.weights["aliexpress_hot"]
            factors.append("aliexpress_hot")
        
        p['score'] = min(score, 100)
        p['factors_used'] = factors
        return p
    
    def score_all(self):
        for i, p in enumerate(self.products):
            self.products[i] = self.score_product(p)
        self.products.sort(key=lambda x: x.get('score', 0), reverse=True)
        return self.products
    
    def get_top_products(self, limit=TOP_LIMIT):
        self.score_all()
        return self.products[:limit]


if __name__ == "__main__":
    m = MasterProductHunter()
    print("✅ Master agent ready")