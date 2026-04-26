# main_orchestrator.py
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Direct imports without config files
from master_product_hunter.master_hunter import MasterProductHunter

# Simple Zambeel scraper without config
class SimpleZambeelScraper:
    def __init__(self):
        self.name = "Zambeel Agent"
    def get_trending_products(self):
        return [
            {"name": "Portable Neck Fan", "price": 48, "category": "cooling"},
            {"name": "Vegetable Chopper", "price": 35, "category": "kitchen"},
            {"name": "Ice Maker Machine", "price": 78, "category": "cooling"}
        ]
    def get_formatted_for_master(self):
        return [{"id": f"zmb_{i}", "name": p["name"], "price": p["price"], "zambeel_price": p["price"]} 
                for i, p in enumerate(self.get_trending_products())]

# Simple AliExpress agent
class SimpleAliExpressScraper:
    def __init__(self):
        self.name = "AliExpress Agent"
    def get_hot_products(self):
        return [
            {"name": "Electric Ice Crusher", "price": 68, "margin": 45, "aliexpress_hot": True, "category": "cooling"},
            {"name": "Cold Brew Coffee Maker", "price": 83, "margin": 50, "aliexpress_hot": True, "category": "cooling"}
        ]
    def get_formatted_for_master(self):
        return [{"id": f"ae_{i}", "name": p["name"], "price": p["price"], "margin": p["margin"], "aliexpress_hot": True} 
                for i, p in enumerate(self.get_hot_products())]

# Simple TikTok agent
class SimpleTikTokAgent:
    def __init__(self):
        self.name = "TikTok Agent"
    def get_viral_products(self):
        return [
            {"name": "Ice Maker", "tiktok_views": 5200000, "category": "cooling"},
            {"name": "Neck Fan", "tiktok_views": 3800000, "category": "cooling"}
        ]
    def get_formatted_for_master(self):
        return [{"id": f"tt_{i}", "name": p["name"], "tiktok_views": p["tiktok_views"]} 
                for i, p in enumerate(self.get_viral_products())]

# Simple Google Trends agent
class SimpleGoogleTrendsAgent:
    def __init__(self):
        self.name = "Google Trends Agent"
    def get_uae_trends(self):
        return {"hot_categories": ["cooling_gadgets", "kitchen_appliances"]}

class Orchestrator:
    def __init__(self):
        print("="*60)
        print("  🚀 DROPSHIPPING AI AGENTS - ORCHESTRATOR")
        print("="*60)
        
        self.master = MasterProductHunter()
        self.zambeel = SimpleZambeelScraper()
        self.aliexpress = SimpleAliExpressScraper()
        self.tiktok = SimpleTikTokAgent()
        self.google = SimpleGoogleTrendsAgent()
        
        print("✅ All agents initialized!\n")
    
    def run_full_scan(self):
        print("🔍 STEP 1: Collecting data...\n")
        
        # Zambeel
        zambeel_products = self.zambeel.get_trending_products()
        zambeel_formatted = self.zambeel.get_formatted_for_master()
        self.master.add_products_batch(zambeel_formatted)
        print(f"   ✅ Added {len(zambeel_products)} products from Zambeel")
        
        # AliExpress
        ae_products = self.aliexpress.get_hot_products()
        ae_formatted = self.aliexpress.get_formatted_for_master()
        self.master.add_products_batch(ae_formatted)
        print(f"   ✅ Added {len(ae_products)} products from AliExpress")
        
        # TikTok
        tt_products = self.tiktok.get_viral_products()
        tt_formatted = self.tiktok.get_formatted_for_master()
        for tt in tt_formatted:
            for existing in self.master.products:
                if tt['name'].lower() in existing['name'].lower():
                    existing['tiktok_views'] = tt.get('tiktok_views', 0)
        print(f"   ✅ Added viral data for {len(tt_products)} products")
        
        # Google Trends
        trends = self.google.get_uae_trends()
        print(f"   ✅ UAE Trends: {trends['hot_categories']}")
        
        print("\n📊 STEP 2: Scoring products...\n")
        top = self.master.get_top_products(5)
        
        print("\n" + "="*60)
        print("  🏆 TOP PRODUCTS FOR DROPSHIPPING")
        print("="*60)
        
        for i, p in enumerate(top, 1):
            print(f"\n{i}. {p.get('name', 'Unknown')}")
            print(f"   Price: AED {p.get('price', 0)}")
            print(f"   Score: {p.get('score', 0)}/100")
            print(f"   Factors: {', '.join(p.get('factors_used', []))}")
        
        return top

if __name__ == "__main__":
    orch = Orchestrator()
    top = orch.run_full_scan()
    print("\n✅ Scan complete!")