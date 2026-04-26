# tiktok_agent.py - FREE VERSION (No API Key)
import asyncio

class TikTokViralAgent:
    def __init__(self):
        self.name = "TikTok Agent (Free)"
    
    def get_viral_products(self):
        """Get trending products from TikTok"""
        try:
            # Try to fetch real data
            products = self._fetch_trending()
            if products:
                return products
        except Exception as e:
            print(f"⚠️ TikTok fetch error: {e}")
        
        # Fallback to mock data
        return self._get_mock_products()
    
    def _fetch_trending(self):
        """Attempt to fetch real TikTok data"""
        try:
            from TikTokApi import TikTokApi
            
            async def fetch():
                async with TikTokApi() as api:
                    await api.create_sessions(num_sessions=1, headless=True)
                    results = []
                    async for video in api.trending.videos(count=15):
                        data = video.as_dict
                        stats = data.get('stats', {})
                        results.append({
                            'name': self._extract_product_name(data.get('desc', '')),
                            'tiktok_views': stats.get('playCount', 0),
                            'tiktok_likes': stats.get('diggCount', 0),
                            'hashtags': data.get('challenges', [])
                        })
                    return results
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            products = loop.run_until_complete(fetch())
            loop.close()
            return products
        except:
            return []
    
    def _extract_product_name(self, description):
        """Extract potential product name from video description"""
        words = description.split()[:5]
        return ' '.join(words) if words else "Trending Product"
    
    def _get_mock_products(self):
        return [
            {"name": "Ice Maker Machine", "tiktok_views": 5200000, "category": "cooling"},
            {"name": "Portable Neck Fan", "tiktok_views": 3800000, "category": "cooling"},
            {"name": "Vegetable Chopper", "tiktok_views": 4500000, "category": "kitchen"},
            {"name": "Cold Brew Pitcher", "tiktok_views": 2100000, "category": "cooling"},
            {"name": "Garlic Press", "tiktok_views": 1800000, "category": "kitchen"}
        ]
    
    def get_formatted_for_master(self):
        products = self.get_viral_products()
        return [{
            'id': f"tt_{i}",
            'name': p['name'],
            'tiktok_views': p['tiktok_views'],
            'tiktok_likes': p.get('tiktok_likes', 0)
        } for i, p in enumerate(products)]
