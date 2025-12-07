import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { authAPI } from './services/api';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import Sales from './components/Sales';
import Rentals from './components/Rentals';
import Returns from './components/Returns';
import Inventory from './components/Inventory';
import Employees from './components/Employees';
import Transactions from './components/Transactions';
import Header from './components/Header';
import './App.css';

function App() {
  const [employee, setEmployee] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is already logged in (session check)
    checkSession();
  }, []);

  const checkSession = async () => {
    try {
      // Try to get current session - if fails, user not logged in
      // For now, we'll rely on localStorage
      const savedEmployee = localStorage.getItem('employee');
      if (savedEmployee) {
        setEmployee(JSON.parse(savedEmployee));
      }
    } catch (error) {
      // Not logged in
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = (employeeData) => {
    setEmployee(employeeData);
    localStorage.setItem('employee', JSON.stringify(employeeData));
  };

  const handleLogout = async () => {
    try {
      await authAPI.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setEmployee(null);
      localStorage.removeItem('employee');
    }
  };

  if (loading) {
    return (
      <div className="App">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <Router>
      <div className="App">
        {employee && <Header employee={employee} onLogout={handleLogout} />}
        <Routes>
          <Route
            path="/login"
            element={
              employee ? (
                <Navigate to="/dashboard" replace />
              ) : (
                <Login onLogin={handleLogin} />
              )
            }
          />
          <Route
            path="/dashboard"
            element={
              employee ? (
                <Dashboard employee={employee} />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
          <Route
            path="/sales"
            element={
              employee ? (
                <Sales
                  employee={employee}
                  onBack={() => window.history.back()}
                />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
          <Route
            path="/rentals"
            element={
              employee ? (
                <Rentals
                  employee={employee}
                  onBack={() => window.history.back()}
                />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
          <Route
            path="/returns"
            element={
              employee ? (
                <Returns
                  employee={employee}
                  onBack={() => window.history.back()}
                />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
          <Route
            path="/inventory"
            element={
              employee ? (
                <Inventory onBack={() => window.history.back()} />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
          <Route
            path="/employees"
            element={
              employee && employee.position === 'Admin' ? (
                <Employees onBack={() => window.history.back()} />
              ) : (
                <Navigate to="/dashboard" replace />
              )
            }
          />
          <Route
            path="/transactions"
            element={
              employee ? (
                <Transactions onBack={() => window.history.back()} />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
          <Route
            path="/"
            element={<Navigate to={employee ? "/dashboard" : "/login"} replace />}
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
