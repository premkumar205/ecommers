import asyncio
import httpx
import pandas as pd
import urllib.parse
import os
import random

IMAGE_DIR = 'dataset/images/'
ERROR_SIGNATURE_SIZE = 308840

def extract_keywords(prompt):
    filler = {"a", "an", "the", "professional", "shot", "of", "high", "quality", "with", "isolated", "background", "white"}
    words = [w.strip(",.") for w in prompt.lower().split() if w.lower().strip(",.") not in filler]
    return ",".join(words[:4])

async def verbose_download(client, product):
    p_id = product['Product_ID']
    p_name = product['Product_Name']
    raw_prompt = product['AI_Image_Prompt']
    category = product.get('Category', 'Product')
    
    clean_name = p_name.split("...")[0].replace("..", "").strip()
    refined_prompt = f"Professional STUDIO PRODUCT photography of a {clean_name} ({category}), high-end e-commerce style, isolated on white background, 4k, hyper-realistic, no humans, no faces"
    
    # Tier 1: AI
    print(f"Refined Prompt: {refined_prompt}")
    for attempt in range(2):
        seed = random.randint(1, 1000000)
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(refined_prompt)}?width=1024&height=1024&nologo=true&seed={seed}"
        try:
            print(f"Attempt {attempt+1} Tier 1: {url}")
            resp = await client.get(url, timeout=30.0, follow_redirects=True)
            print(f"Status: {resp.status_code}, Length: {len(resp.content)}")
            if resp.status_code == 200:
                if len(resp.content) == ERROR_SIGNATURE_SIZE:
                    print("ERROR: Received the cat statue signature.")
                elif len(resp.content) < 10000:
                    print(f"ERROR: Image too small ({len(resp.content)} bytes).")
                else:
                    save_path = os.path.join(IMAGE_DIR, f"product_{p_id}.jpg")
                    with open(save_path, 'wb') as f:
                        f.write(resp.content)
                    print("SUCCESS (Tier 1)")
                    return True
        except Exception as e:
            print(f"EXCEPTION Tier 1: {e}")
            
    # Tier 2: LoremFlickr
    try:
        keywords = extract_keywords(raw_prompt)
        flickr_url = f"https://loremflickr.com/1024/1024/{urllib.parse.quote(keywords)}?lock={p_id}"
        print(f"Attempt Tier 2: {flickr_url}")
        resp = await client.get(flickr_url, timeout=15.0, follow_redirects=True)
        print(f"Status: {resp.status_code}, Length: {len(resp.content)}")
        if resp.status_code == 200:
            if len(resp.content) == ERROR_SIGNATURE_SIZE:
                print("ERROR: Received cat statue signature from Tier 2.")
            elif len(resp.content) < 10000:
                print(f"ERROR: Image too small Tier 2.")
            else:
                save_path = os.path.join(IMAGE_DIR, f"product_{p_id}.jpg")
                with open(save_path, 'wb') as f:
                    f.write(resp.content)
                print("SUCCESS (Tier 2)")
                return True
    except Exception as e:
        print(f"EXCEPTION Tier 2: {e}")
        
    return False

async def main():
    df = pd.read_excel('dataset/product_recommendation_dataset_cleaned.xlsx')
    product = df[df['Product_ID'] == 6].iloc[0]
    async with httpx.AsyncClient() as client:
        await verbose_download(client, product)

if __name__ == "__main__":
    asyncio.run(main())
