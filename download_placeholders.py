import httpx
import os

categories = {
    "beauty": "makeup,cosmetics,beauty",
    "electronics": "laptop,camera,gadget",
    "clothing": "fashion,clothing,apparel",
    "home": "interior,home,furniture",
    "sports": "fitness,sports,equipment"
}

os.makedirs("dataset/placeholders", exist_ok=True)

for name, tags in categories.items():
    print(f"Downloading {name}...")
    # Try multiple sources
    urls = [
        f"https://source.unsplash.com/featured/1024x1024/?{tags}",
        f"https://loremflickr.com/1024/1024/{name}",
        f"https://picsum.photos/1024/1024"
    ]
    
    success = False
    for url in urls:
        try:
            resp = httpx.get(url, follow_redirects=True, timeout=15.0)
            if resp.status_code == 200 and len(resp.content) > 10000:
                with open(f"dataset/placeholders/{name}.jpg", "wb") as f:
                    f.write(resp.content)
                print(f"  Saved from {url}")
                success = True
                break
        except Exception as e:
            print(f"  Failed {url}: {e}")
    
    if not success:
        print(f"  CRITICAL: Could not download {name}")
