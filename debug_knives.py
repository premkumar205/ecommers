import joblib
import pandas as pd

try:
    products = joblib.load('c:/Users/yadav/Downloads/pjt/model/products.pkl')
    print(f"Total products: {len(products)}")
    
    knife_products = [p for p in products if 'knife' in str(p.get('Product_Name', '')).lower()]
    print(f"Knife products found: {len(knife_products)}")
    
    for p in knife_products[:5]:
        print(f"ID: {p.get('Product_ID')}")
        print(f"Name: {p.get('Product_Name')}")
        print(f"Category: {p.get('Category')}")
        print(f"AI_Image_Prompt: {p.get('AI_Image_Prompt')}")
        print("-" * 20)
except Exception as e:
    print(f"Error: {e}")
