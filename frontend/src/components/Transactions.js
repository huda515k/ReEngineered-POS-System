import React, { useState, useEffect } from 'react';
import { FaArrowLeft, FaHistory } from 'react-icons/fa';
import { transactionAPI } from '../services/api';
import './Transactions.css';

const Transactions = ({ onBack }) => {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTransactions();
  }, []);

  const loadTransactions = async () => {
    try {
      setLoading(true);
      const response = await transactionAPI.list();
      setTransactions(response.data);
    } catch (error) {
      console.error('Error loading transactions:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  const getTransactionTypeColor = (type) => {
    switch (type) {
      case 'Sale':
        return 'badge-success';
      case 'Rental':
        return 'badge-info';
      case 'Return':
        return 'badge-warning';
      default:
        return 'badge-info';
    }
  };

  return (
    <div className="transactions-container">
      <div className="transactions-header">
        <button className="btn btn-secondary" onClick={onBack}>
          <FaArrowLeft /> Back
        </button>
        <h1>Transaction History</h1>
        <div className="transactions-stats">
          <span className="stat-badge">
            {transactions.length} {transactions.length === 1 ? 'Transaction' : 'Transactions'}
          </span>
        </div>
      </div>

      <div className="card">
        {loading ? (
          <div className="spinner"></div>
        ) : transactions.length === 0 ? (
          <div className="empty-state">
            <FaHistory className="empty-state-icon" />
            <p className="empty-state-text">No transactions found</p>
          </div>
        ) : (
          <div className="transactions-list">
            {transactions.map(transaction => (
              <div key={transaction.id} className="transaction-card">
                <div className="transaction-header">
                  <div>
                    <span className={`badge ${getTransactionTypeColor(transaction.transaction_type)}`}>
                      {transaction.transaction_type}
                    </span>
                    <span className="transaction-id">#{transaction.id}</span>
                  </div>
                  <div className="transaction-amount">
                    ${parseFloat(transaction.total_amount).toFixed(2)}
                  </div>
                </div>
                <div className="transaction-details">
                  <div className="transaction-detail">
                    <span className="detail-label">Employee:</span>
                    <span>{transaction.employee_username}</span>
                  </div>
                  {transaction.customer_phone && (
                    <div className="transaction-detail">
                      <span className="detail-label">Customer:</span>
                      <span>{transaction.customer_phone}</span>
                    </div>
                  )}
                  <div className="transaction-detail">
                    <span className="detail-label">Date:</span>
                    <span>{formatDate(transaction.created_at)}</span>
                  </div>
                  {transaction.discount_applied && (
                    <div className="transaction-detail">
                      <span className="detail-label">Coupon:</span>
                      <span>{transaction.coupon_code}</span>
                    </div>
                  )}
                </div>
                {transaction.items && transaction.items.length > 0 && (
                  <div className="transaction-items">
                    <strong>Items:</strong>
                    <div className="items-list">
                      {transaction.items.map((item, index) => (
                        <span key={index} className="item-tag">
                          {item.item_name} × {item.quantity}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Transactions;

