
# **Jade Commerce Backend System**

## **Project Description**
The Jade Commerce Backend System is a RESTful API service designed for a jade trading platform. It provides endpoints for user authentication, product management, shopping cart operations, and order processing. The backend is built using **Python**, **Flask**, and **MySQL**, with **role-based access control (RBAC)** for security. The project is containerized using **Docker** and supports cloud deployment on **AWS**.

---

## **Table of Contents**
1. [Features](#features)  
2. [Technologies Used](#technologies-used)  
3. [System Requirements](#system-requirements)  
4. [Installation](#installation)  
5. [Configuration](#configuration)  
6. [API Endpoints](#api-endpoints)  
7. [Running the Project Locally](#running-the-project-locally)  
8. [Containerized Deployment](#containerized-deployment)  
9. [Testing](#testing)  
10. [Future Enhancements](#future-enhancements)

---

## **Features**
- User Authentication (JWT-based login and logout)
- Role-based access control (e.g., admin-only routes)
- CRUD operations for:
  - **Users**
  - **Products**
  - **Shopping Cart**
  - **Orders**
- Containerized development and deployment using **Docker**
- Database management using **MySQL**
- Environment configuration with `.env` files

---

## **Technologies Used**
- **Backend Framework**: Flask
- **Database**: MySQL (via SQLAlchemy ORM)
- **Authentication**: Flask-JWT-Extended
- **Containerization**: Docker
- **Database Migration**: Flask-Migrate
- **Configuration Management**: Python-dotenv
- **HTTP Client Testing**: Postman (for API testing)

---

## **System Requirements**
- **Python**: 3.8 or higher
- **Docker**: Installed and running
- **MySQL**: Installed (or use Docker for a MySQL container)

---

## **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/jade-commerce-backend.git
   cd jade-commerce-backend
   ```

2. Set up a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the `.env` file:
   ```bash
   cp .env.example .env
   ```

   Update the `.env` file with your environment variables (e.g., database credentials).

---

## **Configuration**

| Environment Variable      | Description                          | Example Value                     |
|---------------------------|--------------------------------------|------------------------------------|
| `DATABASE_URI`            | MySQL connection string              | `mysql+pymysql://user:pass@db/jade`|
| `JWT_SECRET_KEY`          | Secret key for JWT                   | `your_secret_key`                  |
| `FLASK_ENV`               | Flask environment                    | `development` or `production`      |
| `PORT`                    | Port on which the app will run       | `5000`                             |

---

## **API Endpoints**

### **Authentication**
| Method | Endpoint          | Description                |
|--------|-------------------|----------------------------|
| POST   | `/auth/login`      | Login and receive JWT       |
| POST   | `/auth/logout`     | Logout and invalidate JWT   |
| GET    | `/auth/admin-only` | Admin-only access          |

### **Users**
| Method | Endpoint          | Description                      |
|--------|-------------------|----------------------------------|
| GET    | `/users/<id>`      | Get user details                 |
| PUT    | `/users/<id>`      | Update user details              |

### **Products**
| Method | Endpoint          | Description                      |
|--------|-------------------|----------------------------------|
| GET    | `/products`        | List all products                |
| POST   | `/products`        | Create a new product (Admin)     |

---

## **Running the Project Locally**

1. Ensure your database is running and the `.env` file is correctly configured.
2. Run the Flask application:
   ```bash
   flask run
   ```

3. Access the application at [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## **Containerized Deployment**

1. Build the Docker images:
   ```bash
   docker-compose build
   ```

2. Start the services:
   ```bash
   docker-compose up
   ```

3. Verify that the services are running:
   ```bash
   docker ps
   ```

4. Access the application at [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## **Testing**

- Use **Postman** or **curl** to test the API endpoints.
- Example request:
  ```bash
  curl -X POST http://127.0.0.1:5000/auth/login -H "Content-Type: application/json" -d '{"email": "test@example.com", "password": "password"}'
  ```

---

## **Future Enhancements**
- **CI/CD Integration**: Implement Jenkins pipelines for automated deployment.
- **Cloud Deployment**: Deploy containers on AWS ECS or Kubernetes.
- **Monitoring**: Add tools like Prometheus and Grafana for real-time monitoring.
- **Improved Security**: Implement HTTPS and rate limiting for API endpoints.
