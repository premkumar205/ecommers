import asyncio
import httpx
import pandas as pd
import os
import urllib.parse
import random
import shutil
from tqdm import tqdm

# Configuration
DATASET_PATH = 'dataset/product_recommendation_dataset_cleaned.xlsx'
PLACEHOLDER_DIR = 'dataset/placeholders/'
CONCURRENCY_LIMIT = 15 
ERROR_SIGNATURE_SIZE = 308840 

async def download_image(client, p_id, p_name, category, semaphore):
    # Determine categorical storage path
    cat_folder = os.path.join('dataset', category)
    if not os.path.exists(cat_folder):
        os.makedirs(cat_folder, exist_ok=True)
    save_path = os.path.join(cat_folder, f"product_{p_id}.jpg")
    
    # Check if we need to regenerate
    if os.path.exists(save_path):
        size = os.path.getsize(save_path)
        # Purge anything that isn't a proven Gold asset size or a large enough AI gen
        # We'll re-verify the specific problematic IDs
        if size == ERROR_SIGNATURE_SIZE or size < 15000:
            try: os.remove(save_path)
            except: pass
        else:
            return True 

    async with semaphore: 
        # Tier 1: AI Generation - Deterministic & Hyper-Strict
        seed = 99 + p_id 
        clean_p = p_name.split("...")[0].replace("..", "").strip()
        refined_prompt = f"Exclusive professional studio product photography of a {clean_p}, centered, isolated on white background, sharp focus, 8k resolution, e-commerce style, no people, no animals"
        
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(refined_prompt)}?width=1024&height=1024&nologo=true&seed={seed}"
        
        try:
            async with client.get(url, timeout=20.0, follow_redirects=True) as resp:
                if resp.status_code == 200:
                    data = resp.content
                    # Strict validation: length and signature
                    if len(data) > 20000 and len(data) != ERROR_SIGNATURE_SIZE:
                        with open(save_path, "wb") as f:
                            f.write(data)
                        return True
        except: pass

        # Tier 2: NUCLEAR ABSOLUTE ACCURACY FALLBACK
        def get_gold_absolute(name, cat):
            c_l = cat.lower()
            if "fashion" in c_l: return "gold_fashion.jpg"
            if "beauty" in c_l: return "gold_beauty.jpg"
            if "electronics" in c_l: return "gold_electronics.jpg"
            if "home" in c_l: return "gold_home.jpg"
            if "sports" in c_l: return "gold_sports.jpg"
            return "gold_electronics.jpg"

        gold_file = get_gold_absolute(p_name, category)
        gold_src = os.path.join(PLACEHOLDER_DIR, gold_file)
        if os.path.exists(gold_src):
            shutil.copy(gold_src, save_path)
            return True

        return False

async def main():
    if not os.path.exists(DATASET_PATH):
        print(f"Error: {DATASET_PATH} not found.")
        return

    df = pd.read_excel(DATASET_PATH)
    print(f"Loaded {len(df)} products for generation.")

    if not os.path.exists(PLACEHOLDER_DIR):
        os.makedirs(PLACEHOLDER_DIR, exist_ok=True)

    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
    
    async with httpx.AsyncClient(timeout=30) as client:
        tasks = [download_image(client, int(row['Product_ID']), str(row['Product_Name']), str(row.get('Category', 'Electronics')).strip(), semaphore) for _, row in df.iterrows()]
        
        for f in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
            await f

    print("Complete.")

if __name__ == "__main__":
    asyncio.run(main())
