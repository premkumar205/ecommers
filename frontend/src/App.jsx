import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import ProductDetail from './pages/ProductDetail';
import SearchResults from './pages/SearchResults';
import LoginPage from './pages/LoginPage';
import Cart from './pages/Cart';
import Wishlist from './pages/Wishlist';
import CartProvider from './context/CartContext';
import WishlistProvider from './context/WishlistContext';
import { Toaster } from 'react-hot-toast';

function App() {
  return (
    <CartProvider>
      <WishlistProvider>
        <BrowserRouter>
          <div className="min-h-screen bg-white">
            <Toaster position="bottom-center" toastOptions={{duration: 3000, style: { background: '#333', color: '#fff' }}} />
            <Navbar />
            <main>
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/product/:id" element={<ProductDetail />} />
                <Route path="/search" element={<SearchResults />} />
                <Route path="/cart" element={<Cart />} />
                <Route path="/wishlist" element={<Wishlist />} />
                <Route path="/login" element={<LoginPage />} />
              </Routes>
            </main>
            
            <footer className="bg-gray-900 text-gray-300 py-12 text-center mt-auto">
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                  <p className="text-gray-400 font-medium">© {new Date().getFullYear()} AI-Shop. Powered by Machine Learning Recommendations.</p>
              </div>
            </footer>
          </div>
        </BrowserRouter>
      </WishlistProvider>
    </CartProvider>
  );
}

export default App;
