import React, { useState } from 'react';
import { FaArrowLeft, FaSearch } from 'react-icons/fa';
import { transactionAPI } from '../services/api';
import './Returns.css';

const Returns = ({ employee, onBack }) => {
  const [customerPhone, setCustomerPhone] = useState('');
  const [outstandingRentals, setOutstandingRentals] = useState([]);
  const [selectedItems, setSelectedItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleSearch = async () => {
    if (!customerPhone || customerPhone.length < 10) {
      setMessage({ type: 'error', text: 'Please enter a valid phone number' });
      return;
    }

    setLoading(true);
    try {
      const response = await transactionAPI.getOutstandingRentals(customerPhone);
      setOutstandingRentals(response.data);
      if (response.data.length === 0) {
        setMessage({ type: 'info', text: 'No outstanding rentals found for this customer' });
      } else {
        setMessage('');
      }
    } catch (error) {
      setMessage({
        type: 'error',
        text: error.response?.data?.error || 'Failed to load rentals'
      });
      setOutstandingRentals([]);
    } finally {
      setLoading(false);
    }
  };

  const handleReturn = async () => {
    if (selectedItems.length === 0) {
      setMessage({ type: 'error', text: 'Please select items to return' });
      return;
    }

    setLoading(true);
    try {
      // Extract item IDs from selected rental IDs
      const itemIds = outstandingRentals
        .filter(rental => selectedItems.includes(rental.id))
        .map(rental => rental.item_id);
      
      await transactionAPI.processReturn(customerPhone, itemIds);
      setMessage({ type: 'success', text: 'Return processed successfully!' });
      setSelectedItems([]);
      setOutstandingRentals([]);
      setTimeout(() => {
        setMessage('');
        onBack();
      }, 2000);
    } catch (error) {
      setMessage({
        type: 'error',
        text: error.response?.data?.error || 'Failed to process return'
      });
    } finally {
      setLoading(false);
    }
  };

  const toggleItem = (rentalId) => {
    if (selectedItems.includes(rentalId)) {
      setSelectedItems(selectedItems.filter(id => id !== rentalId));
    } else {
      setSelectedItems([...selectedItems, rentalId]);
    }
  };

  return (
    <div className="returns-container">
      <div className="returns-header">
        <button className="btn btn-secondary" onClick={onBack}>
          <FaArrowLeft /> Back
        </button>
        <h1>Process Returns</h1>
        <div className="user-info">
          <span className="user-badge">{employee.full_name}</span>
        </div>
      </div>

      {message && (
        <div className={`alert alert-${message.type}`}>
          <span>{message.type === 'success' ? '✓' : message.type === 'error' ? '⚠️' : 'ℹ️'}</span>
          <span>{message.text}</span>
        </div>
      )}

      <div className="card">
        <h2 className="card-title">Customer Information</h2>
        <div className="form-group">
          <label className="form-label">Customer Phone Number</label>
          <div style={{ display: 'flex', gap: '1rem' }}>
            <input
              type="text"
              className="form-input"
              placeholder="Enter customer phone number"
              value={customerPhone}
              onChange={(e) => setCustomerPhone(e.target.value.replace(/\D/g, ''))}
              style={{ flex: 1 }}
            />
            <button
              className="btn btn-primary"
              onClick={handleSearch}
              disabled={loading}
            >
              <FaSearch /> Search
            </button>
          </div>
        </div>
      </div>

      {outstandingRentals.length > 0 && (
        <div className="card">
          <h2 className="card-title">Outstanding Rentals</h2>
          <div className="rentals-list">
            {outstandingRentals.map(rental => (
              <div
                key={rental.id}
                className={`rental-item ${selectedItems.includes(rental.id) ? 'selected' : ''}`}
                onClick={() => toggleItem(rental.id)}
              >
                <div className="rental-info">
                  <div className="rental-item-name">{rental.item_name}</div>
                  <div className="rental-details">
                    Rented: {new Date(rental.rental_date).toLocaleDateString()} | Due: {new Date(rental.due_date).toLocaleDateString()}
                    {rental.days_overdue > 0 && (
                      <span className="overdue-badge">Overdue: {rental.days_overdue} days</span>
                    )}
                  </div>
                </div>
                <div className="rental-checkbox">
                  <input
                    type="checkbox"
                    checked={selectedItems.includes(rental.id)}
                    onChange={() => toggleItem(rental.id)}
                  />
                </div>
              </div>
            ))}
          </div>

          {selectedItems.length > 0 && (
            <button
              className="btn btn-primary"
              style={{ width: '100%', marginTop: '1.5rem', padding: '1rem', fontSize: '1.1rem' }}
              onClick={handleReturn}
              disabled={loading}
            >
              {loading ? 'Processing...' : `Process Return (${selectedItems.length} items)`}
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default Returns;

