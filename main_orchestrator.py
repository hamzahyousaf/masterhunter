# main_orchestrator.py
import sys
import os
import json
import requests

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.master_hunter import MasterProductHunter
from agents.zambeel_agent import ZambeelScraper
from agents.aliexpress_agent import AliExpressScraper
from agents.tiktok_agent import TikTokViralAgent
from agents.google_trends_agent import GoogleTrendsAgent
from agents.trends_agent import TrendsAgent

# ============================================================
# TELEGRAM SENDER FUNCTION
# ============================================================
def send_telegram(message):
    """Send message to Telegram"""
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("CHAT_ID")
    
    if not token or not chat_id:
        print("⚠️ TELEGRAM_TOKEN or CHAT_ID not set in secrets")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        response = requests.post(url, json=payload, timeout=15)
        if response.status_code == 200:
            print("✅ Telegram message sent!")
            return True
        else:
            print(f"❌ Telegram error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Telegram exception: {e}")
        return False

# ============================================================
# ORCHESTRATOR
# ============================================================
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
        self.trends = TrendsAgent()
        
        print("\n✅ All agents initialized!\n")
    
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
        trends_data = self.google.get_uae_trends()
        print(f"   ✅ UAE Trends: {trends_data['hot_categories']}")
        
        # Amazon Trends (new!)
        trends_products = self.trends.get_trending_products()
        trends_formatted = self.trends.get_formatted_for_master()
        self.master.add_products_batch(trends_formatted)
        print(f"   ✅ Added {len(trends_products)} products from Amazon Trends")
        
        # Score and rank
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
        
        # Save to file
        with open("latest_products.json", "w") as f:
            json.dump(top, f, indent=2)
        
        return top

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    orch = Orchestrator()
    top_products = orch.run_full_scan()
    
    print("\n" + "="*60)
    print("  ✅ Scan complete!")
    print("="*60)
    
    # Send test message first
    print("\n📤 Sending products to Telegram...")
    
    # Send top products
    if top_products:
        msg = "🏆 <b>TOP PRODUCTS TODAY</b>\n\n"
        for i, p in enumerate(top_products[:3], 1):
            msg += f"{i}. <b>{p.get('name', 'Unknown')}</b>\n"
            msg += f"   💰 Price: AED {p.get('price', 0)}\n"
            msg += f"   📊 Score: {p.get('score', 0)}/100\n"
            msg += f"   ✅ Factors: {', '.join(p.get('factors_used', []))}\n\n"
        
        send_telegram(msg)
    else:
        send_telegram("⚠️ No products found in today's scan.")
    
    print("\n✅ Done!")
