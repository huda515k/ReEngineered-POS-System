import React, { useState, useEffect } from 'react';
import { FaArrowLeft, FaUsers, FaPlus, FaTrash } from 'react-icons/fa';
import { employeeAPI } from '../services/api';
import './Employees.css';

const Employees = ({ onBack }) => {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    first_name: '',
    last_name: '',
    position: 'Cashier'
  });
  const [message, setMessage] = useState('');

  useEffect(() => {
    loadEmployees();
  }, []);

  const loadEmployees = async () => {
    try {
      setLoading(true);
      const response = await employeeAPI.list();
      setEmployees(response.data);
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to load employees' });
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await employeeAPI.create(formData);
      setMessage({ type: 'success', text: 'Employee created successfully' });
      setShowAddForm(false);
      setFormData({
        username: '',
        password: '',
        first_name: '',
        last_name: '',
        position: 'Cashier'
      });
      loadEmployees();
    } catch (error) {
      setMessage({
        type: 'error',
        text: error.response?.data?.error || 'Failed to create employee'
      });
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this employee?')) {
      return;
    }
    try {
      await employeeAPI.delete(id);
      setMessage({ type: 'success', text: 'Employee deleted successfully' });
      loadEmployees();
    } catch (error) {
      setMessage({
        type: 'error',
        text: error.response?.data?.error || 'Failed to delete employee'
      });
    }
  };

  return (
    <div className="employees-container">
      <div className="employees-header">
        <button className="btn btn-secondary" onClick={onBack}>
          <FaArrowLeft /> Back
        </button>
        <h1>Employee Management</h1>
        <button
          className="btn btn-primary"
          onClick={() => setShowAddForm(!showAddForm)}
        >
          {showAddForm ? (
            <>Cancel</>
          ) : (
            <>
              <FaPlus /> Add Employee
            </>
          )}
        </button>
      </div>

      {message && (
        <div className={`alert alert-${message.type}`}>
          <span>{message.type === 'success' ? '✓' : '⚠️'}</span>
          <span>{message.text}</span>
        </div>
      )}

      {showAddForm && (
        <div className="card">
          <h2 className="card-title">Add New Employee</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-grid">
              <div className="form-group">
                <label className="form-label">Username</label>
                <input
                  type="text"
                  className="form-input"
                  value={formData.username}
                  onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <label className="form-label">Password</label>
                <input
                  type="password"
                  className="form-input"
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  required
                  minLength={6}
                />
              </div>
              <div className="form-group">
                <label className="form-label">First Name</label>
                <input
                  type="text"
                  className="form-input"
                  value={formData.first_name}
                  onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <label className="form-label">Last Name</label>
                <input
                  type="text"
                  className="form-input"
                  value={formData.last_name}
                  onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <label className="form-label">Position</label>
                <select
                  className="form-input"
                  value={formData.position}
                  onChange={(e) => setFormData({ ...formData, position: e.target.value })}
                  required
                >
                  <option value="Cashier">Cashier</option>
                  <option value="Admin">Admin</option>
                </select>
              </div>
            </div>
            <button type="submit" className="btn btn-primary">
              Create Employee
            </button>
          </form>
        </div>
      )}

      <div className="card">
        <h2 className="card-title">All Employees</h2>
        {loading ? (
          <div className="spinner"></div>
        ) : employees.length === 0 ? (
          <div className="empty-state">
            <FaUsers className="empty-state-icon" />
            <p className="empty-state-text">No employees found</p>
          </div>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Username</th>
                <th>Name</th>
                <th>Position</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {employees.map(employee => (
                <tr key={employee.id}>
                  <td><strong>{employee.username}</strong></td>
                  <td>{employee.full_name}</td>
                  <td>
                    <span className={`badge ${employee.position === 'Admin' ? 'badge-info' : 'badge-success'}`}>
                      {employee.position}
                    </span>
                  </td>
                  <td>
                    <span className={`badge ${employee.is_active ? 'badge-success' : 'badge-danger'}`}>
                      {employee.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td>
                    <button
                      className="btn btn-danger"
                      style={{ padding: '0.5rem 1rem', fontSize: '0.875rem' }}
                      onClick={() => handleDelete(employee.id)}
                    >
                      <FaTrash /> Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
    );
};

export default Employees;

