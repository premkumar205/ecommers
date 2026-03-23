import joblib
import pandas as pd

try:
    products = joblib.load('c:/Users/yadav/Downloads/pjt/model/products.pkl')
    
    knife_products = [p for p in products if 'knife' in str(p.get('Product_Name', '')).lower()]
    print(f"Knife products found: {len(knife_products)}")
    
    for p in knife_products:
        p_id = p.get('Product_ID')
        name = p.get('Product_Name')
        prompt = p.get('AI_Image_Prompt', '')
        print(f"ID: {p_id} | Name: {name} | Prompt: {prompt[:50]}...")
except Exception as e:
    print(f"Error: {e}")
