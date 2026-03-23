import os
import random
import urllib.parse
import pandas as pd
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, RedirectResponse
import httpx
from pydantic import BaseModel

# Standardize environment and state
import recommendation

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Standardized headers for image fetching
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
}

class Product(BaseModel):
    Product_ID: int
    Product_Name: str
    Category: str
    Brand: str
    Price: float
    Rating: float
    Description: str
    AI_Image_Prompt: str
    image_path: str
    combined_text: str

@app.on_event("startup")
async def startup_event():
    recommendation.load_models()
    print(f"Server started. Database size: {len(recommendation.products_db) if recommendation.products_db else 0}")

@app.get("/")
async def root():
    return {"message": "Welcome to the E-commerce Backend API"}

@app.get("/products")
async def get_products():
    return recommendation.products_db

@app.get("/product/{product_id}")
async def get_product(product_id: int):
    for product in recommendation.products_db:
        # Robust ID matching (handles floats vs ints)
        try:
            pid = int(float(product['Product_ID']))
            if pid == product_id:
                prompt = product.get('AI_Image_Prompt', product.get('Product_Name', 'product'))
                product['image_url'] = f"http://127.0.0.1:8000/api/image?id={product_id}&prompt={urllib.parse.quote(str(prompt))}"
                return product
        except:
            continue
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/search")
async def search_products(q: str = Query("")):
    results = recommendation.search_products(q)
    for p in results:
        prompt = p.get('AI_Image_Prompt', p.get('Product_Name', 'product'))
        p_id = int(float(p.get('Product_ID')))
        p['image_url'] = f"http://127.0.0.1:8000/api/image?id={p_id}&prompt={urllib.parse.quote(str(prompt))}"
    # Wrap in "products" key for frontend compatibility
    return {"products": results}

@app.get("/featured")
async def get_featured():
    # Return random 8 products as featured
    if not recommendation.products_db: return {"products": []}
    featured = random.sample(recommendation.products_db, min(8, len(recommendation.products_db)))
    for p in featured:
        p_id = int(float(p.get('Product_ID')))
        prompt = p.get('AI_Image_Prompt', p.get('Product_Name', 'product'))
        p['image_url'] = f"http://127.0.0.1:8000/api/image?id={p_id}&prompt={urllib.parse.quote(str(prompt))}"
    return {"products": featured}

@app.get("/top-rated")
async def get_top_rated():
    # Sort by Rating and return top 8
    if not recommendation.products_db: return {"products": []}
    sorted_products = sorted(recommendation.products_db, key=lambda x: float(x.get('Rating', 0)), reverse=True)
    top_rated = sorted_products[:8]
    for p in top_rated:
        p_id = int(float(p.get('Product_ID')))
        prompt = p.get('AI_Image_Prompt', p.get('Product_Name', 'product'))
        p['image_url'] = f"http://127.0.0.1:8000/api/image?id={p_id}&prompt={urllib.parse.quote(str(prompt))}"
    return {"products": top_rated}

@app.get("/api/image")
async def get_image(prompt: str, prod_id: int = Query(None, alias="id")):
    def extract_keywords(p, product_name=""):
        filler = {"a", "an", "the", "professional", "shot", "of", "high", "quality", "with", "isolated", "background", "white", "premium", "top", "rated", "view", "photography", "clean", "minimalist", "and", "for", "in", "on", "at", "by", "is", "it", "to", "from", "atmosphere", "sophisticated", "stunning", "amazing", "beautiful", "gorgeous"}
        words = [w.strip(",.") for w in p.lower().split() if w.lower().strip(",.") not in filler and len(w) > 1]
        if len(words) < 2 and product_name:
            name_words = [w.strip(",.") for w in product_name.lower().split() if w.lower().strip(",.") not in filler]
            for nw in name_words:
                if nw not in words: words.append(nw)
        return " ".join(words[:5])

    def get_premium_gold(p_prompt, category):
        p_lower = p_prompt.lower()
        if "shoe" in p_lower or "sneaker" in p_lower: return "gold_shoes.jpg"
        if "watch" in p_lower: return "gold_watch.jpg"
        if "laptop" in p_lower or "computer" in p_lower: return "gold_laptop.jpg"
        if "dress" in p_lower or "clothing" in p_lower: return "gold_clothing.jpg"
        if "lipstick" in p_lower or "beauty" in p_lower: return "gold_beauty.jpg"
        if "knife" in p_lower or "cutlery" in p_lower or "kitchen" in p_lower: return "gold_home.jpg"
        
        cat_lower = str(category).lower()
        if "beauty" in cat_lower: return "gold_beauty.jpg"
        if "electronics" in cat_lower or "computers" in cat_lower:
            if "phone" in p_lower: return "gold_smartphone.jpg"
            if "speaker" in p_lower: return "gold_speaker.jpg"
            return "gold_laptop.jpg"
        if "clothing" in cat_lower: return "gold_clothing.jpg"
        if "sports" in cat_lower: return "gold_shoes.jpg"
        if "home" in cat_lower or "kitchen" in cat_lower: return "gold_home.jpg"
        return None

    ERROR_SIGNATURE_SIZE = 308840
    p_obj = None
    if prod_id is not None:
        for p in recommendation.products_db:
            try:
                if int(float(p.get('Product_ID'))) == int(prod_id):
                    p_obj = p
                    break
            except: continue
        
        if p_obj:
            category = str(p_obj.get('Category', 'Electronics'))
            potential_path = os.path.join("../dataset", category, f"product_{prod_id}.jpg")
            if not os.path.exists(potential_path):
                potential_path = os.path.join("../dataset", "images", f"product_{prod_id}.jpg")

            if os.path.exists(potential_path):
                size = os.path.getsize(potential_path)
                if size > 5000 and size != ERROR_SIGNATURE_SIZE:
                    with open(potential_path, "rb") as f:
                        return Response(content=f.read(), media_type="image/jpeg")

    # Tier 1: Dynamic Unique Generation
    try:
        if prod_id is not None:
            prod_name = p_obj.get('Product_Name', '') if p_obj else ""
            keywords = extract_keywords(prompt, prod_name)
            final_prompt = f"professional product photography of {keywords}, white background, studio lighting, 8k, highly detailed"
            seed_val = int(prod_id)
            unique_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(final_prompt)}?width=1024&height=1024&nologo=true&seed={seed_val}&model=flux"
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(unique_url, headers=HEADERS)
                if resp.status_code == 200:
                    return Response(content=resp.content, media_type="image/jpeg")
                else:
                    # Tier 2: Fallback to LoremFlickr
                    flickr_url = f"https://loremflickr.com/1024/1024/{urllib.parse.quote(keywords)}"
                    f_resp = await client.get(flickr_url, follow_redirects=True)
                    if f_resp.status_code == 200:
                        return Response(content=f_resp.content, media_type="image/jpeg")
    except Exception as e:
        pass

    # Tier 2: Local Gold Safeguard
    try:
        gold_file = get_premium_gold(prompt, p_obj.get('Category', '') if p_obj else '')
        if gold_file:
            gold_path = os.path.join("../dataset", "placeholders", gold_file)
            if os.path.exists(gold_path):
                with open(gold_path, "rb") as f:
                    return Response(content=f.read(), media_type="image/jpeg")
    except: pass

    # Final Fallback
    return RedirectResponse(url=f"https://placehold.co/1024x1024/0f172a/FFFFFF?text={urllib.parse.quote(prompt[:20])}")

@app.get("/recommend/{product_id}")
async def recommend_products(product_id: int):
    recommended = recommendation.get_recommendations(product_id)
    for p in recommended:
        prompt = p.get('AI_Image_Prompt', p.get('Product_Name', 'product'))
        p_id = int(float(p.get('Product_ID')))
        p['image_url'] = f"http://127.0.0.1:8000/api/image?id={p_id}&prompt={urllib.parse.quote(str(prompt))}"
    return {"recommended_products": recommended}

@app.get("/categories")
async def get_categories():
    categories = sorted(list(set(p['Category'] for p in recommendation.products_db)))
    return categories

@app.get("/category/{category_name}")
async def get_products_by_category(category_name: str):
    results = [p for p in recommendation.products_db if p['Category'] == category_name]
    for p in results:
        prompt = p.get('AI_Image_Prompt', p.get('Product_Name', 'product'))
        p_id = int(float(p.get('Product_ID')))
        p['image_url'] = f"http://127.0.0.1:8000/api/image?id={p_id}&prompt={urllib.parse.quote(str(prompt))}"
    return {"products": results}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
