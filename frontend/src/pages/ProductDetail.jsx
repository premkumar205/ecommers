import React, { useState, useEffect, useContext } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { CartContext } from '../context/CartContext';
import { WishlistContext } from '../context/WishlistContext';
import { fetchProductById, fetchRecommendations } from '../services/api';
import ProductCard from '../components/ProductCard';
import { Star, ShoppingCart, Heart, ShieldCheck, Truck, RotateCcw } from 'lucide-react';
import { toast } from 'react-hot-toast';

const ProductDetail = () => {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  
  const { addToCart } = useContext(CartContext);
  const { toggleWishlist, isInWishlist } = useContext(WishlistContext);

  useEffect(() => {
    const loadProductData = async () => {
      setLoading(true);
      window.scrollTo(0, 0); // Reset scroll on load
      try {
        const prodData = await fetchProductById(id);
        if (!prodData.error) {
           setProduct(prodData);
           const recData = await fetchRecommendations(id);
           setRecommendations(recData.recommended_products || []);
        }
      } catch (err) {
        console.error("Failed to fetch product", err);
      } finally {
        setLoading(false);
      }
    };
    
    loadProductData();
  }, [id]);

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-12 animate-pulse">
        <div className="flex flex-col md:flex-row gap-12">
          <div className="w-full md:w-1/2 h-[500px] bg-gray-200 rounded-2xl"></div>
          <div className="w-full md:w-1/2 space-y-6">
            <div className="h-10 bg-gray-200 rounded w-3/4"></div>
            <div className="h-6 bg-gray-200 rounded w-1/4"></div>
            <div className="h-32 bg-gray-200 rounded w-full"></div>
            <div className="h-12 bg-gray-200 rounded w-1/3"></div>
            <div className="flex gap-4">
              <div className="h-14 bg-gray-200 rounded w-1/2 mt-8"></div>
              <div className="h-14 bg-gray-200 rounded w-1/6 mt-8"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="text-center py-20">
        <h2 className="text-2xl font-bold text-gray-900">Product Not Found</h2>
      </div>
    );
  }

  const isWishlisted = isInWishlist(product.Product_ID);
  const ratingStr = product.Rating || "0";
  const rating = parseFloat(ratingStr) || 0;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Breadcrumb */}
      <div className="flex items-center text-sm text-gray-500 mb-8 py-2 overflow-x-auto whitespace-nowrap">
        <Link to="/" className="hover:text-indigo-600 transition-colors">Home</Link>
        <span className="mx-2 text-gray-400">&gt;</span>
        <Link 
          to={`/search?q=${encodeURIComponent((product.Category || "Products").split('>')[0])}`} 
          className="hover:text-indigo-600 transition-colors"
        >
          {(product.Category || "Products").split('>')[0]}
        </Link>
        <span className="mx-2 text-gray-400">&gt;</span>
        <Link 
          to={`/search?q=${encodeURIComponent(product.Brand || "Brand")}`} 
          className="text-gray-900 font-medium hover:text-indigo-600 transition-colors"
        >
          {product.Brand || "Brand"}
        </Link>
      </div>

      <div className="flex flex-col md:flex-row gap-12 lg:gap-16">
        {/* Product Image Gallery */}
        <div className="w-full md:w-1/2 flex justify-center">
            <div className="sticky top-24 bg-gray-50 p-6 rounded-3xl border border-gray-100 w-full max-w-lg aspect-square flex items-center justify-center relative shadow-sm">
              <img 
                src={product.image_url} 
                alt={product.Product_Name}
                className="max-w-full max-h-full object-contain mix-blend-multiply"
                onError={(e) => {
                   e.target.onerror = null;
                   e.target.src = "https://placehold.co/600x600/7c3aed/FFFFFF?text=Product";
                }}
              />
              <button 
                  onClick={() => {
                    toggleWishlist(product);
                    if (!isWishlisted) toast.success('Added to Wishlist');
                  }}
                  className="absolute top-6 right-6 p-3 bg-white rounded-full shadow-md hover:scale-110 transition-transform"
              >
                  <Heart size={24} className={isWishlisted ? "text-red-500 fill-current" : "text-gray-400"} />
              </button>
            </div>
        </div>

        {/* Product Info */}
        <div className="w-full md:w-1/2 flex flex-col pt-2">
          <div className="mb-2">
            <span className="bg-indigo-100 text-indigo-800 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">
              {product.Brand || "Premium Brand"}
            </span>
          </div>
          
          <h1 className="text-3xl sm:text-4xl font-extrabold text-gray-900 mb-4 leading-tight">
            {product.Product_Name}
          </h1>
          
          <div className="flex items-center gap-4 mb-6 pb-6 border-b border-gray-200">
             <div className="flex items-center text-yellow-500 bg-yellow-50 px-3 py-1 rounded-full">
               <Star size={18} fill="currentColor" className="mr-1" />
               <span className="font-bold text-gray-900">{rating.toFixed(1)}</span>
             </div>
             <span className="text-gray-500 text-sm">
               | <span className="ml-2 hover:text-indigo-600 cursor-pointer underline decoration-dotted underline-offset-4">Read reviews</span>
             </span>
          </div>

          <div className="text-4xl font-black text-gray-900 mb-8 flex items-end tracking-tight">
             {product.Price}
             <span className="text-sm font-normal text-gray-500 mb-1 ml-2 tracking-normal block">Incl. of all taxes</span>
          </div>

          <h3 className="font-bold text-gray-900 mb-2 text-lg">About this item</h3>
          <p className="text-gray-600 mb-8 leading-relaxed whitespace-pre-line text-lg">
            {product.Description || "No detailed description available for this product."}
          </p>

          <div className="mt-auto space-y-4 pt-6 text-gray-500 text-sm border-t border-gray-100 mb-8">
            <div className="flex items-center p-3 rounded-lg bg-gray-50"><ShieldCheck className="text-green-500 mr-3" /> 1 Year Brand Warranty</div>
            <div className="flex items-center p-3 rounded-lg bg-gray-50"><RotateCcw className="text-blue-500 mr-3" /> 30 Day Return Policy</div>
            <div className="flex items-center p-3 rounded-lg bg-gray-50"><Truck className="text-indigo-500 mr-3" /> Free Express Delivery</div>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 mt-4">
            <button 
                onClick={() => {
                  addToCart(product);
                  toast.success('Added to Cart');
                }}
                className="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white py-4 px-8 rounded-xl font-bold text-lg shadow-lg hover:shadow-indigo-500/30 transition-all flex items-center justify-center"
            >
              <ShoppingCart size={22} className="mr-3" />
              Add to Cart
            </button>
            <button 
              onClick={() => { addToCart(product); navigate('/cart'); }}
              className="flex-1 bg-gray-900 hover:bg-black text-white py-4 px-8 rounded-xl font-bold text-lg shadow-lg transition-all"
            >
              Buy Now
            </button>
          </div>
        </div>
      </div>

      {/* Recommendations Section */}
      {recommendations.length > 0 && (
        <div className="mt-24 border-t border-gray-200 pt-16">
          <div className="flex justify-between items-center mb-8">
             <h2 className="text-3xl font-extrabold text-gray-900">
               Customers who viewed this also viewed
             </h2>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
            {recommendations.map(rec => (
              <ProductCard key={rec.Product_ID} product={{...rec, Product_Name: rec.Product_Name.substring(0,40)+"..."}} /> // Truncate name for smaller cards
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ProductDetail;
