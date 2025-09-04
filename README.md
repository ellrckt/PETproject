# PetProject 🐾
## 👥 Authors

### 🛠️ Developers

**Daniil Zubrik** - Backend Developer  
[![Email](https://img.shields.io/badge/Email-daniilzubrik@gmail.com-blue?style=flat&logo=gmail)](mailto:daniilzubrik@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-ellrckt-181717?style=flat&logo=github)](https://github.com/ellrckt)
[![Telegram](https://img.shields.io/badge/Telegram-@MLKS6-26A5E4?style=flat&logo=telegram)](https://t.me/MLKS6)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-daniilzubrik-0A66C2?style=flat&logo=linkedin)](https://linkedin.com/in/alexeypetrov)

## 📋 Description
### PetProject is a web application with a monolithic architecture, currently implementing an authentication system, user profile management, and geolocation functionality. The project is built on microservice-oriented principles using modern technologies and cloud infrastructure.

## 🏗️ Technology Stack
# Backend
Python with FastAPI framework

JWT tokens for authentication

Google OAuth for social authorization

SQLAlchemy as ORM for database operations

Pydantic for data validation and serialization

Alembic for migration management

# Databases
PostgreSQL with PostGIS extension for geodata

Redis for caching and fast data access

# Storage
Selectel S3 for storing media files and photos

# Infrastructure
Docker and Docker Compose for containerization

Isolated pet-network

## 🎯 Key Features
## 🔐 Authentication System
JWT tokens for secure access

Google OAuth integration

Protected API endpoints

## 👤 Profile Management
User profile creation and editing

Two-tier data storage (PostgreSQL + Redis)

Fast access to frequently requested data

## 🌐 Geolocation
User location detection service

Preparation for "recommended friends nearby" feature

Geospatial data support through PostGIS

## 💾 File Storage
Selectel S3 integration

User photo upload and storage

Scalable cloud storage

## 📊 Project Architecture
The project is organized following clean architecture principles:

Routers (API endpoints) → Services (business logic) → Repositories (data operations) → Databases

## 🐳 Docker Infrastructure
Running Services:
postgis/postgis:13-3.3 - main database with geospatial functions

dpage/pgadmin4:latest - web interface for PostgreSQL management

redis/redis-stack-server:latest - Redis server for caching

redis/redisinsight:latest - web interface for Redis management

## Network Settings:
Isolated bridge network pet-network

Port forwarding for service access

## ✅ Architecture Advantages
## 🚀 Performance
Redis caching significantly reduces load on main database

Fast API response due to optimized data structure (in progress...)

## 🔧 Code Maintainability
Clear separation of responsibilities between layers

Easy testing of individual components (in progress...)

Use of type hints and Pydantic models

## 📈 Scalability
Readiness for horizontal scaling (in progress...)

Easy future extraction into microservices (in progress...)

Cloud storage easily scales under load

## 🛡️ Security
JWT tokens for secure authentication

## ⚠️ Possible Improvements
For production readiness:
Adding monitoring (Prometheus, Grafana)

Configuring logging and request tracing

Setting up health-checks for containers

For security:

Under consideration

## 🎯 Development Perspectives
Implementation of geolocation-based recommendation system

Adding WebSocket for real-time notifications

Adding user chat functionality

Implementing full-text search

Splitting into microservices as load grows

Creating posts, subscriptions, likes, etc. (in progress...)

# Frontend
...
