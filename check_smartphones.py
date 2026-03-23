import joblib
import os

products_db = joblib.load('model/products.pkl')
smartphones = [p for p in products_db if 'Smartphone' in str(p.get('Product_Name', ''))]

print(f"Found {len(smartphones)} smartphones.")
for p in smartphones[:10]:
    p_id = p.get('Product_ID')
    category = p.get('Category', 'Electronics')
    img_path = os.path.join('dataset', category, f'product_{p_id}.jpg')
    exists = os.path.exists(img_path)
    size = os.path.getsize(img_path) if exists else "N/A"
    print(f"ID: {p_id}, Name: {p.get('Product_Name')}, Image: {img_path}, Size: {size}")
