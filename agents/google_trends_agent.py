# google_trends_agent.py - REAL DATA VERSION (Improved)
from pytrends.request import TrendReq
from datetime import datetime
import time


class GoogleTrendsAgent:
    def __init__(self):
        self.name = "Google Trends Agent (Real)"
        # tz=240 = UAE timezone (GMT+4)
        self.pytrends = TrendReq(hl='en-US', tz=240, timeout=(10, 25))

        # Dropshipping product categories with keywords
        self.CATEGORY_KEYWORDS = {
            "kitchen_gadgets":   ['chopper', 'blender', 'air fryer', 'kitchen', 'cook', 'recipe', 'grater', 'slicer'],
            "cooling_gadgets":   ['fan', 'portable ac', 'cooling', 'ice maker', 'mist fan', 'neck fan'],
            "beauty_health":     ['hair', 'skin', 'face', 'cream', 'serum', 'massager', 'beauty', 'gua sha'],
            "fitness":           ['gym', 'workout', 'resistance band', 'yoga', 'protein', 'fitness', 'exercise'],
            "home_organization": ['organizer', 'storage', 'shelf', 'rack', 'drawer', 'closet', 'hanger'],
            "phone_accessories": ['phone case', 'charger', 'cable', 'airpods', 'wireless', 'holder', 'stand'],
            "baby_kids":         ['baby', 'kids', 'toddler', 'toy', 'stroller', 'feeding', 'diaper'],
            "car_accessories":   ['car', 'dashboard', 'seat cover', 'parking', 'auto', 'vehicle'],
            "pet_products":      ['dog', 'cat', 'pet', 'paw', 'leash', 'collar', 'feeder'],
            "cleaning":          ['mop', 'vacuum', 'cleaning', 'scrubber', 'spray', 'wash', 'dust'],
        }

        # Products to actively search on Google Trends for UAE
        self.PRODUCT_SEED_KEYWORDS = [
            ["portable fan", "neck fan", "mini fan"],
            ["air fryer", "vegetable chopper", "food processor"],
            ["hair removal", "facial massager", "skin care"],
            ["phone stand", "wireless charger", "cable organizer"],
            ["home organizer", "storage box", "drawer divider"],
        ]

    # ─────────────────────────────────────────────
    # MAIN METHOD
    # ─────────────────────────────────────────────
    def get_uae_trends(self):
        """Get real trending data for UAE dropshipping"""
        try:
            trending_searches   = self._get_trending_searches()
            product_interest    = self._get_product_interest()
            rising_queries      = self._get_rising_queries()

            all_trends = trending_searches + rising_queries
            categories = self._detect_categories(all_trends)

            return {
                "current_season":   self._detect_season(),
                "hot_categories":   categories,
                "rising_searches":  all_trends[:8],
                "product_interest": product_interest,   # which seeds are hot right now
                "timestamp":        datetime.now().isoformat(),
                "data_source":      "real"
            }

        except Exception as e:
            print(f"⚠️  Google Trends error: {e}")
            return self._get_fallback_data()

    # ─────────────────────────────────────────────
    # STEP 1 — Daily trending searches (UAE)
    # ─────────────────────────────────────────────
    def _get_trending_searches(self):
        """
        pytrends country codes: use short ISO codes.
        UAE = 'united_arab_emirates' for trending_searches()
        """
        try:
            df = self.pytrends.trending_searches(pn='united_arab_emirates')
            return df.head(15).values.flatten().tolist()
        except Exception as e:
            print(f"   trending_searches error: {e}")
            return []

    # ─────────────────────────────────────────────
    # STEP 2 — Interest over time for product seeds
    # ─────────────────────────────────────────────
    def _get_product_interest(self):
        """
        Check which product categories are trending in UAE right now.
        Returns dict: {keyword: interest_score 0-100}
        """
        results = {}
        for keyword_group in self.PRODUCT_SEED_KEYWORDS:
            try:
                self.pytrends.build_payload(
                    kw_list=keyword_group,
                    cat=0,
                    timeframe='now 7-d',   # last 7 days
                    geo='AE',              # UAE
                    gprop=''
                )
                df = self.pytrends.interest_over_time()
                if not df.empty:
                    for kw in keyword_group:
                        if kw in df.columns:
                            score = int(df[kw].mean())
                            if score > 10:   # ignore low-interest keywords
                                results[kw] = score
                time.sleep(1)   # be polite to Google's API
            except Exception as e:
                print(f"   interest_over_time error for {keyword_group}: {e}")
                continue

        # Sort by interest score descending
        return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))

    # ─────────────────────────────────────────────
    # STEP 3 — Rising related queries
    # ─────────────────────────────────────────────
    def _get_rising_queries(self):
        """Get rising queries related to trending products in UAE"""
        rising = []
        # Use just one seed group to avoid rate limits
        try:
            self.pytrends.build_payload(
                kw_list=['buy online', 'best product'],
                timeframe='now 7-d',
                geo='AE'
            )
            related = self.pytrends.related_queries()
            for kw in related:
                data = related[kw]
                if data and data.get('rising') is not None:
                    top_rising = data['rising'].head(5)['query'].tolist()
                    rising.extend(top_rising)
            time.sleep(1)
        except Exception as e:
            print(f"   related_queries error: {e}")

        return rising[:10]

    # ─────────────────────────────────────────────
    # HELPERS
    # ─────────────────────────────────────────────
    def _detect_categories(self, trends):
        """Map trending search terms to dropshipping categories"""
        found = {}
        for trend in trends:
            trend_lower = str(trend).lower()
            for category, keywords in self.CATEGORY_KEYWORDS.items():
                if any(k in trend_lower for k in keywords):
                    found[category] = found.get(category, 0) + 1

        # Sort by frequency, return top 5
        sorted_cats = sorted(found.items(), key=lambda x: x[1], reverse=True)
        return [cat for cat, _ in sorted_cats[:5]] or ["general"]

    def _detect_season(self):
        month = datetime.now().month
        if 5 <= month <= 9:
            return "summer"     # UAE summer = very hot, cooling products win
        elif 10 <= month <= 11:
            return "autumn"
        elif month == 12 or month <= 2:
            return "winter"     # UAE "winter" = mild, outdoor products win
        else:
            return "spring"

    def _get_fallback_data(self):
        """Used only when Google Trends is rate-limiting or down"""
        return {
            "current_season":   self._detect_season(),
            "hot_categories":   ["cooling_gadgets", "kitchen_gadgets", "beauty_health"],
            "rising_searches":  ["ice maker", "portable fan", "air fryer", "hair removal"],
            "product_interest": {"portable fan": 80, "air fryer": 65, "hair removal": 55},
            "timestamp":        datetime.now().isoformat(),
            "data_source":      "fallback"
        }


# ─────────────────────────────────────────────────
# Quick test — run this file directly to check
# ─────────────────────────────────────────────────
if __name__ == "__main__":
    agent = GoogleTrendsAgent()
    print("Testing Google Trends Agent (UAE)...\n")
    result = agent.get_uae_trends()

    print(f"Season:          {result['current_season']}")
    print(f"Hot categories:  {result['hot_categories']}")
    print(f"Rising searches: {result['rising_searches'][:5]}")
    print(f"Product interest (top 5):")
    interest = result.get('product_interest', {})
    for kw, score in list(interest.items())[:5]:
        bar = '█' * (score // 10) + '░' * (10 - score // 10)
        print(f"  {bar}  {score:3d}  {kw}")
    print(f"\nData source: {result['data_source']}")
    print(f"Timestamp:   {result['timestamp']}")
