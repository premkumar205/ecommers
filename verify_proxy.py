import httpx
import urllib.parse

prompt = "A professional shot of a Running Shoes made of organic cotton. The item is resting on a polished white marble surface. Featuring soft studio lighting with gentle shadows, macro 85mm lens close-up focusing on texture. Real catalog photography with authentic textures and sophisticated atmosphere."
url = f"http://localhost:8000/api/image?id=1&prompt={urllib.parse.quote(prompt)}"

try:
    with httpx.Client(timeout=10.0) as client:
        resp = client.get(url, follow_redirects=True)
        print(f"Status: {resp.status_code}")
        print(f"Content-Type: {resp.headers.get('Content-Type')}")
        print(f"Content Length: {len(resp.content)}")
except Exception as e:
    print(f"Error: {e}")
