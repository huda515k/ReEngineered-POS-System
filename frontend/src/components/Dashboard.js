import React from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  FaDollarSign, 
  FaBox, 
  FaUndo, 
  FaWarehouse, 
  FaHistory, 
  FaUsers,
  FaChevronRight 
} from 'react-icons/fa';
import './Dashboard.css';

const Dashboard = ({ employee }) => {
  const navigate = useNavigate();
  const isAdmin = employee.position === 'Admin';

  const menuItems = [
    {
      title: 'Sales',
      icon: FaDollarSign,
      description: 'Process sales transactions',
      color: '#48bb78',
      onClick: () => navigate('/sales'),
      available: true,
    },
    {
      title: 'Rentals',
      icon: FaBox,
      description: 'Manage rental transactions',
      color: '#4299e1',
      onClick: () => navigate('/rentals'),
      available: true,
    },
    {
      title: 'Returns',
      icon: FaUndo,
      description: 'Process item returns',
      color: '#ed8936',
      onClick: () => navigate('/returns'),
      available: true,
    },
    {
      title: 'Inventory',
      icon: FaWarehouse,
      description: 'View and manage inventory',
      color: '#9f7aea',
      onClick: () => navigate('/inventory'),
      available: true,
    },
    {
      title: 'Transactions',
      icon: FaHistory,
      description: 'View transaction history',
      color: '#38b2ac',
      onClick: () => navigate('/transactions'),
      available: true,
    },
    {
      title: 'Employees',
      icon: FaUsers,
      description: 'Manage employees',
      color: '#f56565',
      onClick: () => navigate('/employees'),
      available: isAdmin,
    },
  ];

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <div className="dashboard-welcome">
          <h1>Welcome back, {employee.full_name}!</h1>
          <p className="dashboard-subtitle">Select an option below to get started</p>
        </div>
        <div className="user-badge-large">
          <span className="user-position-badge">{employee.position}</span>
        </div>
      </div>

      <div className="dashboard-grid">
        {menuItems
          .filter(item => item.available)
          .map((item, index) => {
            const Icon = item.icon;
            return (
              <div
                key={index}
                className="dashboard-card"
                onClick={item.onClick}
                style={{ '--card-color': item.color }}
              >
                <div className="dashboard-card-icon-wrapper" style={{ backgroundColor: `${item.color}15` }}>
                  <Icon className="dashboard-card-icon" style={{ color: item.color }} />
                </div>
                <div className="dashboard-card-content">
                  <h3 className="dashboard-card-title">{item.title}</h3>
                  <p className="dashboard-card-description">{item.description}</p>
                </div>
                <FaChevronRight className="dashboard-card-arrow" style={{ color: item.color }} />
              </div>
            );
          })}
      </div>
    </div>
  );
};

export default Dashboard;

