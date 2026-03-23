import httpx
import asyncio
import os

async def check():
    url = "https://image.pollinations.ai/prompt/A%20professional%20shot%20of%20a%20NIKE%20Running%20Shoes?width=1024&height=1024&nologo=true&seed=123"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, follow_redirects=True, timeout=30)
        print(f"Status: {resp.status_code}")
        print(f"Content-Type: {resp.headers.get('content-type')}")
        print(f"Content Length: {len(resp.content)}")
        print(f"First 100 bytes: {resp.content[:100]}")
        
        if len(resp.content) > 0:
            os.makedirs("test_debug", exist_ok=True)
            with open("test_debug/product_1.jpg", "wb") as f:
                f.write(resp.content)
            print("Saved to test_debug/product_1.jpg")

if __name__ == "__main__":
    asyncio.run(check())
