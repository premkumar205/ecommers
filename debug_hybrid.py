import httpx
import asyncio
import os
import urllib.parse
import random

async def check():
    p_id = 1
    prompt = "A professional shot of a NIKE Running Shoes"
    save_path = f"dataset/images/product_{p_id}.jpg"
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    async with httpx.AsyncClient(headers=headers) as client:
        # Tier 1: AI
        seed = random.randint(1, 1000000)
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=1024&height=1024&nologo=true&seed={seed}"
        print(f"Trying AI: {url}")
        try:
            resp = await client.get(url, timeout=20.0, follow_redirects=True)
            print(f"  AI Status: {resp.status_code}")
            if resp.status_code == 200:
                print(f"  AI Content Type: {resp.headers.get('content-type')}")
                print(f"  AI Content Length: {len(resp.content)}")
                if resp.content.startswith(b'\xff\xd8') or b'JFIF' in resp.content[:50]:
                    with open(save_path, 'wb') as f:
                        f.write(resp.content)
                    print("  [AI SUCCESS] Saved.")
                    return
                else:
                    print("  [AI FAIL] Not a JPEG.")
        except Exception as e:
            print(f"  [AI EXCEPTION] {e}")

        # Tier 2: Unsplash
        keywords = ",".join(prompt.split()[:3])
        unsplash_url = f"https://source.unsplash.com/featured/1024x1024/?{urllib.parse.quote(keywords)}"
        print(f"Trying Unsplash: {unsplash_url}")
        try:
            resp = await client.get(unsplash_url, timeout=15.0, follow_redirects=True)
            print(f"  Unsplash Status: {resp.status_code}")
            if resp.status_code == 200:
                print(f"  Unsplash Content Type: {resp.headers.get('content-type')}")
                with open(save_path, 'wb') as f:
                    f.write(resp.content)
                print("  [UNSPLASH SUCCESS] Saved.")
                return
        except Exception as e:
            print(f"  [UNSPLASH EXCEPTION] {e}")

if __name__ == "__main__":
    asyncio.run(check())
