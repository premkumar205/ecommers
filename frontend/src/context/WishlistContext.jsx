import React, { createContext, useState, useEffect, useContext } from 'react';

export const WishlistContext = createContext();

export default function WishlistProvider({ children }) {
  const [wishlistItems, setWishlistItems] = useState(() => {
    try {
      const stored = localStorage.getItem('wishlistItems');
      return stored ? JSON.parse(stored) : [];
    } catch (error) {
      console.error("Error parsing wishlistItems from localStorage", error);
      return [];
    }
  });

  useEffect(() => {
    localStorage.setItem('wishlistItems', JSON.stringify(wishlistItems));
  }, [wishlistItems]);

  const toggleWishlist = (product) => {
    setWishlistItems((prev) => {
      const exists = prev.find(item => item.Product_ID === product.Product_ID);
      if (exists) {
        return prev.filter(item => item.Product_ID !== product.Product_ID);
      }
      return [...prev, product];
    });
  };

  const isInWishlist = (productId) => {
    return wishlistItems.some(item => item.Product_ID === productId);
  };

  return (
    <WishlistContext.Provider value={{ wishlistItems, toggleWishlist, isInWishlist }}>
      {children}
    </WishlistContext.Provider>
  );
};
