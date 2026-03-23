import React, { useState, useEffect } from 'react';
import ProductCard from '../components/ProductCard';
import { fetchFeaturedProducts, fetchTopRatedProducts, fetchProductsByCategory } from '../services/api';

const Home = () => {
  const [featured, setFeatured] = useState([]);
  const [topRated, setTopRated] = useState([]);
  const [electronics, setElectronics] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {
        const [featRes, topRes, elRes] = await Promise.all([
          fetchFeaturedProducts(),
          fetchTopRatedProducts(),
          fetchProductsByCategory('Electronics') // Example category
        ]);
        
        setFeatured(featRes.products || []);
        setTopRated(topRes.products || []);
        setElectronics(elRes.products || []);
      } catch (err) {
        console.error("Error loading home page data", err);
      } finally {
        setLoading(false);
      }
    };
    
    loadData();
  }, []);

  const renderSection = (title, items) => (
    <div className="my-12">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900 border-b-2 border-indigo-600 pb-2 inline-block">
          {title}
        </h2>
        <a href="#" className="text-indigo-600 hover:text-indigo-800 font-medium text-sm flex items-center">
          View All
          <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" /></svg>
        </a>
      </div>
      
      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {[1, 2, 3, 4].map(i => (
            <div key={i} className="bg-white rounded-xl shadow-sm border border-gray-100 h-96 animate-pulse flex flex-col">
              <div className="bg-gray-200 h-64 w-full rounded-t-xl"></div>
              <div className="p-4 flex-1 flex flex-col justify-between">
                <div>
                  <div className="h-4 bg-gray-200 rounded w-1/4 mb-2"></div>
                  <div className="h-6 bg-gray-200 rounded w-full mb-3"></div>
                </div>
                <div className="h-8 bg-gray-200 rounded w-1/3"></div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {items.slice(0, 4).map(product => (
            <ProductCard key={product.Product_ID} product={product} />
          ))}
        </div>
      )}
    </div>
  );

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      
      {/* Hero Banner Placeholder */}
      <div className="relative rounded-2xl overflow-hidden mb-12 bg-gradient-to-r from-gray-900 to-indigo-900 h-80 flex items-center shadow-lg">
        <div className="absolute inset-0 bg-black opacity-40"></div>
        <div className="relative z-10 px-8 md:px-16 max-w-2xl">
          <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-4 leading-tight">
            Discover Your Next Favorite Product
          </h1>
          <p className="text-lg text-gray-200 mb-8 font-medium">
            AI-powered recommendations tailored just for you. Shop the best deals and top brands today.
          </p>
          <a href="#featured" className="bg-white text-gray-900 font-bold py-3 px-8 rounded-full hover:bg-indigo-50 transition-colors shadow-md transform hover:-translate-y-1 inline-block">
            Shop Now
          </a>
        </div>
        <div className="absolute right-0 bottom-0 hidden lg:block opacity-50 pointer-events-none">
            {/* Abstract geometric shape mimicking a shopping bag or gift */}
            <svg width="400" height="400" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
              <path fill="#4F46E5" d="M47.7,-57.2C59.4,-44.6,64.9,-27.2,68.4,-9.1C72,9.1,73.5,28,64.6,41.9C55.7,55.8,36.5,64.7,16.5,69.5C-3.4,74.2,-24.1,74.7,-41.6,66.1C-59.2,57.5,-73.6,39.9,-77.8,20.2C-82.1,0.5,-76.3,-21.3,-64,-37.7C-51.7,-54.2,-33.1,-65.2,-15.5,-69.1C2.1,-73,20,-70,36,-57.2Z" transform="translate(100 100) scale(1.1)" />
            </svg>
        </div>
      </div>

      <div id="featured">
        {renderSection("Featured Products", featured)}
      </div>

      <div className="rounded-2xl overflow-hidden my-16 bg-indigo-50 border border-indigo-100 p-8 md:p-12 flex flex-col md:flex-row items-center justify-between shadow-inner">
        <div className="mb-6 md:mb-0 md:mr-8 text-center md:text-left">
          <h3 className="text-3xl font-extrabold text-indigo-900 mb-3">AI Personalization Engine</h3>
          <p className="text-indigo-700 text-lg max-w-md">Our advanced machine learning models analyze descriptions, tags, and ratings to find products you'll truly love.</p>
        </div>
        <div className="flex gap-4">
           <div className="bg-white p-4 rounded-xl shadow-sm border border-indigo-100 text-center w-32">
             <span className="block text-3xl font-black text-indigo-600 mb-1">98%</span>
             <span className="text-xs font-semibold text-gray-500 uppercase tracking-widest">Match Rate</span>
           </div>
           <div className="bg-white p-4 rounded-xl shadow-sm border border-indigo-100 text-center w-32">
             <span className="block text-3xl font-black text-indigo-600 mb-1">Fast</span>
             <span className="text-xs font-semibold text-gray-500 uppercase tracking-widest">Real-time</span>
           </div>
        </div>
      </div>

      {renderSection("Top Rated", topRated)}
      
      {renderSection("Electronics & Gadgets", electronics)}

    </div>
  );
};

export default Home;
