# Google Analytics Setup

To enable Google Analytics tracking, follow these steps:

1. **Create a Google Analytics Account:**
   - Go to [Google Analytics](https://analytics.google.com/)
   - Create a new property for your website
   - Get your Measurement ID (format: G-XXXXXXXXXX)

2. **Update the Tracking Code:**
   - In `Templates/base.html`, replace `GA_MEASUREMENT_ID` with your actual Measurement ID
   - The code should look like:
     ```javascript
     gtag('config', 'G-XXXXXXXXXX');
     ```

3. **Verify Installation:**
   - Visit your website
   - Use Google Analytics Real-time reports to see if visits are being tracked
   - Check the admin dashboard for analytics data

## Features Added

### 🔐 Authentication System
- User registration and login
- Protected admin dashboard
- Session management

### 📊 Advanced Analytics Dashboard
- **Site Visit Tracking:** Total visits, last 30 days, last 7 days
- **Unique Visitors:** Count of distinct IP addresses
- **Page Popularity:** Most visited pages with visit counts
- **Recent Activity:** Latest page visits with timestamps
- **Contact Messages:** Total and recent message counts

### 🎯 Google Analytics Integration
- Automatic page view tracking
- User behavior analytics
- Real-time visitor insights

### 🛡️ Security Features
- Admin-only dashboard access
- CSRF protection on forms
- Secure user authentication

## Admin Dashboard Access

1. Login with admin credentials
2. Navigate to `/admin-dashboard/`
3. View comprehensive analytics and site management tools

## Database Models

- **PageVisit:** Tracks all page visits with IP, user agent, referrer, and timestamp
- Enhanced with analytics queries for dashboard metrics