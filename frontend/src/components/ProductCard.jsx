import React, { useState, useContext } from 'react';
import { Link } from 'react-router-dom';
import { CartContext } from '../context/CartContext';
import { WishlistContext } from '../context/WishlistContext';
import { Heart, ShoppingCart, Star } from 'lucide-react';
import { toast } from 'react-hot-toast';

const ProductCard = ({ product }) => {
  const { addToCart } = useContext(CartContext);
  const { toggleWishlist, isInWishlist } = useContext(WishlistContext);
  const [imgLoaded, setImgLoaded] = useState(false);
  const isWishlisted = isInWishlist(product.Product_ID);

  // Parse rating
  const ratingStr = product.Rating || "0";
  const rating = parseFloat(ratingStr) || 0;

  console.log("Rendering ProductCard for:", product);

  return (
    <div className="bg-white rounded-xl shadow-sm hover:shadow-xl transition-shadow duration-300 overflow-hidden flex flex-col group border border-gray-100">
      <Link to={`/product/${product.Product_ID}`} className="relative block h-64 overflow-hidden bg-gray-50">
        <img
          src={product.image_url}
          alt={product.Product_Name}
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
          onError={(e) => {
             e.target.onerror = null; 
             e.target.src = "https://placehold.co/300x300/7c3aed/FFFFFF?text=Product";
          }}
          loading="lazy"
        />
        {/* Category Badge */}
        {product.Category && (
            <span className="absolute top-2 left-2 bg-indigo-600 text-white text-xs font-bold px-2 py-1 rounded shadow-sm opacity-90 z-10">
                {(product.Category || "").split('>')[0]?.trim() || product.Category}
            </span>
        )}
      </Link>

      <div className="p-4 flex flex-col flex-grow">
        <Link to={`/product/${product.Product_ID}`} className="block mt-auto flex-grow block">
            <span className="text-xs text-gray-500 font-semibold uppercase tracking-wider block mb-1">
                {product.Brand || "Brand"}
            </span>
            <h3 className="font-bold text-gray-900 text-lg leading-tight mb-2 line-clamp-2 hover:text-indigo-600 transition-colors">
                {product.Product_Name}
            </h3>
        </Link>
        
        <div className="flex items-center mb-3">
          <div className="flex items-center text-yellow-500">
            <Star size={16} fill="currentColor" />
            <span className="ml-1 text-sm font-bold text-gray-700">{rating.toFixed(1)}</span>
          </div>
        </div>

        <div className="flex items-center justify-between mt-auto pt-4 border-t border-gray-100">
          <span className="text-xl font-extrabold text-gray-900">
            {product.Price}
          </span>
          <div className="flex space-x-2">
            <button
              onClick={(e) => { 
                e.preventDefault(); 
                toggleWishlist(product); 
                if (!isWishlisted) toast.success('Added to Wishlist');
              }}
              className={`p-2 rounded-full transition-colors ${
                isWishlisted 
                  ? 'bg-red-50 text-red-500 hover:bg-red-100' 
                  : 'bg-gray-50 text-gray-400 hover:bg-gray-100 hover:text-red-500'
              }`}
              title="Add to Wishlist"
            >
              <Heart size={20} fill={isWishlisted ? "currentColor" : "none"} />
            </button>
            <button
              onClick={(e) => { 
                e.preventDefault(); 
                addToCart(product); 
                toast.success('Added to Cart');
              }}
              className="p-2 bg-indigo-600 text-white rounded-full hover:bg-indigo-700 transition-colors shadow-sm"
              title="Add to Cart"
            >
              <ShoppingCart size={20} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
