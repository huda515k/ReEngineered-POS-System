import React, { useState, useEffect } from 'react';
import { FaArrowLeft, FaWarehouse, FaSearch } from 'react-icons/fa';
import { itemAPI } from '../services/api';
import './Inventory.css';

const Inventory = ({ onBack }) => {
  const [items, setItems] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadItems();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      loadItems();
    }, 300);
    return () => clearTimeout(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchTerm]);

  const loadItems = async () => {
    try {
      setLoading(true);
      const response = await itemAPI.list(searchTerm);
      setItems(response.data);
    } catch (error) {
      console.error('Error loading items:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="inventory-container">
      <div className="inventory-header">
        <button className="btn btn-secondary" onClick={onBack}>
          <FaArrowLeft /> Back
        </button>
        <h1>Inventory Management</h1>
        <div className="inventory-stats">
          <span className="stat-badge">
            {items.length} {items.length === 1 ? 'Item' : 'Items'}
          </span>
        </div>
      </div>

      <div className="card">
        <div className="search-bar">
          <FaSearch className="search-icon" />
          <input
            type="text"
            className="form-input"
            placeholder="Search items by name or ID..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        {loading ? (
          <div className="spinner"></div>
        ) : items.length === 0 ? (
          <div className="empty-state">
            <FaWarehouse className="empty-state-icon" />
            <p className="empty-state-text">No items found</p>
          </div>
        ) : (
          <div className="inventory-table-wrapper">
            <table className="table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Price</th>
                  <th>Quantity</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {items.map(item => (
                  <tr key={item.id}>
                    <td>
                      <span className="item-id-badge">#{item.legacy_item_id}</span>
                    </td>
                    <td>
                      <strong>{item.name}</strong>
                    </td>
                    <td>
                      <span className="price-badge">${parseFloat(item.price).toFixed(2)}</span>
                    </td>
                    <td>
                      <span className={`quantity-badge ${item.quantity > 10 ? 'high' : item.quantity > 0 ? 'medium' : 'low'}`}>
                        {item.quantity}
                      </span>
                    </td>
                    <td>
                      {item.quantity > 10 ? (
                        <span className="badge badge-success">In Stock</span>
                      ) : item.quantity > 0 ? (
                        <span className="badge badge-warning">Low Stock</span>
                      ) : (
                        <span className="badge badge-danger">Out of Stock</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default Inventory;

