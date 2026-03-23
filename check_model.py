import joblib
try:
    products = joblib.load('model/products.pkl')
    print(f"Total products: {len(products)}")
    first = products[0]
    print(f"Keys: {list(first.keys())}")
    print(f"Name: {first.get('Product_Name')}")
    print(f"Prompt: {first.get('AI_Image_Prompt')}")
except Exception as e:
    print(f"Error: {e}")
