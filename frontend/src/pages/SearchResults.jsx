import React, { useState, useEffect } from 'react';
import { useLocation, Link } from 'react-router-dom';
import ProductCard from '../components/ProductCard';
import { searchProducts } from '../services/api';

const SearchResults = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const location = useLocation();
  const query = new URLSearchParams(location.search).get('q');

  useEffect(() => {
    const fetchResults = async () => {
      if (!query) {
        setLoading(false);
        return;
      }
      setLoading(true);
      try {
        const data = await searchProducts(query);
        setProducts(data.products || []);
      } catch (error) {
        console.error("Search results error", error);
        setProducts([]);
      } finally {
        setLoading(false);
      }
    };
    fetchResults();
  }, [query]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 min-h-screen">
      <div className="flex items-center gap-2 text-sm text-gray-500 mb-6">
        <Link to="/" className="hover:text-indigo-600">Home</Link>
        <span>/</span>
        <span className="text-gray-900 font-medium">Search</span>
      </div>

      <div className="flex justify-between items-end mb-8">
        <div>
           <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">
             Search Results
           </h1>
           <p className="text-gray-500 mt-1">
             {products.length} {products.length === 1 ? 'result' : 'results'} found for <span className="text-indigo-600 font-bold">"{query}"</span>
           </p>
        </div>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {[1, 2, 3, 4, 5, 6, 7, 8].map(i => (
             <div key={i} className="bg-white rounded-2xl shadow-sm border border-gray-100 h-[400px] animate-pulse flex flex-col">
               <div className="bg-gray-100 h-64 w-full rounded-t-2xl"></div>
               <div className="p-5 flex-1 flex flex-col justify-between">
                 <div className="space-y-3">
                   <div className="h-4 bg-gray-100 rounded w-1/4"></div>
                   <div className="h-6 bg-gray-100 rounded w-full"></div>
                 </div>
                 <div className="h-8 bg-gray-100 rounded w-1/2 mt-4"></div>
               </div>
             </div>
          ))}
        </div>
      ) : products.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {products.map(product => (
            <ProductCard key={product.Product_ID} product={product} />
          ))}
        </div>
      ) : (
        <div className="text-center py-24 bg-white rounded-3xl border-2 border-dashed border-gray-100 shadow-sm">
           <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-50 text-gray-400 mb-4">
             <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
           </div>
           <p className="text-xl text-gray-600 font-bold mb-2">No matching products found</p>
           <p className="text-gray-400 max-w-xs mx-auto mb-8">We couldn't find anything matching your search. Try checking your spelling or using more general terms.</p>
           <Link 
             to="/"
             className="inline-flex items-center px-6 py-3 border border-transparent text-base font-bold rounded-full shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all transform hover:scale-105"
           >
             Continue Shopping
           </Link>
        </div>
      )}
    </div>
  );
};

export default SearchResults;
