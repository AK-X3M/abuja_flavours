# 🍽 Abuja Flavours — Django Food Ordering App

A full-stack, production-ready food ordering web application built with Django, featuring authentic West African cuisine.

## ✨ Features

- **Authentication**: Signup / Login / Logout
- **Menu**: Category-filtered meal browsing with images
- **Cart**: Add, update quantity, remove items — with live AJAX updates
- **Checkout**: EcoCash & Credit Card (simulated)
- **Order Confirmation**: Order summary with status tracker
- **Admin Panel**: Full Django admin for managing meals, orders

## 🚀 Quick Start

### 1. Prerequisites
```bash
python >= 3.10
pip
```

### 2. Install Dependencies
```bash
pip install django pillow
```

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Seed the Database
```bash
python manage.py seed_data
```

### 5. Create Admin User (optional)
```bash
python manage.py createsuperuser
```

### 6. Start the Server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

## 📁 Project Structure

```
abuja_flavours/
├── abuja_flavours/         # Project config
│   ├── settings.py
│   └── urls.py
├── core/                   # Main app
│   ├── models.py           # Category, Meal, Cart, Order, OrderItem
│   ├── views.py            # All views
│   ├── urls.py             # URL patterns
│   ├── context_processors.py
│   ├── templatetags/
│   │   └── dict_extras.py  # get_item filter
│   └── management/
│       └── commands/
│           └── seed_data.py
├── templates/
│   ├── base.html
│   └── core/
│       ├── landing.html
│       ├── auth.html
│       ├── menu.html
│       ├── cart.html
│       ├── checkout.html
│       └── confirmation.html
└── static/
    ├── css/main.css
    └── js/main.js
```

## 🎨 Design System

| Token | Value | Usage |
|-------|-------|-------|
| Primary Red | #C0392B | CTAs, prices, accents |
| Yellow | #F0B429 | Highlights |
| Amber | #E8793A | Gradients, badges |
| Background | #F8F6F2 | Page background |
| Charcoal | #2C2C2C | Text |

**Fonts**: Playfair Display (headings) + DM Sans (body)

## 💳 Payment Simulation

Both payment methods are simulated:
- **EcoCash**: Enter any phone number + PIN
- **Credit Card**: Enter any 16-digit number + expiry + CVV

No real charges are made.

## 🌍 Tax

15% tax is automatically applied at checkout.

## ⚙️ Admin

Access at `/admin/` with superuser credentials to manage:
- Categories & Meals (with image URLs)
- Cart items
- Orders & Order Items
