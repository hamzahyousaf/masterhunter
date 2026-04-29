# google_trends_agent.py - FIXED VERSION (404 + 429 solved)
from pytrends.request import TrendReq
from datetime import datetime
import time
import random


class GoogleTrendsAgent:
    def __init__(self):
        self.name = "Google Trends Agent (Real)"
        self.pytrends = TrendReq(
            hl='en-US',
            tz=240,           # UAE timezone GMT+4
            timeout=(10, 25),
            retries=3,
            backoff_factor=2  # 429 pe automatically wait karega: 2s, 4s, 8s
        )

        self.CATEGORY_KEYWORDS = {
            "kitchen_gadgets":   ['chopper', 'blender', 'air fryer', 'kitchen', 'cook', 'grater', 'slicer'],
            "cooling_gadgets":   ['fan', 'cooling', 'ice maker', 'mist fan', 'neck fan', 'portable ac'],
            "beauty_health":     ['hair', 'skin', 'face', 'cream', 'serum', 'massager', 'beauty', 'gua sha'],
            "fitness":           ['gym', 'workout', 'resistance band', 'yoga', 'protein', 'exercise'],
            "home_organization": ['organizer', 'storage', 'shelf', 'rack', 'drawer', 'hanger'],
            "phone_accessories": ['phone case', 'charger', 'cable', 'wireless', 'holder', 'stand'],
            "baby_kids":         ['baby', 'kids', 'toddler', 'toy', 'stroller', 'feeding'],
            "car_accessories":   ['car', 'dashboard', 'seat cover', 'auto', 'vehicle'],
            "pet_products":      ['dog', 'cat', 'pet', 'leash', 'collar', 'feeder'],
            "cleaning":          ['mop', 'vacuum', 'scrubber', 'spray', 'wash', 'dust'],
        }

        # Sirf 2 groups — 429 se bachne ke liye
        self.PRODUCT_SEED_KEYWORDS = [
            ["portable fan", "air fryer", "hair removal"],
            ["phone stand", "home organizer", "car accessories"],
        ]

    # ─────────────────────────────────────────────
    def get_uae_trends(self):
        try:
            trending_searches = self._get_trending_searches()
            time.sleep(random.uniform(3, 5))

            product_interest = self._get_product_interest()

            categories = self._detect_categories(trending_searches)

            return {
                "current_season":   self._detect_season(),
                "hot_categories":   categories,
                "rising_searches":  trending_searches[:8],
                "product_interest": product_interest,
                "timestamp":        datetime.now().isoformat(),
                "data_source":      "real" if trending_searches else "smart_fallback"
            }

        except Exception as e:
            print(f"⚠️  Google Trends main error: {e}")
            return self._get_fallback_data()

    # ─────────────────────────────────────────────
    # FIX 1 — 3 methods try karo, jo kaam kare use karo
    # ─────────────────────────────────────────────
    def _get_trending_searches(self):

        # Try 1: Standard name
        try:
            df = self.pytrends.trending_searches(pn='united_arab_emirates')
            if df is not None and not df.empty:
                print("   ✅ trending_searches: united_arab_emirates worked")
                return df.head(15).values.flatten().tolist()
        except Exception as e:
            print(f"   trending_searches (name) failed: {e}")

        time.sleep(2)

        # Try 2: realtime endpoint
        try:
            df = self.pytrends.realtime_trending_searches(pn='AE')
            if df is not None and not df.empty:
                titles = df['title'].head(15).tolist() if 'title' in df.columns else []
                if titles:
                    print("   ✅ realtime_trending_searches: AE worked")
                    return titles
        except Exception as e:
            print(f"   realtime_trending_searches failed: {e}")

        time.sleep(2)

        # Try 3: top_charts
        try:
            df = self.pytrends.top_charts(datetime.now().year - 1, hl='en-US', tz=240, geo='AE')
            if df is not None and not df.empty:
                print("   ✅ top_charts: AE worked")
                return df['title'].head(15).tolist()
        except Exception as e:
            print(f"   top_charts failed: {e}")

        print("   ⚠️  All trending methods failed")
        return []

    # ─────────────────────────────────────────────
    # FIX 2 — Slow requests + smaller batches
    # ─────────────────────────────────────────────
    def _get_product_interest(self):
        results = {}
        for keyword_group in self.PRODUCT_SEED_KEYWORDS:
            try:
                self.pytrends.build_payload(
                    kw_list=keyword_group,
                    cat=0,
                    timeframe='today 1-m',  # 30 days = more stable than 7-d
                    geo='AE',
                    gprop=''
                )
                df = self.pytrends.interest_over_time()
                if not df.empty:
                    for kw in keyword_group:
                        if kw in df.columns:
                            score = int(df[kw].mean())
                            if score > 5:
                                results[kw] = score
                                print(f"   ✅ {kw}: {score}/100")

                # Random wait 4-8 seconds
                wait = random.uniform(4, 8)
                print(f"   Waiting {wait:.1f}s...")
                time.sleep(wait)

            except Exception as e:
                print(f"   ❌ interest_over_time {keyword_group}: {e}")
                time.sleep(10)  # 429 pe extra wait
                continue

        return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))

    # ─────────────────────────────────────────────
    def _detect_categories(self, trends):
        found = {}
        for trend in trends:
            trend_lower = str(trend).lower()
            for category, keywords in self.CATEGORY_KEYWORDS.items():
                if any(k in trend_lower for k in keywords):
                    found[category] = found.get(category, 0) + 1

        sorted_cats = sorted(found.items(), key=lambda x: x[1], reverse=True)
        return [cat for cat, _ in sorted_cats[:5]] or self._season_default_categories()

    def _season_default_categories(self):
        season = self._detect_season()
        defaults = {
            "summer": ["cooling_gadgets", "kitchen_gadgets", "beauty_health"],
            "winter": ["home_organization", "fitness", "kitchen_gadgets"],
            "autumn": ["kitchen_gadgets", "beauty_health", "home_organization"],
            "spring": ["beauty_health", "fitness", "cleaning"],
        }
        return defaults.get(season, ["kitchen_gadgets", "beauty_health"])

    def _detect_season(self):
        month = datetime.now().month
        if 5 <= month <= 9:   return "summer"
        elif 10 <= month <= 11: return "autumn"
        elif month == 12 or month <= 2: return "winter"
        else: return "spring"

    def _get_fallback_data(self):
        """Smart fallback — season-based, not fixed mock data"""
        season = self._detect_season()
        season_data = {
            "summer": {
                "categories": ["cooling_gadgets", "kitchen_gadgets", "beauty_health"],
                "searches":   ["portable fan", "ice maker", "neck cooler", "mist fan", "air fryer"],
                "interest":   {"portable fan": 85, "ice maker": 72, "air fryer": 60}
            },
            "winter": {
                "categories": ["home_organization", "fitness", "kitchen_gadgets"],
                "searches":   ["air fryer", "home organizer", "resistance band", "food processor"],
                "interest":   {"air fryer": 78, "home organizer": 65, "resistance band": 55}
            },
            "autumn": {
                "categories": ["kitchen_gadgets", "beauty_health", "home_organization"],
                "searches":   ["air fryer", "hair removal", "storage organizer"],
                "interest":   {"air fryer": 75, "hair removal": 62}
            },
            "spring": {
                "categories": ["beauty_health", "fitness", "cleaning"],
                "searches":   ["facial massager", "yoga mat", "resistance band"],
                "interest":   {"facial massager": 70, "yoga mat": 65}
            }
        }
        data = season_data.get(season, season_data["summer"])
        return {
            "current_season":   season,
            "hot_categories":   data["categories"],
            "rising_searches":  data["searches"],
            "product_interest": data["interest"],
            "timestamp":        datetime.now().isoformat(),
            "data_source":      "smart_fallback"
        }


if __name__ == "__main__":
    agent = GoogleTrendsAgent()
    print("Testing Google Trends Agent (UAE)...\n")
    result = agent.get_uae_trends()

    print(f"\n{'='*50}")
    print(f"Season:          {result['current_season']}")
    print(f"Data source:     {result['data_source']}")
    print(f"Hot categories:  {result['hot_categories']}")
    print(f"Rising searches: {result['rising_searches'][:5]}")
    print(f"\nProduct interest:")
    for kw, score in list(result.get('product_interest', {}).items())[:5]:
        bar = '█' * (score // 10) + '░' * (10 - score // 10)
        print(f"  {bar}  {score:3d}  {kw}")
