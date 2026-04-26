# tiktok_agent.py - FREE VERSION (No API Key)
from TikTokApi import TikTokApi
import asyncio

class TikTokViralAgent:
    def __init__(self):
        self.name = "TikTok Agent (Free)"
    
    def get_trending_products(self, hashtag="kitchen", limit=20):
        async def fetch():
            async with TikTokApi() as api:
                await api.create_sessions(num_sessions=1, sleep_after=3)
                results = []
                async for video in api.trending.videos(count=limit):
                    data = video.as_dict
                    stats = data.get('stats', {})
                    results.append({
                        'name': self._extract_product(data.get('desc', '')),
                        'tiktok_views': stats.get('playCount', 0),
                        'tiktok_likes': stats.get('diggCount', 0),
                        'tiktok_shares': stats.get('shareCount', 0),
                        'hashtags': [tag['title'] for tag in data.get('challenges', [])]
                    })
                return results
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            products = loop.run_until_complete(fetch())
        finally:
            loop.close()
        return products
    
    def _extract_product(self, desc):
        words = desc.split()[:6]
        return ' '.join(words) if words else "Trending Product"
    
    def get_formatted_for_master(self):
        products = self.get_trending_products()
        return [{
            'id': f"tt_{i}",
            'name': p['name'],
            'tiktok_views': p['tiktok_views'],
            'tiktok_likes': p['tiktok_likes']
        } for i, p in enumerate(products)]
