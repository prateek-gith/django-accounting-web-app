# Accounting Software

A **Windows Forms-based Accounting Software** built using a **5-layer architecture**.
The system allows users to manage financial transactions, accounts, and records efficiently using **SQL Server** as the database and **Entity Framework (Database First approach)** for data access. ([GitHub][1])

This project demonstrates **clean architecture principles**, **Repository Pattern**, and **Unit of Work Pattern** for scalable and maintainable software development.

---

# Project Overview

This application is designed to help businesses or individuals manage their accounting operations such as:

* Managing accounts
* Recording financial transactions
* Organizing financial data
* Generating reports

The system follows a **layered architecture** to maintain separation of concerns and improve maintainability.

---

# Architecture

The project is structured using **5-layer architecture**:

### 1. Presentation Layer

* Handles the **User Interface**
* Built using **Windows Forms**
* Allows users to interact with the system

### 2. Application Layer

* Contains **business logic**
* Manages accounting operations and workflows

### 3. Domain Layer

* Defines **core entities**
* Example entities:

  * Account
  * Transaction
  * Ledger

### 4. Data Access Layer

* Responsible for **database communication**
* Uses **Entity Framework (Database First)**

### 5. Utility / Infrastructure Layer

* Contains helper utilities
* Handles configuration and common services

---

# Technologies Used

* **C#**
* **.NET Framework**
* **Windows Forms**
* **SQL Server**
* **Entity Framework**
* **Repository Pattern**
* **Unit of Work Pattern**

---

# Key Features

* User-friendly desktop interface
* Manage financial accounts
* Record and track transactions
* Structured layered architecture
* Clean separation between business logic and data access
* Scalable and maintainable design

---

# Design Patterns

### Repository Pattern

Provides an abstraction layer for database operations so that business logic does not directly interact with the database.

### Unit of Work Pattern

Ensures that multiple operations are executed within a **single transaction**, maintaining data integrity.

---

# Project Structure

```
Accounting_Software
│
├── Accounting                # Main Windows Forms UI
├── Accounting_App            # Application layer (Business Logic)
├── Accounting_Business       # Domain entities and models
├── Accounting_DataLayer      # Database operations
├── Accounting_Utility        # Helper classes and utilities
├── Accounting_ViewModel      # ViewModels for UI
├── packages                  # External dependencies
└── Accounting.sln            # Visual Studio Solution File
```

---

# Installation & Setup

### 1 Clone the Repository

```bash
git clone https://github.com/prateek-gith/Accounting_Software.git
```

---

### 2 Open Project

Open the solution file in **Visual Studio**

```
Accounting.sln
```

---

### 3 Configure Database

1. Install **SQL Server**
2. Create a database
3. Update the **connection string** in the configuration file.

---

### 4 Run the Application

Build and run the project using **Visual Studio**.

---

# Future Improvements

Possible improvements for the project:

* Dashboard with financial analytics
* Export reports to **Excel / PDF**
* Authentication & role-based access
* Cloud database support
* API integration

---

# Author

**Prateek Yadav**

Python & Web Developer
Interested in **Automation, Backend Development, and Data Systems**
