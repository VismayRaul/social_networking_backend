# Social Networking Backend

This is a social networking backend built using Django and Django REST Framework (DRF) with JWT authentication. The application uses Docker for easy setup and deployment.

## Features

- User signup with username, email, and password.
- User login with JWT-based authentication.
- Case-insensitive email handling during login.
- Protected endpoints accessible only to authenticated users.
- Search for users by email and name.
- Friend request management (send, accept, reject).
- Rate-limiting to prevent spamming friend requests.
- Persistent data storage using SQLite (or PostgreSQL if defined).

## Technologies Used

- **Django**: Python web framework.
- **Django REST Framework**: For building RESTful APIs.
- **Simple JWT**: For handling authentication using JSON Web Tokens.
- **Docker**: For containerization and easy setup.
- **SQLite**: Default database for development (can be switched to PostgreSQL or other databases).

## Prerequisites

- Docker and Docker Compose installed on your machine.
- Basic knowledge of Docker, Django, and REST APIs.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/social-networking-backend.git
cd social-networking-backend
