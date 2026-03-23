import sys
import traceback

try:
    import backend.recommendation as rec
    import backend.image_service as imgs

    print("Loading models...")
    rec.load_models()
    
    print("Loading cache...")
    imgs.load_cache()
    
    print("Startup OK")
except Exception as e:
    print("Exception occurred:")
    traceback.print_exc()
