# Social Networking Backend

This is a social networking backend application built using Django and Django REST Framework (DRF) with JWT authentication. The backend includes features for user authentication, searching users, managing friend requests, and more. The project uses Docker to simplify the setup process.

## Features

- **User Authentication**: Signup and login functionalities with JWT tokens.
- **Email Case-Insensitive Login**: Allows users to login without worrying about email case sensitivity.
- **User Search**: Search users by email or username with pagination support.
- **Friend Request Management**: Send, accept, or reject friend requests.
- **Rate Limiting**: Limits the number of friend requests sent within a specific time frame.
- **Persistent Data Storage**: Uses SQLite for development.

## Technologies Used

- **Django**: Web framework for building the backend.
- **Django REST Framework**: For building RESTful APIs.
- **Simple JWT**: For handling JSON Web Token (JWT) authentication.
- **Docker**: For containerizing the application to simplify setup and deployment.
- **SQLite**: Default database for development.

## Prerequisites

Before you begin, ensure you have the following software installed on your machine:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: Comes with Docker Desktop for Windows and Mac. For Linux, install it separately: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Installation Guide

### 1. Clone the Repository

Clone the project to your local machine using the following command:

```bash
git clone https://github.com/VismayRaul/social_networking_backend.git
cd social_networking_backend
docker-compose up #command to run the project```

(**Note**: Postman collection for testing is provided in the project file itself.)
