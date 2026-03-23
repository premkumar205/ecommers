import asyncio
import httpx
import pandas as pd
import os
from bulk_generate_images import download_image

async def debug_one(p_id):
    df = pd.read_excel('dataset/product_recommendation_dataset_cleaned.xlsx')
    product = df[df['Product_ID'] == p_id].iloc[0]
    
    print(f"DEBUG ID {p_id}: {product['Product_Name']}")
    print(f"Category: {product.get('Category')}")
    
    headers = {"User-Agent": "Mozilla/5.0"}
    async with httpx.AsyncClient(headers=headers) as client:
        res = await download_image(client, product)
        print(f"Result: {res}")
        
    save_path = f"dataset/images/product_{p_id}.jpg"
    if os.path.exists(save_path):
        print(f"FILE EXISTS: {save_path}, Size: {os.path.getsize(save_path)}")
    else:
        print(f"FILE MISSING: {save_path}")

if __name__ == "__main__":
    import sys
    pid = int(sys.argv[1]) if len(sys.argv) > 1 else 252
    asyncio.run(debug_one(pid))
