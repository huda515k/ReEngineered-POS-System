import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FaShoppingCart, FaCrown, FaBriefcase, FaSignOutAlt } from 'react-icons/fa';
import './Header.css';

const Header = ({ employee, onLogout }) => {
  const navigate = useNavigate();

  const handleLogout = async () => {
    await onLogout();
    navigate('/login');
  };

  return (
    <header className="header">
      <div className="header-left">
        <div className="header-logo" onClick={() => navigate('/dashboard')}>
          <FaShoppingCart className="header-logo-icon" />
          <h1>POS System</h1>
        </div>
      </div>
      <div className="header-right">
        <div className="user-info">
          <div className="user-badge">
            {employee.position === 'Admin' ? (
              <FaCrown className="user-icon" />
            ) : (
              <FaBriefcase className="user-icon" />
            )}
            <span className="user-name">{employee.full_name}</span>
          </div>
          <span className="user-position">{employee.position}</span>
        </div>
        <button className="btn btn-danger logout-btn" onClick={handleLogout}>
          <FaSignOutAlt /> Logout
        </button>
      </div>
    </header>
  );
};

export default Header;

