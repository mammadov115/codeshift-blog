# CodeShift Blog Platform

This project is a fully containerized, feature-rich blog platform built with Django. It supports various user roles, post management functionalities, and deep, nested commenting for dynamic user interaction.

---

## 🚀 Getting Started

This application is designed to be run using **Docker** and **Docker Compose**. Once the containers are built and running, the database is automatically initialized with necessary migrations, initial data, and a superuser account.

### Prerequisites

- Docker
- Docker Compose

### Running the Project

**Build and Run Containers:**  
Navigate to the project's root directory (where `docker-compose.yml` is located) and run:

```bash
docker compose up --build
````

The `--build` flag ensures the latest changes (including initial data and superuser creation) are applied.

**Access the Application:**
The application will be accessible at:

```
http://localhost:8000/
```

---

## ✨ Core Features & Instructions

### 1. Initial State

Upon first accessing the homepage, you will not see any posts. This is by design, as posts must be created by an authenticated Author.

### 2. User Roles and Registration

The platform supports two types of authenticated users:

| Role   | Permissions                                           | Action Required                |
| ------ | ----------------------------------------------------- | ------------------------------ |
| Reader | Can view posts and write comments.                    | Register via the Sign-Up page. |
| Author | Can Create, Retrieve, Update, Delete their own posts. | Register via the Sign-Up page. |

> To begin posting: Please register as a new user (**Author**) first.

### 3. Post Creation and Management

* **Create Posts:** After logging in as an Author, navigate to the post creation page to write your first article.
* **Homepage Display:** All posts created by Authors will be immediately visible on the main homepage.
* **CRUD Operations:** Authors have full control (Create, Update, Delete) over the posts they have personally created.

### 4. Interactive Comments System

* **Commenting:** Any registered user (Reader or Author) can leave comments on posts.
* **Nested Comments:** The system supports a nested/threaded comment structure, allowing users to reply directly to other comments for organized discussions.

### 5. Django Administration Panel

The administrative backend allows superusers to manage all site content, users, permissions, and database records.

* **Access URL:** `http://localhost:8000/admin`
* **Default Superuser Credentials (Created on Docker Up):**

| Field    | Value                                     |
| -------- | ----------------------------------------- |
| Username | admin                                     |
| Email    | [admin@admin.com](mailto:admin@admin.com) |
| Password | admin                                     |

---


Enjoy blogging!

