# master_hunter.py
import json
import os
import time

class MasterProductHunter:
    def __init__(self):
        self.name = "Master Product Hunter"
        self.products = []
        print(f"✅ {self.name} initialized")
    
    def add_products_batch(self, products):
        self.products.extend(products)
    
    def score_product(self, p):
        score = 0
        factors = []
        
        # Price range check (20-80 AED)
        price = p.get('price', 0)
        if 20 <= price <= 80:
            score += 15
            factors.append("price_range")
        
        # Zambeel available
        if p.get('zambeel_price'):
            score += 20
            factors.append("zambeel_available")
        
        # Margin check
        if p.get('margin', 0) >= 40:
            score += 15
            factors.append("margin")
        
        # TikTok viral
        views = p.get('tiktok_views', 0)
        if views > 1000000:
            score += 12
            factors.append("tiktok_viral")
        elif views > 500000:
            score += 8
            factors.append("tiktok_viral")
        
        # AliExpress hot
        if p.get('aliexpress_hot'):
            score += 10
            factors.append("aliexpress_hot")
        
        p['score'] = min(score, 100)
        p['factors_used'] = factors
        return p
    
    def score_all_products(self):
        for i, p in enumerate(self.products):
            self.products[i] = self.score_product(p)
        self.products.sort(key=lambda x: x.get('score', 0), reverse=True)
        return self.products
    
    def get_top_products(self, limit=5):
        self.score_all_products()
        return self.products[:limit]
