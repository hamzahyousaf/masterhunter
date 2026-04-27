# agents/omkar_amazon_agent.py
import requests
import os

class OmkarAmazonAgent:
    def __init__(self):
        self.name = "Omkar Amazon Agent"
        # 👇 BAS YAHAN APNI KEY DALO (double quotes ke andar)
        self.api_key = "ok_c8d2da1c4624796bcab421c08ea11472"
        self.base_url = "https://api.omkar.cloud"  # Official Base URL
    
    def search_products(self, keyword="kitchen gadgets", country="ae"):
        """Amazon UAE mein products search karo"""
        url = f"{self.base_url}/amazon/search"
        headers = {"X-API-Key": self.api_key}
        
        # 'ae' country code automatically amazon.ae target karega
        params = {"q": keyword, "country": country, "max": 20}
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                
                # OmkarCloud ka response structure standard hota hai
                items = data.get('items', []) or data.get('results', [])
                if not items and 'products' in data:
                    items = data['products']
                
                products = []
                for item in items[:10]:
                    # Price safely extract karo
                    price = item.get('price')
                    if isinstance(price, dict):
                        price = price.get('value', 0)
                    
                    products.append({
                        'id': f"ok_{item.get('asin', '')}",
                        'name': item.get('title', ''),
                        'price': float(price) if price else 0,
                        'rating': float(item.get('rating', 0)),
                        'reviews': item.get('reviews_count', 0),
                        'source': 'omkar_amazon',
                        'margin': 40
                    })
                return products
            else:
                print(f"API Error {response.status_code}: {response.text[:100]}")
        except Exception as e:
            print(f"Request Failed: {e}")
        
        # Fallback Mock Data
        return [
            {"id": "fallback_1", "name": f"{keyword} Gadget", "price": 49, "margin": 40}
        ]
    
    def get_formatted_for_master(self):
        products = self.search_products()
        return [{'id': p['id'], 'name': p['name'], 'price': p['price'], 'amazon_trend': True} 
                for p in products]
