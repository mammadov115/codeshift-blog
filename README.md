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

## 📝 API Endpoints

The platform exposes a RESTful API for programmatic access:

| Endpoint                                      | View                                | Name                   | Description                     |
| --------------------------------------------- | ----------------------------------- | ---------------------- | ------------------------------- |
| `/api/v1/`                                    | `drf_yasg.views.SchemaView`         | `schema-swagger-ui`    | Swagger UI schema               |
| `/api/v1/accounts/authors/`                   | `AuthorProfileListView`             | `author-list`          | List all authors                |
| `/api/v1/accounts/authors/<int:id>/`          | `AuthorProfileRetrieveUpdateView`   | `author-detail`        | Retrieve/Update author profile  |
| `/api/v1/accounts/login/`                     | `LoginView`                         | `user-login`           | User login                      |
| `/api/v1/accounts/readers/`                   | `ReaderProfileListView`             | `reader-list`          | List all readers                |
| `/api/v1/accounts/readers/<int:id>/`          | `ReaderProfileRetrieveUpdateView`   | `reader-detail`        | Retrieve/Update reader profile  |
| `/api/v1/accounts/register/`                  | `RegisterView`                      | `user-register`        | Register new user               |
| `/api/v1/blogs/categories/`                   | `CategoryListCreateView`            | `category-list-create` | List/Create blog categories     |
| `/api/v1/blogs/categories/<slug:slug>/`       | `CategoryRetrieveUpdateDestroyView` | `category-detail`      | Retrieve/Update/Delete category |
| `/api/v1/blogs/comments/<int:pk>/`            | `CommentDetailView`                 | `comment-detail`       | Retrieve/Update/Delete comment  |
| `/api/v1/blogs/posts/`                        | `PostListCreateView`                | `post-list-create`     | List/Create posts               |
| `/api/v1/blogs/posts/<int:post_id>/comments/` | `CommentListCreateView`             | `comment-list-create`  | List/Create comments for a post |
| `/api/v1/blogs/posts/<slug:slug>/`            | `PostDetailView`                    | `post-detail`          | Retrieve/Update/Delete a post   |
| `/swagger<format>/`                           | `drf_yasg.views.SchemaView`         | `schema-json`          | JSON schema endpoint            |

---

## ⏱ Throttling & Rate Limiting

To prevent abuse and excessive load, all API endpoints are **throttled**:

* **Authenticated Users:** Limited to `100 requests/hour`
* **Anonymous Users:** Limited to `20 requests/hour`

Exceeded limits return:

```
HTTP 429 Too Many Requests
```

* This ensures fair usage, protects the server from overload, and prevents spam (e.g., excessive comment posting).

> You can configure throttling rates in `settings.py` under `REST_FRAMEWORK` → `DEFAULT_THROTTLE_RATES`.

---

## 🔧 Notes

* All API endpoints follow **RESTful conventions** and are fully documented via Swagger and Redoc.
* Nested comments, post CRUD, and author-reader roles are fully integrated with throttling to ensure a stable, fair system.


Enjoy blogging!

