# main_orchestrator.py
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# SAHI PATHS (folders ke saath)
from agents.master_hunter import MasterProductHunter
from agents.zambeel_agent import ZambeelScraper
from agents.aliexpress_agent import AliExpressScraper
from agents.tiktok_agent import TikTokViralAgent
from agents.google_trends_agent import GoogleTrendsAgent

class Orchestrator:
    def __init__(self):
        print("="*60)
        print("  🚀 DROPSHIPPING AI AGENTS - ORCHESTRATOR")
        print("="*60)
        
        self.master = MasterProductHunter()
        self.zambeel = ZambeelScraper()
        self.aliexpress = AliExpressScraper()
        self.tiktok = TikTokViralAgent()
        self.google = GoogleTrendsAgent()
        
        print("\n✅ All agents initialized!\n")
    
    def run_full_scan(self):
        print("🔍 STEP 1: Collecting data...\n")
        
        zambeel_products = self.zambeel.get_trending_products()
        zambeel_formatted = self.zambeel.get_formatted_for_master()
        self.master.add_products_batch(zambeel_formatted)
        print(f"   ✅ Added {len(zambeel_products)} products from Zambeel")
        
        ae_products = self.aliexpress.get_hot_products()
        ae_formatted = self.aliexpress.get_formatted_for_master()
        self.master.add_products_batch(ae_formatted)
        print(f"   ✅ Added {len(ae_products)} products from AliExpress")
        
        tt_products = self.tiktok.get_viral_products()
        tt_formatted = self.tiktok.get_formatted_for_master()
        for tt in tt_formatted:
            for existing in self.master.products:
                if tt['name'].lower() in existing['name'].lower():
                    existing['tiktok_views'] = tt.get('tiktok_views', 0)
        print(f"   ✅ Added viral data for {len(tt_products)} products")
        
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
        
        # Save to file for Telegram
        import json
        with open("latest_products.json", "w") as f:
            json.dump(top, f, indent=2)
        
        return top

if __name__ == "__main__":
    orch = Orchestrator()
    orch.run_full_scan()
    print("\n✅ Scan complete!")
