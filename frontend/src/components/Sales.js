import React, { useState, useEffect } from 'react';
import { FaArrowLeft, FaSearch, FaShoppingCart, FaPlus, FaMinus, FaTimes } from 'react-icons/fa';
import { itemAPI, transactionAPI } from '../services/api';
import './Sales.css';

const Sales = ({ employee, onBack }) => {
  const [items, setItems] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [cart, setCart] = useState([]);
  const [couponCode, setCouponCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const loadItems = async () => {
    try {
      const response = await itemAPI.list(searchTerm);
      setItems(response.data);
    } catch (error) {
      console.error('Error loading items:', error);
    }
  };

  useEffect(() => {
    loadItems();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      if (searchTerm !== '') {
        loadItems();
      }
    }, 300);
    return () => clearTimeout(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchTerm]);

  const addToCart = (item) => {
    if (item.quantity <= 0) {
      setMessage({ type: 'error', text: 'Item out of stock' });
      return;
    }

    const existingItem = cart.find(cartItem => cartItem.id === item.id);
    if (existingItem) {
      if (existingItem.quantity >= item.quantity) {
        setMessage({ type: 'error', text: 'Not enough stock available' });
        return;
      }
      setCart(cart.map(cartItem =>
        cartItem.id === item.id
          ? { ...cartItem, quantity: cartItem.quantity + 1 }
          : cartItem
      ));
    } else {
      setCart([...cart, { ...item, quantity: 1 }]);
    }
    setMessage({ type: 'success', text: `${item.name} added to cart` });
    setTimeout(() => setMessage(''), 3000);
  };

  const removeFromCart = (itemId) => {
    setCart(cart.filter(item => item.id !== itemId));
  };

  const updateQuantity = (itemId, quantity) => {
    if (quantity <= 0) {
      removeFromCart(itemId);
      return;
    }
    const item = items.find(i => i.id === itemId);
    if (item && quantity > item.quantity) {
      setMessage({ type: 'error', text: 'Not enough stock available' });
      return;
    }
    setCart(cart.map(item =>
      item.id === itemId ? { ...item, quantity } : item
    ));
  };

  const calculateSubtotal = () => {
    return cart.reduce((sum, item) => sum + (parseFloat(item.price) * item.quantity), 0);
  };

  const calculateTotal = () => {
    const subtotal = calculateSubtotal();
    const tax = subtotal * 0.06; // 6% tax
    return subtotal + tax;
  };

  const handleCheckout = async () => {
    if (cart.length === 0) {
      setMessage({ type: 'error', text: 'Cart is empty' });
      return;
    }

    setLoading(true);
    try {
      await transactionAPI.createSale(
        cart,
        couponCode || null
      );
      setMessage({ type: 'success', text: 'Sale completed successfully!' });
      setCart([]);
      setCouponCode('');
      loadItems(); // Refresh inventory
      setTimeout(() => {
        setMessage('');
        onBack();
      }, 2000);
    } catch (error) {
      setMessage({
        type: 'error',
        text: error.response?.data?.error || 'Failed to complete sale'
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="sales-container">
      <div className="sales-header">
        <button className="btn btn-secondary" onClick={onBack}>
          <FaArrowLeft /> Back
        </button>
        <h1>Sales Transaction</h1>
        <div className="user-info">
          <span className="user-badge">{employee.full_name}</span>
        </div>
      </div>

      {message && (
        <div className={`alert alert-${message.type}`}>
          <span>{message.type === 'success' ? '✓' : '⚠️'}</span>
          <span>{message.text}</span>
        </div>
      )}

      <div className="sales-grid">
        <div className="sales-left">
          <div className="card">
            <h2 className="card-title">Search Items</h2>
            <div className="search-bar">
              <FaSearch className="search-icon" />
              <input
                type="text"
                className="form-input"
                placeholder="Search by name or ID..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                style={{ marginBottom: '1rem' }}
              />
            </div>
            
            <div className="items-grid">
              {items.map(item => (
                <div
                  key={item.id}
                  className="item-card"
                  onClick={() => addToCart(item)}
                >
                  <div className="item-header">
                    <span className="item-id">#{item.legacy_item_id}</span>
                    <span className={`stock-badge ${item.quantity > 0 ? 'in-stock' : 'out-of-stock'}`}>
                      {item.quantity > 0 ? `${item.quantity} in stock` : 'Out of stock'}
                    </span>
                  </div>
                  <h3 className="item-name">{item.name}</h3>
                  <div className="item-price">${parseFloat(item.price).toFixed(2)}</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="sales-right">
          <div className="card">
            <h2 className="card-title">Shopping Cart</h2>
            
            {cart.length === 0 ? (
              <div className="empty-state">
                <FaShoppingCart className="empty-state-icon" />
                <p className="empty-state-text">Cart is empty</p>
                <p style={{ color: '#a0aec0', fontSize: '0.9rem' }}>Add items from the left to get started</p>
              </div>
            ) : (
              <>
                <div className="cart-items">
                  {cart.map(item => (
                    <div key={item.id} className="cart-item">
                      <div className="cart-item-info">
                        <div className="cart-item-name">{item.name}</div>
                        <div className="cart-item-details">
                          ${parseFloat(item.price).toFixed(2)} × {item.quantity}
                        </div>
                      </div>
                      <div className="cart-item-controls">
                        <button
                          className="btn-quantity"
                          onClick={() => updateQuantity(item.id, item.quantity - 1)}
                        >
                          <FaMinus />
                        </button>
                        <span className="cart-quantity">{item.quantity}</span>
                        <button
                          className="btn-quantity"
                          onClick={() => updateQuantity(item.id, item.quantity + 1)}
                          disabled={item.quantity >= items.find(i => i.id === item.id)?.quantity}
                        >
                          <FaPlus />
                        </button>
                        <button
                          className="btn-remove"
                          onClick={() => removeFromCart(item.id)}
                        >
                          <FaTimes />
                        </button>
                      </div>
                      <div className="cart-item-price">
                        ${(parseFloat(item.price) * item.quantity).toFixed(2)}
                      </div>
                    </div>
                  ))}
                </div>

                <div className="coupon-section">
                  <input
                    type="text"
                    className="form-input"
                    placeholder="Enter coupon code (optional)"
                    value={couponCode}
                    onChange={(e) => setCouponCode(e.target.value)}
                  />
                </div>

                <div className="total-section">
                  <div className="total-row">
                    <span>Subtotal:</span>
                    <span>${calculateSubtotal().toFixed(2)}</span>
                  </div>
                  <div className="total-row">
                    <span>Tax (6%):</span>
                    <span>${(calculateSubtotal() * 0.06).toFixed(2)}</span>
                  </div>
                  <div className="total-row total-final">
                    <span>Total:</span>
                    <span>${calculateTotal().toFixed(2)}</span>
                  </div>
                </div>

                <button
                  className="btn btn-primary"
                  style={{ width: '100%', marginTop: '1.5rem', padding: '1rem', fontSize: '1.1rem' }}
                  onClick={handleCheckout}
                  disabled={loading}
                >
                  {loading ? 'Processing...' : 'Complete Sale'}
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sales;

