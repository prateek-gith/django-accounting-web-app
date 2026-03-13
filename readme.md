# My Accounting Project

A **web-based Accounting Management System** built using **Django, Python, SQLite3, HTML, and CSS**.
The system helps manage financial records such as **Sales, Purchases, Payments, Receipts, Accounts, Daybook, and Ledger** with a clean dashboard and graphical reports.

This project also supports **automatic PDF generation for vouchers**, making it useful for basic business accounting operations.

---

# Project Features

* Dashboard with financial summary
* Graphical representation of accounting data
* Manage Sales transactions
* Manage Purchase transactions
* Record Receipts
* Record Payments
* Maintain Accounts
* Daybook for daily transactions
* Ledger for account-wise reports
* Generate **PDF vouchers automatically**
* Clean sidebar navigation UI
* Database integration with SQLite

---

# Dashboard

The dashboard provides:

* Total Sales
* Total Purchases
* Total Receipts
* Total Payments
* Monthly graph visualization of accounting activity

This helps users quickly understand business financial performance.

---

# Technologies Used

Backend

* Python
* Django

Frontend

* HTML
* CSS
* JavaScript

Database

* SQLite3

Other Tools

* Django Template Engine
* Chart/Graph visualization library
* PDF generation library (for voucher export)

---

# Project Modules

### Dashboard

Displays financial summary and graph visualization.

### Sales

Used to record and manage all sales transactions.

### Purchase

Used to record purchase transactions.

### Payment

Records payments made to suppliers or other parties.

### Receipt

Records incoming payments from customers.

### Daybook

Shows all transactions recorded day by day.

### Ledger

Displays account-wise transaction history.

### Accounts

Used to manage account names and details.

---

# Project Structure

```
MY_ACCOUNTING_PROJECT
│
├── accounts
├── dashboard
├── daybook
├── ledger
├── payments
├── purchase
├── receipts
├── sales
│
├── my_accounting_project   # Main Django Project Folder
│
├── db.sqlite3              # Database
├── manage.py               # Django Project Manager
└── readme.md
```

---

# Installation Guide

### 1 Clone Repository

```bash
git clone https://github.com/prateek-gith/MY_ACCOUNTING_PROJECT.git
```

---

### 2 Move into Project Folder

```bash
cd MY_ACCOUNTING_PROJECT
```

---

### 3 Install Dependencies

```bash
pip install django
```

(Install additional libraries if required)

---

### 4 Run Migrations

```bash
python manage.py migrate
```

---

### 5 Start Server

```bash
python manage.py runserver
```

---

# Future Improvements

* User authentication system
* Multi-user accounting
* Excel export for reports
* Profit & Loss report
* GST report support
* Advanced financial analytics
* Cloud database support

---

# Author

**Prateek Yadav**

Python Developer | Django Developer

Skills:

* Python
* Django
* Web Development
* Automation
* Data Processing

---

# License

This project is open-source and available for learning and educational purposes.

---
