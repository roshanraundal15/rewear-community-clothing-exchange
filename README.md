## 🚀 Problem Statement  
ReWear – Community Clothing Exchange 
Build a community-driven clothing exchange platform that allows users to donate, request, and swap clothes locally, promoting sustainability and affordability.

---

## 👥 Team Details

### 👑 Team Leader
- **Name:** Roshan Dattatray Raundal  
- **Email:** rdraundal15@gmail.com  
- **Phone:** 8828095273  

### 💡 Reviewer
- **Name:** Yashkumar Vaishnav (GitHub: `yava-odoo`)

### 👨‍💻 Team Members
1. **Name:** Mayur Sapkal  
   **Email:** mayursapkal41@apsit.edu.in  
  

2. **Name:** Karan Panchal  
   **Email:** *panchalkaran677@gmail.com*  
  

3. **Name:** Lucky Sharma  
   **Email:** mrluckysharma165@gmail.com  
 

---

## 🔗 Collaborator
- Added GitHub user: `yava-odoo`



# ReWear 👕♻

_ReWear_ is a community-driven clothing exchange platform built with Django. The platform empowers users to list pre-loved clothes, request direct swaps, or redeem items using points—promoting sustainable fashion and helping reduce textile waste.

---

## 🌱 Overview

ReWear aims to foster a sustainable fashion community by encouraging users to reuse wearable garments instead of discarding them. The platform supports both direct swaps and a point-based redemption system, making it easy and rewarding to refresh your wardrobe while helping the planet.

![WhatsApp Image 2025-07-12 at 16 35 14_385c16ab](https://github.com/user-attachments/assets/80de164e-aa6f-49c4-bb09-934aa47d68a4)


## 🚀 Features

- **User Registration & Authentication**
  - Secure email/password signup and login
- **Landing Page**
  - Platform introduction
  - Calls-to-action: "Start Swapping", "Browse Items", "List an Item"
  - Featured items carousel
- **User Dashboard**
  - Profile details and points balance
  - Overview of uploaded items
  - List of ongoing and completed swaps
- **Item Detail Page**
  - Image gallery and full item description
  - Uploader information
  - Options to "Swap Request" or "Redeem via Points"
  - Item availability status
- **Add New Item Page**
  - Upload images
  - Enter title, description, category, type, size, condition, and tags
  - Submit to list item
- **Admin Role**
  - Moderate and approve/reject item listings
  - Remove inappropriate or spam items
  - Lightweight admin panel for oversight
- **Professional UI**
  - Modern design using Bootstrap

---

## 🗂️ Project Structure

```
rewear/
├── core/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── templates/core/
│   │   ├── dashboard.html
│   │   ├── item_detail.html
│   │   ├── upload_item.html
│   │   └── manage_requests.html
│   └── static/
├── rewear/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/
├── db.sqlite3
└── manage.py
```

---

## ⚡ Getting Started

### 1. Setup Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate       # On Linux/macOS
.venv\Scripts\activate          # On Windows
```

### 2. Install Dependencies

```bash
pip install django pillow
```

### 3. Database Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

---

## 💡 Usage

- **List a Clothing Item:** Upload images, add details, and submit for admin approval.
- **Browse & Swap:** Explore the catalog, request a swap, or redeem items using your points.
- **Dashboard:** Track your uploads, swaps, and points balance.
- **Admin Panel:** Approve/reject listings and manage user submissions.

---

## 👩‍💻 Technologies Used

- **Backend:** Django (Python)
- **Frontend:** Bootstrap, HTML5, CSS3
- **Database:** SQLite
- **Image Handling:** Pillow

---

## 🏆 Contribution

We welcome contributions to enhance sustainable fashion! Feel free to submit pull requests, report issues, or suggest new features.

---

**ReWear** — Redefining wardrobes, one swap at a time!
