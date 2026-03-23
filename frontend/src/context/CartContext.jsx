import React, { createContext, useState, useEffect, useContext } from 'react';

export const CartContext = createContext();

export default function CartProvider({ children }) {
  const [cartItems, setCartItems] = useState(() => {
    try {
      const stored = localStorage.getItem('cartItems');
      return stored ? JSON.parse(stored) : [];
    } catch (error) {
      console.error("Error parsing cartItems from localStorage", error);
      return [];
    }
  });

  useEffect(() => {
    localStorage.setItem('cartItems', JSON.stringify(cartItems));
  }, [cartItems]);

  const addToCart = (product) => {
    setCartItems((prev) => {
      const existing = prev.find(item => item.Product_ID === product.Product_ID);
      if (existing) {
        return prev.map(item => item.Product_ID === product.Product_ID 
          ? { ...item, quantity: item.quantity + 1 } 
          : item);
      }
      return [...prev, { ...product, quantity: 1 }];
    });
  };

  const removeFromCart = (productId) => {
    setCartItems((prev) => prev.filter(item => item.Product_ID !== productId));
  };

  const updateQuantity = (productId, amount) => {
    setCartItems((prev) => prev.map(item => {
      if (item.Product_ID === productId) {
        const newQuantity = item.quantity + amount;
        return { ...item, quantity: newQuantity > 0 ? newQuantity : 1 };
      }
      return item;
    }));
  };

  const cartTotal = cartItems.reduce((total, item) => {
    const priceStr = String(item.Price || "0").replace(/[^0-9.]/g, '');
    const price = parseFloat(priceStr) || 0;
    return total + (price * item.quantity);
  }, 0);

  return (
    <CartContext.Provider value={{ cartItems, addToCart, removeFromCart, updateQuantity, cartTotal }}>
      {children}
    </CartContext.Provider>
  );
};
