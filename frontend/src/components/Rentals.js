import React, { useState, useEffect } from 'react';
import { FaArrowLeft, FaBox, FaTimes, FaPlus, FaMinus } from 'react-icons/fa';
import { itemAPI, transactionAPI } from '../services/api';
import './Rentals.css';

const Rentals = ({ employee, onBack }) => {
  const [items, setItems] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [cart, setCart] = useState([]);
  const [customerPhone, setCustomerPhone] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  // Debug: Log employee info
  useEffect(() => {
    console.log('Rentals component mounted/updated:', { 
      employee, 
      hasEmployee: !!employee,
      employeeId: employee?.id,
      employeePosition: employee?.position 
    });
  }, [employee]);

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
      setCart(cart.map(cartItem =>
        cartItem.id === item.id
          ? { ...cartItem, quantity: cartItem.quantity + 1 }
          : cartItem
      ));
    } else {
      setCart([...cart, { ...item, quantity: 1 }]);
    }
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

  const handleCheckout = async (e) => {
    // Prevent default form submission if any
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }
    
    console.log('=== handleCheckout STARTED ===', { 
      customerPhone, 
      cartLength: cart.length, 
      employee,
      cart: cart.map(item => ({ id: item.id, name: item.name, quantity: item.quantity }))
    });
    
    // Validate customer phone number
    const phoneRegex = /^\d{10,15}$/;
    if (!customerPhone || !phoneRegex.test(customerPhone)) {
      setMessage({ type: 'error', text: 'Please enter a valid phone number (10-15 digits)' });
      return;
    }
    
    // Validate cart is not empty
    if (cart.length === 0) {
      setMessage({ type: 'error', text: 'Cart is empty. Please add items to the cart.' });
      return;
    }

    // Validate all items have sufficient stock
    for (const cartItem of cart) {
      const item = items.find(i => i.id === cartItem.id);
      if (!item) {
        setMessage({ type: 'error', text: `Item ${cartItem.name} not found in inventory` });
        return;
      }
      if (item.quantity < cartItem.quantity) {
        setMessage({ 
          type: 'error', 
          text: `Insufficient stock for ${cartItem.name}. Available: ${item.quantity}, Requested: ${cartItem.quantity}` 
        });
        return;
      }
    }

    setLoading(true);
    setMessage(''); // Clear previous messages
    
    console.log('Sending rental request:', {
      customer_phone: customerPhone,
      items: cart.map(item => ({ item_id: item.id, quantity: item.quantity }))
    });
    
    try {
      const response = await transactionAPI.createRental(customerPhone, cart);
      console.log('Rental response:', response);
      setMessage({ type: 'success', text: 'Rental completed successfully!' });
      setCart([]);
      setCustomerPhone('');
      loadItems(); // Refresh inventory
      
      setTimeout(() => {
        setMessage('');
        onBack();
      }, 2000);
    } catch (error) {
      console.error('Rental error details:', {
        error,
        response: error.response,
        status: error.response?.status,
        data: error.response?.data,
        message: error.message
      });
      
      let errorMessage = 'Failed to complete rental. Please try again.';
      
      if (error.response) {
        // Server responded with error
        if (error.response.status === 401) {
          errorMessage = 'Session expired. Please log in again.';
        } else if (error.response.status === 403) {
          errorMessage = 'You do not have permission to perform this action.';
        } else if (error.response.data) {
          errorMessage = error.response.data.error || 
                        error.response.data.detail || 
                        JSON.stringify(error.response.data);
        }
      } else if (error.request) {
        // Request made but no response
        errorMessage = 'Network error. Please check your connection and ensure the backend server is running.';
      } else {
        // Error in request setup
        errorMessage = error.message || 'An unexpected error occurred.';
      }
      
      setMessage({
        type: 'error',
        text: errorMessage
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
        <h1>Rental Transaction</h1>
        <div className="user-info">
          <span className="user-badge">{employee?.full_name || employee?.first_name || 'User'}</span>
        </div>
      </div>

      {message && (
        <div className={`alert alert-${message.type}`}>
          <span>{message.type === 'success' ? '✓' : '⚠️'}</span>
          <span>{message.text}</span>
        </div>
      )}

      {/* Debug info - remove in production */}
      {process.env.NODE_ENV === 'development' && (
        <div style={{ 
          position: 'fixed', 
          bottom: '10px', 
          right: '10px', 
          background: 'rgba(0,0,0,0.8)', 
          color: 'white', 
          padding: '10px', 
          borderRadius: '5px',
          fontSize: '12px',
          zIndex: 9999,
          maxWidth: '300px'
        }}>
          <div><strong>Debug Info:</strong></div>
          <div>Phone: {customerPhone || 'empty'} ({customerPhone?.length || 0} chars)</div>
          <div>Cart: {cart.length} items</div>
          <div>Loading: {loading ? 'YES' : 'NO'}</div>
          <div>Button Disabled: {(loading || !customerPhone || cart.length === 0) ? 'YES' : 'NO'}</div>
          <div>Phone Valid: {customerPhone && /^\d{10,15}$/.test(customerPhone) ? 'YES' : 'NO'}</div>
        </div>
      )}

      <div className="sales-grid">
        <div className="sales-left">
          <div className="card">
            <h2 className="card-title">Customer Information</h2>
            <div className="form-group">
              <label className="form-label">
                Customer Phone Number 
                <span style={{ color: '#e53e3e', marginLeft: '0.5rem' }}>*</span>
                {customerPhone && (
                  <span style={{ 
                    color: /^\d{10,15}$/.test(customerPhone) ? '#48bb78' : '#e53e3e',
                    marginLeft: '0.5rem',
                    fontSize: '0.85rem'
                  }}>
                    ({customerPhone.length} digits - {/^\d{10,15}$/.test(customerPhone) ? 'Valid' : 'Need 10-15 digits'})
                  </span>
                )}
              </label>
              <input
                type="tel"
                className="form-input"
                placeholder="Enter customer phone number (10-15 digits)"
                value={customerPhone}
                onChange={(e) => {
                  const digitsOnly = e.target.value.replace(/\D/g, '');
                  console.log('Phone input changed:', { original: e.target.value, digitsOnly, length: digitsOnly.length });
                  setCustomerPhone(digitsOnly);
                }}
                onBlur={() => {
                  if (customerPhone && customerPhone.length < 10) {
                    setMessage({ 
                      type: 'error', 
                      text: `Phone number must be at least 10 digits. You entered ${customerPhone.length} digits.` 
                    });
                  }
                }}
                style={{
                  borderColor: customerPhone && !/^\d{10,15}$/.test(customerPhone) ? '#e53e3e' : undefined
                }}
              />
              {customerPhone && customerPhone.length > 0 && customerPhone.length < 10 && (
                <div style={{ color: '#e53e3e', fontSize: '0.85rem', marginTop: '0.25rem' }}>
                  Phone number must be at least 10 digits (currently {customerPhone.length})
                </div>
              )}
            </div>
          </div>

          <div className="card">
            <h2 className="card-title">Search Items</h2>
            <input
              type="text"
              className="form-input"
              placeholder="Search by name or ID..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{ marginBottom: '1rem' }}
            />
            
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
            <h2 className="card-title">Rental Cart</h2>
            
            {cart.length === 0 ? (
              <div className="empty-state">
                <FaBox className="empty-state-icon" />
                <p className="empty-state-text">Cart is empty</p>
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

                <div className="total-section">
                  <div className="total-row">
                    <span>Subtotal:</span>
                    <span>${cart.reduce((sum, item) => sum + (parseFloat(item.price) * item.quantity), 0).toFixed(2)}</span>
                  </div>
                  <div className="total-row">
                    <span>Tax (6%):</span>
                    <span>${(cart.reduce((sum, item) => sum + (parseFloat(item.price) * item.quantity), 0) * 0.06).toFixed(2)}</span>
                  </div>
                  <div className="total-row total-final">
                    <span>Total:</span>
                    <span>${(cart.reduce((sum, item) => sum + (parseFloat(item.price) * item.quantity), 0) * 1.06).toFixed(2)}</span>
                  </div>
                </div>

                <button
                  type="button"
                  className="btn btn-primary"
                  style={{ 
                    width: '100%', 
                    marginTop: '1.5rem', 
                    padding: '1rem', 
                    fontSize: '1.1rem',
                    opacity: (loading || !customerPhone || cart.length === 0) ? 0.6 : 1,
                    cursor: (loading || !customerPhone || cart.length === 0) ? 'not-allowed' : 'pointer',
                    pointerEvents: (loading || !customerPhone || cart.length === 0) ? 'none' : 'auto'
                  }}
                  onClick={(e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    console.log('=== RENTAL BUTTON CLICKED ===', { 
                      loading, 
                      customerPhone, 
                      cartLength: cart.length,
                      cart: cart,
                      disabled: loading || !customerPhone || cart.length === 0
                    });
                    if (!loading && customerPhone && cart.length > 0) {
                      handleCheckout(e);
                    } else {
                      console.warn('Button click ignored - validation failed', {
                        loading,
                        hasPhone: !!customerPhone,
                        phoneLength: customerPhone?.length,
                        cartLength: cart.length
                      });
                    }
                  }}
                  disabled={loading || !customerPhone || cart.length === 0}
                  title={
                    !customerPhone ? 'Please enter customer phone number (10-15 digits)' :
                    cart.length === 0 ? 'Cart is empty - add items first' :
                    loading ? 'Processing rental...' :
                    'Complete rental transaction'
                  }
                >
                  {loading ? 'Processing...' : 'Complete Rental'}
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Rentals;

