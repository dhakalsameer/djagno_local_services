# 🇳🇵 Local Services Marketplace (Django)

**A Nepal-focused, real-world service booking platform**

---

## 🚀 Project Overview

This is a web-based marketplace where **service providers** (plumbers, electricians, tutors, cleaners, freelancers, etc.) can list their services, and **customers** can search, book, and review them.

The goal of this project is to demonstrate:

- Real business logic  
- Role-based authentication & permissions  
- Booking & availability systems  
- Scalable backend thinking with Django  

Perfect for:
✔️ Portfolio  
✔️ Freelancing  
✔️ Remote backend jobs  

---

## 🎯 Core Idea

Unlike basic CRUD projects (like Room Finder), this platform includes:

- Two user roles: **Customer & Service Provider**
- Booking + availability logic
- Reviews & ratings
- Dashboards & analytics
- Real-world permission handling

---

## 🗂️ Key Features

### 1️⃣ User Roles & Authentication

**Roles**
- 👤 Customer
- 🧑‍🔧 Service Provider

**Features**
- Register & Login
- Role-based access control
- Providers can manage *only their own services*
- Customers can book *any available service*

---

### 2️⃣ Service Management (Providers)

- Create / Update / Delete services
- Set:
  - Price
  - Description
  - Category
  - Availability schedule
- View booking requests

---

### 3️⃣ Booking System (Customers)

- Browse & search services
- Book services with date & time
- Track booking status:
  - Pending
  - Accepted
  - Completed
  - Cancelled

---

### 4️⃣ Reviews & Ratings

- Customers can leave reviews after service completion
- Providers get:
  - Star ratings
  - Public feedback

---

### 5️⃣ Dashboards

**Provider Dashboard**
- Total bookings  
- Ratings & reviews  

**Customer Dashboard**
- Booking history  
- Active bookings  

---

## 🛠️ Tech Stack

- **Backend:** Django, Django ORM  
- **Frontend:** Django Templates + Tailwind CSS  
- **Auth:** Django Authentication + Custom Roles  
- **Database:** SQLite (dev) / PostgreSQL (prod ready)  

---

## 🧩 App Structure

```txt
local_services/
├── accounts/      # Auth, profiles, roles
├── services/      # Service listings
├── bookings/      # Booking system
├── reviews/       # Reviews & ratings
├── dashboard/     # User dashboards
├── templates/
├── static/
└── manage.py
