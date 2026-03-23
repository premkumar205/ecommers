import joblib
import pandas as pd
import numpy as np

# Global variables for models
tfidf = None
similarity = None
products_db = None
indices = None

def load_models():
    """Loads all ML models into memory at startup."""
    global tfidf, similarity, products_db, indices
    try:
        tfidf = joblib.load('../model/tfidf.pkl')
        similarity = joblib.load('../model/similarity.pkl')
        products_db = joblib.load('../model/products.pkl')
        indices = joblib.load('../model/indices.pkl')
        print("Successfully loaded ML models.")
    except Exception as e:
        print(f"Error loading models: {e}")

def get_recommendations(product_id: int):
    """
    Returns recommendations based on hybrid content/popularity:
    0.7 * similarity_score + 0.3 * rating_score
    """
    if str(product_id) not in [str(k) for k in indices.keys()]:
        return []

    # Get index of the product
    idx = None
    for k, v in indices.items():
        if str(k) == str(product_id):
            idx = v
            break
            
    if idx is None:
        return []

    # Get pairwise similarity scores
    sim_scores = list(enumerate(similarity[idx]))
    
    # We will compute the hybrid score for each
    hybrid_scores = []
    for i, sim in sim_scores:
        if i == idx:
            continue # skip the item itself
            
        product = products_db[i]
        rating = product.get('Rating', 0)
        try:
            rating = float(rating)
        except:
            rating = 0.0
            
        # Normalize rating to 0-1 scale assuming max rating is 5
        rating_score = rating / 5.0
        
        final_score = 0.7 * sim + 0.3 * rating_score
        hybrid_scores.append((i, final_score))
        
    # Sort products based on hybrid score
    hybrid_scores = sorted(hybrid_scores, key=lambda x: x[1], reverse=True)
    
    # Get top 6
    top_indices = [i[0] for i in hybrid_scores[:6]]
    
    # Return matched products
    return [products_db[i] for i in top_indices]
def search_products(query: str):
    """Simple keyword search across name, category, and brand."""
    if not query:
        return products_db[:20] # Return first 20 if no query
    
    q = query.lower()
    results = []
    for p in products_db:
        name = str(p.get('Product_Name', '')).lower()
        cat = str(p.get('Category', '')).lower()
        brand = str(p.get('Brand', '')).lower()
        if q in name or q in cat or q in brand:
            results.append(p)
            
    return results[:20] # Limit search results for performance
