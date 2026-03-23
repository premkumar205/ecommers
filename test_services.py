import httpx
import time

def test_service(name, url):
    print(f"Testing {name}: {url}")
    try:
        start = time.time()
        resp = httpx.get(url, follow_redirects=True, timeout=10.0)
        duration = time.time() - start
        print(f"  Status: {resp.status_code}")
        print(f"  Type: {resp.headers.get('Content-Type')}")
        print(f"  Length: {len(resp.content)}")
        print(f"  Time: {duration:.2f}s")
        if resp.status_code == 200 and len(resp.content) > 2000:
            print("  SUCCESS")
            return True
    except Exception as e:
        print(f"  FAILED: {e}")
    return False

# Test Pollinations (with a simple prompt)
test_service("Pollinations", "https://image.pollinations.ai/prompt/smartphone?width=512&height=512&nologo=true")

# Test Unsplash Source
test_service("Unsplash", "https://source.unsplash.com/512x512/?smartphone")

# Test LoremFlickr
test_service("LoremFlickr", "https://loremflickr.com/512/512/smartphone")
