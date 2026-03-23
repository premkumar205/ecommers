import React, { useContext } from 'react';
import { WishlistContext } from '../context/WishlistContext';
import ProductCard from '../components/ProductCard';
import { Link } from 'react-router-dom';
import { Heart, ArrowRight } from 'lucide-react';

const Wishlist = () => {
  const { wishlistItems } = useContext(WishlistContext);

  if (wishlistItems.length === 0) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-24 text-center">
        <div className="bg-red-50 rounded-full w-24 h-24 flex items-center justify-center mx-auto mb-6">
           <Heart size={48} className="text-red-300" />
        </div>
        <h2 className="text-3xl font-extrabold text-gray-900 mb-4">Your Wishlist is Empty</h2>
        <p className="text-gray-500 mb-8 max-w-md mx-auto">Save items you love to your wishlist so you can easily find them later. Start exploring now!</p>
        <Link to="/" className="inline-flex items-center bg-indigo-600 border border-transparent rounded-full shadow-md py-3 px-8 text-base font-medium text-white hover:bg-indigo-700 transition">
          Discover Products <ArrowRight size={18} className="ml-2" />
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="flex items-center justify-between mb-8 pb-4 border-b border-gray-200">
        <h1 className="text-3xl font-extrabold text-gray-900 flex items-center">
            <Heart size={28} className="text-red-500 mr-3" fill="currentColor" />
            My Wishlist
        </h1>
        <span className="text-gray-500 font-medium bg-gray-100 px-4 py-1 rounded-full">{wishlistItems.length} Items</span>
      </div>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {wishlistItems.map((item) => (
          <ProductCard key={item.Product_ID} product={item} />
        ))}
      </div>
    </div>
  );
};

export default Wishlist;
