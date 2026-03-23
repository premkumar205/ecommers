import React, { useState, useEffect, useRef, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ShoppingCart, Heart, Search, Menu, X } from 'lucide-react';
import { CartContext } from '../context/CartContext';
import { WishlistContext } from '../context/WishlistContext';
import { searchProducts } from '../services/api';

const Navbar = () => {
  const navigate = useNavigate();
  const { cartItems } = useContext(CartContext);
  const { wishlistItems } = useContext(WishlistContext);
  const [searchQuery, setSearchQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const searchRef = useRef(null);

  const cartCount = cartItems.reduce((acc, item) => acc + item.quantity, 0);
  const wishlistCount = wishlistItems.length;

  useEffect(() => {
    const fetchSuggestions = async () => {
      if (searchQuery.length > 1) {
        try {
          const data = await searchProducts(searchQuery);
          setSuggestions(data.products.slice(0, 5));
          setShowSuggestions(true);
        } catch (error) {
          console.error("Search error", error);
        }
      } else {
        setSuggestions([]);
        setShowSuggestions(false);
      }
    };
    
    // Debounce
    const timeoutId = setTimeout(fetchSuggestions, 300);
    return () => clearTimeout(timeoutId);
  }, [searchQuery]);

  // Handle outside click to close suggestions
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setShowSuggestions(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [searchRef]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      setShowSuggestions(false);
      navigate(`/search?q=${encodeURIComponent(searchQuery)}`);
    }
  };

  return (
    <nav className="bg-gray-900 text-white sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo */}
          <div className="flex-shrink-0 flex items-center">
            <Link to="/" className="text-2xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-cyan-400">
              AI-Shop
            </Link>
          </div>

          {/* Search Bar - Desktop */}
          <div className="hidden md:block flex-1 max-w-2xl mx-8">
            <div className="relative" ref={searchRef}>
              <form onSubmit={handleSearchSubmit} className="relative">
                <input
                  type="text"
                  className="w-full bg-white text-gray-900 rounded-l-md rounded-r-none py-2 px-4 pl-4 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  placeholder="Search products, categories, brands..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onFocus={() => { if(searchQuery.length > 1) setShowSuggestions(true); }}
                />
                <button 
                  type="submit" 
                  className="absolute right-0 top-0 bottom-0 bg-indigo-500 hover:bg-indigo-600 px-4 rounded-r-md flex items-center transition-colors"
                >
                  <Search size={20} className="text-white" />
                </button>
              </form>

              {/* Search Suggestions */}
              {showSuggestions && suggestions.length > 0 && (
                <div className="absolute top-full left-0 right-12 mt-1 bg-white rounded-md shadow-lg overflow-hidden z-50 text-gray-900 border border-gray-200">
                  <ul className="py-1">
                    {suggestions.map((p) => (
                      <li key={p.Product_ID}>
                        <Link 
                          to={`/product/${p.Product_ID}`}
                          className="block px-4 py-2 hover:bg-gray-100 text-sm flex items-center"
                          onClick={() => setShowSuggestions(false)}
                        >
                          <img src={p.image_url || 'https://via.placeholder.com/40'} alt="" className="w-8 h-8 object-cover rounded mr-3" />
                          <div className="truncate">
                            <span className="font-semibold block truncate leading-tight">{p.Product_Name}</span>
                            <span className="text-xs text-gray-500">{(p.Category || "Products").split('>')[0]}</span>
                          </div>
                        </Link>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>

          {/* Icons Menu - Desktop */}
          <div className="hidden md:flex items-center space-x-6">
            <Link to="/wishlist" className="relative hover:text-indigo-400 transition-colors flex flex-col items-center">
              <Heart size={24} />
              <span className="text-[10px] mt-1">Wishlist</span>
              {wishlistCount > 0 && (
                <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center">
                  {wishlistCount}
                </span>
              )}
            </Link>
            
            <Link to="/cart" className="relative hover:text-indigo-400 transition-colors flex flex-col items-center cursor-pointer">
              <ShoppingCart size={24} />
              <span className="text-[10px] mt-1">Cart</span>
              {cartCount > 0 && (
                <span className="absolute -top-2 -right-2 bg-indigo-500 text-white text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center">
                  {cartCount}
                </span>
              )}
            </Link>
            
            <div className="flex items-center pl-6 border-l border-gray-700 h-8">
              <div className="flex items-center bg-gray-800/50 rounded-lg border border-gray-700 p-1 shadow-inner">
                <button 
                  onClick={() => navigate('/login')} 
                  className="text-sm font-medium px-4 py-1.5 hover:text-indigo-400 hover:bg-gray-700/50 rounded-md transition-all ease-in-out duration-200"
                >
                  Login
                </button>
                <div className="w-px h-4 bg-gray-700 mx-1"></div>
                <button 
                  onClick={() => navigate('/login')} 
                  className="text-sm font-medium bg-indigo-600 hover:bg-indigo-500 px-4 py-1.5 rounded-md transition-all ease-in-out duration-200 shadow-sm text-white"
                >
                  Register
                </button>
              </div>
            </div>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
             <button onClick={() => setIsMenuOpen(!isMenuOpen)} className="text-gray-300 hover:text-white focus:outline-none">
               {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
             </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Content */}
      {isMenuOpen && (
        <div className="md:hidden bg-gray-800 pb-4 px-4">
           {/* Mobile Search */}
           <div className="pt-2 pb-4">
               <form onSubmit={handleSearchSubmit} className="relative flex">
                 <input
                   type="text"
                   className="w-full bg-white text-gray-900 rounded-l-md py-2 px-3 focus:outline-none"
                   placeholder="Search..."
                   value={searchQuery}
                   onChange={(e) => setSearchQuery(e.target.value)}
                 />
                 <button type="submit" className="bg-indigo-500 px-4 rounded-r-md">
                   <Search size={20} className="text-white" />
                 </button>
               </form>
               {suggestions.length > 0 && searchQuery.length > 1 && (
                  <div className="mt-1 bg-white rounded-md shadow text-gray-900">
                    <ul className="py-1">
                      {suggestions.map((p) => (
                        <li key={p.Product_ID}>
                          <Link 
                            to={`/product/${p.Product_ID}`}
                            className="block px-4 py-2 hover:bg-gray-100 text-sm truncate"
                            onClick={() => setIsMenuOpen(false)}
                          >
                            {p.Product_Name}
                          </Link>
                        </li>
                      ))}
                    </ul>
                  </div>
               )}
           </div>
           
           <div className="flex justify-around border-t border-gray-700 pt-4 pb-4">
              <Link to="/wishlist" onClick={() => setIsMenuOpen(false)} className="flex flex-col items-center relative hover:text-indigo-400">
                 <Heart size={24} />
                 <span className="text-xs mt-1">Wishlist ({wishlistCount})</span>
              </Link>
              <Link to="/cart" className="flex flex-col items-center relative hover:text-indigo-400 cursor-pointer" onClick={() => setIsMenuOpen(false)}>
                 <ShoppingCart size={24} />
                 <span className="text-xs mt-1">Cart ({cartCount})</span>
              </Link>
           </div>
           <div className="flex justify-center border-t border-gray-700 pt-4">
              <div className="flex items-center bg-gray-900 rounded-xl border border-gray-700 p-1 w-full max-w-xs shadow-lg">
                <button 
                  onClick={() => { navigate('/login'); setIsMenuOpen(false); }} 
                  className="flex-1 text-sm font-medium py-2 px-4 hover:bg-gray-800 rounded-lg transition-colors text-white text-center"
                >
                  Login
                </button>
                <div className="w-px h-6 bg-gray-700 mx-1"></div>
                <button 
                  onClick={() => { navigate('/login'); setIsMenuOpen(false); }} 
                  className="flex-1 text-sm font-medium py-2 px-4 bg-indigo-600 hover:bg-indigo-500 rounded-lg shadow-md text-white text-center transition-all"
                >
                  Register
                </button>
              </div>
           </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
