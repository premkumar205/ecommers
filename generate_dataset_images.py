import pandas as pd
import asyncio
import httpx
import os
import urllib.parse
import shutil
from tqdm.asyncio import tqdm

# Settings
DATASET_PATH = 'dataset/product_recommendation_dataset_cleaned.xlsx'
CLEANED_DATASET_PATH = 'dataset/product_recommendation_dataset_cleaned.xlsx'
IMAGE_DIR = 'dataset/images'
CONCURRENCY_LIMIT = 5
RETRIES = 3
TIMEOUT = 30.0
POLLINATIONS_TIMEOUT = 20.0
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

os.makedirs(IMAGE_DIR, exist_ok=True)

def get_gold_path(prompt):
    p_lower = str(prompt).lower()
    if any(k in p_lower for k in ["phone", "smartphone", "iphone", "mobile"]): return "dataset/placeholders/gold_smartphone.jpg"
    if any(k in p_lower for k in ["speaker", "audio", "soundbar", "jbl"]): return "dataset/placeholders/gold_speaker.jpg"
    if any(k in p_lower for k in ["shoe", "sneaker", "running", "footwear", "nike"]): 
        if "phone" not in p_lower: # Avoid mismatch with 'nike phone case' etc.
            return "dataset/placeholders/gold_shoes.jpg"
    if any(k in p_lower for k in ["watch", "smartwatch", "apple watch"]): return "dataset/placeholders/gold_watch.jpg"
    if any(k in p_lower for k in ["laptop", "computer", "macbook", "keyboard"]): return "dataset/placeholders/gold_laptop.jpg"
    if any(k in p_lower for k in ["beauty", "perfume", "makeup", "serum", "lipstick"]): return "dataset/placeholders/gold_beauty.jpg"
    if any(k in p_lower for k in ["clothing", "shirt", "dress", "hoodie", "jacket"]): return "dataset/placeholders/gold_clothing.jpg"
    if any(k in p_lower for k in ["football", "cricket", "sports", "skipping rope"]): return "dataset/placeholders/sports.jpg"
    return None

async def download_image(client, sem, product_id, full_prompt):
    filename = f"product_{product_id}.jpg"
    filepath = os.path.join(IMAGE_DIR, filename)
    image_path = f"/images/{filename}"
    
    # Priority 1: Local Gold Visual (High Quality, Fast)
    gold_src = get_gold_path(full_prompt)
    if gold_src and os.path.exists(gold_src):
        print(f"Match Gold: {product_id} -> {gold_src}")
        shutil.copy(gold_src, filepath)
        return image_path
        
    # Priority 2: LoremFlickr (Thematic, Remote)
    try:
        category = "electronics"
        if "phone" in full_prompt.lower(): category = "smartphone"
        elif "speaker" in full_prompt.lower(): category = "speaker"
        elif "shoe" in full_prompt.lower(): category = "shoes"
        elif "watch" in full_prompt.lower(): category = "watch"
        elif "laptop" in full_prompt.lower(): category = "laptop"
        elif "beauty" in full_prompt.lower(): category = "beauty"
        
        lorem_url = f"https://loremflickr.com/1024/1024/{category}?lock={product_id}"
        async with sem:
            response = await client.get(lorem_url, timeout=TIMEOUT, follow_redirects=True, headers=HEADERS)
            if response.status_code == 200 and len(response.content) > 30000:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                return image_path
    except Exception:
        pass
        
    # Final Fallback: Placeholder JPG
    try:
        placeholder_url = f"https://placehold.co/1024x1024.jpg?text=Product+{product_id}"
        async with sem:
            response = await client.get(placeholder_url, timeout=TIMEOUT, headers=HEADERS)
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                return image_path
    except Exception:
        pass
        
    return image_path

async def main():
    print("Loading dataset...")
    df = pd.read_excel(DATASET_PATH)
    
    # Load custom prompts if they exist
    prompts_csv_path = 'product_prompts.csv'
    if os.path.exists(prompts_csv_path):
        print(f"Loading custom prompts from {prompts_csv_path}...")
        prompts_df = pd.read_csv(prompts_csv_path)
        if 'Product_ID' in prompts_df.columns:
            df = df.merge(prompts_df[['Product_ID', 'Prompt']], on='Product_ID', how='left')
            if 'AI_Image_Prompt' in df.columns:
                df['AI_Image_Prompt'] = df['Prompt'].fillna(df['AI_Image_Prompt'])
            else:
                df['AI_Image_Prompt'] = df['Prompt']
            df.drop(columns=['Prompt'], inplace=True)
            print("Successfully merged custom prompts.")
    
    df.fillna("Unknown", inplace=True)
    for col in df.select_dtypes(['object']).columns:
        df[col] = df[col].astype(str).str.strip()
    if 'Image_URL' in df.columns:
        df.drop(columns=['Image_URL'], inplace=True)
        
    print(f"Total rows to process: {len(df)}")
    
    sem = asyncio.Semaphore(CONCURRENCY_LIMIT)
    timeout_cfg = httpx.Timeout(40.0, connect=10.0)
    
    async with httpx.AsyncClient(timeout=timeout_cfg) as client:
        print("Starting batch image processing (Local Gold + LoremFlickr)...")
        tasks = []
        for index, row in df.iterrows():
            prod_id = row.get('Product_ID', index + 1)
            prompt = row.get('AI_Image_Prompt', 'product photography')
            tasks.append(download_image(client, sem, prod_id, prompt))
            
        results = await tqdm.gather(*tasks, desc="Generating images")
            
    df['image_path'] = results
    
    print(f"Saving cleaned dataset to {CLEANED_DATASET_PATH}...")
    df.to_excel(CLEANED_DATASET_PATH, index=False)
    print("Execution completed!")

if __name__ == "__main__":
    asyncio.run(main())
