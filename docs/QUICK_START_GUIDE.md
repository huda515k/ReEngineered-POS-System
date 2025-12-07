# Quick Start Guide - How to View the POS System

## 🚀 Quick Start (2 Terminal Windows)

### Step 1: Start the Backend Server (Terminal 1)

```bash
# Navigate to backend directory
cd "/Users/hudakhannyazee/Documents/SRe Project/reengineered_pos_system/backend"

# Activate virtual environment
source venv/bin/activate

# Start Django server
python manage.py runserver
```

**Expected Output:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

✅ **Backend is now running at:** http://localhost:8000

---

### Step 2: Start the Frontend Server (Terminal 2)

```bash
# Navigate to frontend directory
cd "/Users/hudakhannyazee/Documents/SRe Project/reengineered_pos_system/frontend"

# Install dependencies (only needed first time)
npm install

# Start React development server
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view pos-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

✅ **Frontend is now running at:** http://localhost:3000

---

### Step 3: Open in Browser

1. **Open your web browser** (Chrome, Firefox, Safari, or Edge)
2. **Navigate to:** http://localhost:3000
3. **You should see the Login page**

---

## 🔐 Test Credentials

Use these credentials to log in:

### Admin Account:
- **Username:** `110001`
- **Password:** `1`

### Cashier Account:
- **Username:** `110002`
- **Password:** `lehigh2016`

---

## 📱 What You Can Do

### As Admin:
- ✅ View Dashboard
- ✅ Process Sales
- ✅ Process Rentals
- ✅ Process Returns
- ✅ View Inventory
- ✅ View Transactions
- ✅ **Manage Employees** (Admin only)

### As Cashier:
- ✅ View Dashboard
- ✅ Process Sales
- ✅ Process Rentals
- ✅ Process Returns
- ✅ View Inventory
- ✅ View Transactions

---

## 🛠️ Troubleshooting

### Backend Issues

**Problem:** `ModuleNotFoundError` or import errors
```bash
# Solution: Make sure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**Problem:** `Port 8000 already in use`
```bash
# Solution: Use a different port
python manage.py runserver 8001
# Then update frontend/src/services/api.js to use port 8001
```

**Problem:** Database errors
```bash
# Solution: Run migrations
python manage.py migrate
```

### Frontend Issues

**Problem:** `npm: command not found`
```bash
# Solution: Install Node.js from https://nodejs.org/
```

**Problem:** `Port 3000 already in use`
```bash
# Solution: React will ask to use a different port, press Y
# Or set PORT environment variable:
PORT=3001 npm start
```

**Problem:** `Cannot connect to backend`
- Make sure backend is running on port 8000
- Check that CORS is enabled in backend settings
- Verify `proxy` in `package.json` points to `http://localhost:8000`

**Problem:** `Module not found` errors
```bash
# Solution: Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

---

## 🔍 Verify Everything is Working

### 1. Check Backend API
Open in browser: http://localhost:8000/api/items/

You should see JSON data with items.

### 2. Check Frontend
Open in browser: http://localhost:3000

You should see the Login page.

### 3. Test Login
- Enter username: `110001`
- Enter password: `1`
- Click "Sign In"
- You should see the Dashboard

---

## 📂 File Locations

- **Backend:** `/Users/hudakhannyazee/Documents/SRe Project/reengineered_pos_system/backend/`
- **Frontend:** `/Users/hudakhannyazee/Documents/SRe Project/reengineered_pos_system/frontend/`
- **Database:** `/Users/hudakhannyazee/Documents/SRe Project/reengineered_pos_system/backend/db.sqlite3`

---

## 🎯 Quick Commands Reference

### Backend Commands
```bash
cd backend
source venv/bin/activate
python manage.py runserver          # Start server
python manage.py migrate            # Run migrations
python manage.py createsuperuser    # Create admin user
python manage.py test               # Run tests
```

### Frontend Commands
```bash
cd frontend
npm install                        # Install dependencies
npm start                          # Start development server
npm run build                      # Build for production
npm test                           # Run tests
```

---

## 🌐 Access Points

Once both servers are running:

| Service | URL | Description |
|--------|-----|-------------|
| **Frontend** | http://localhost:3000 | Main application (start here) |
| **Backend API** | http://localhost:8000/api/ | REST API endpoints |
| **Django Admin** | http://localhost:8000/admin/ | Database admin (if superuser created) |

---

## ✅ Success Checklist

- [ ] Backend server running (Terminal 1 shows "Starting development server")
- [ ] Frontend server running (Terminal 2 shows "Compiled successfully")
- [ ] Browser opens http://localhost:3000
- [ ] Login page displays
- [ ] Can log in with test credentials
- [ ] Dashboard displays after login
- [ ] Can navigate to different sections

---

## 🎉 You're Ready!

Once both servers are running and you can see the login page, you're all set! The application is fully functional and ready to use.

**Note:** Keep both terminal windows open while using the application. Press `Ctrl+C` in each terminal to stop the servers when done.

