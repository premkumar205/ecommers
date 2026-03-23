import React, { useContext } from 'react';
import { CartContext } from '../context/CartContext';
import { Link } from 'react-router-dom';
import { Trash2, ShoppingBag, ArrowRight } from 'lucide-react';

const Cart = () => {
  const { cartItems, removeFromCart, updateQuantity, cartTotal } = useContext(CartContext);

  if (cartItems.length === 0) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-24 text-center">
        <div className="bg-gray-50 rounded-full w-24 h-24 flex items-center justify-center mx-auto mb-6">
           <ShoppingBag size={48} className="text-indigo-200" />
        </div>
        <h2 className="text-3xl font-extrabold text-gray-900 mb-4">Your Cart is Empty</h2>
        <p className="text-gray-500 mb-8 max-w-md mx-auto">Looks like you haven't added anything to your cart yet. Explore our top recommendations.</p>
        <Link to="/" className="inline-flex items-center bg-indigo-600 border border-transparent rounded-full shadow-md py-3 px-8 text-base font-medium text-white hover:bg-indigo-700 transition">
          Continue Shopping <ArrowRight size={18} className="ml-2" />
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 className="text-3xl font-extrabold text-gray-900 mb-8 border-b border-gray-200 pb-4">Shopping Cart ({cartItems.length} items)</h1>
      
      <div className="flex flex-col lg:flex-row gap-8">
        {/* Cart Items */}
        <div className="flex-1 space-y-6">
          {cartItems.map((item) => (
            <div key={item.Product_ID} className="flex flex-col sm:flex-row bg-white border border-gray-100 rounded-2xl shadow-sm p-4 hover:shadow-md transition gap-6 items-center">
              <div className="w-full sm:w-40 h-40 bg-gray-50 rounded-xl overflow-hidden flex-shrink-0">
                  <img 
                    src={item.image_url || `https://via.placeholder.com/200?text=${item.Product_Name}`} 
                    alt={item.Product_Name} 
                    className="w-full h-full object-contain"
                  />
              </div>
              <div className="flex-1 w-full text-center sm:text-left">
                <Link to={`/product/${item.Product_ID}`} className="text-lg font-bold text-gray-900 hover:text-indigo-600 block line-clamp-2 mb-2 leading-tight">
                  {item.Product_Name}
                </Link>
                <div className="text-sm font-semibold text-gray-500 mb-4 bg-gray-100 inline-block px-3 py-1 rounded-full">{item.Brand}</div>
                
                <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
                  <div className="flex items-center border border-gray-200 rounded-lg p-1 bg-gray-50">
                    <button 
                      onClick={() => updateQuantity(item.Product_ID, -1)}
                      className="px-4 py-1.5 text-gray-500 hover:text-black hover:bg-white rounded font-bold shadow-sm transition"
                    >
                      -
                    </button>
                    <span className="px-6 py-1 border-x border-gray-200 font-bold bg-white mx-1 rounded">{item.quantity}</span>
                    <button 
                      onClick={() => updateQuantity(item.Product_ID, 1)}
                      className="px-4 py-1.5 text-gray-500 hover:text-black hover:bg-white rounded font-bold shadow-sm transition"
                    >
                      +
                    </button>
                  </div>
                  
                  <div className="text-2xl font-black text-gray-900">
                    {/* Simplified calculation format, parse original string */}
                    {(parseFloat(String(item.Price || "0").replace(/[^0-9.]/g, '')) * item.quantity).toFixed(2)}
                  </div>
                </div>
              </div>
              
              <button 
                onClick={() => removeFromCart(item.Product_ID)}
                className="text-red-400 hover:text-red-500 p-3 hover:bg-red-50 rounded-full transition w-full sm:w-auto flex justify-center mt-2 sm:mt-0"
                title="Remove Item"
              >
                <Trash2 size={24} />
              </button>
            </div>
          ))}
        </div>

        {/* Order Summary */}
        <div className="w-full lg:w-96">
          <div className="bg-gray-50 rounded-2xl p-6 border border-gray-100 sticky top-24 shadow-sm">
            <h2 className="text-xl font-extrabold text-gray-900 mb-6 pb-4 border-b border-gray-200">Order Summary</h2>
            
            <div className="space-y-4 mb-6 text-gray-600">
              <div className="flex justify-between font-medium">
                <span>Subtotal</span>
                <span className="text-gray-900 font-bold">₹{cartTotal.toFixed(2)}</span>
              </div>
              <div className="flex justify-between font-medium">
                <span>Shipping Estimate</span>
                <span className="text-green-600 font-bold">FREE</span>
              </div>
              <div className="flex justify-between font-medium">
                <span>Tax Estimate</span>
                <span className="text-gray-900 font-bold">₹0.00</span>
              </div>
            </div>
            
            <div className="flex justify-between font-black text-2xl text-gray-900 border-t border-gray-200 pt-6 mb-8">
              <span>Order Total</span>
              <span>₹{cartTotal.toFixed(2)}</span>
            </div>
            
            <button className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-4 rounded-xl shadow-lg transition text-lg flex justify-center items-center">
              Proceed to Checkout <ArrowRight size={20} className="ml-2" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Cart;
