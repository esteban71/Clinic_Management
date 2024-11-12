# Interop-rabilit-avanc-e




## User Guide

### Introduction

Welcome to the Clinic Management System! This system is designed to streamline the operations of medical clinics, making it easier to manage patient records, appointments, and staff information. This guide will help you get started with using the system effectively.

### Getting Started

#### Prerequisites

Before you begin, ensure you have the following installed on your local machine:
- Docker
- Docker Compose

#### Running the Application

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Start the Docker Containers:**
   ```bash
   docker-compose up -d
   ```

4. **Access the Application:**  
   Open your web browser and navigate to [http://localhost:3000](http://localhost:3000) to access the frontend of the application.

# User Roles and Permissions

The system supports different user roles, each with specific permissions:

## Receptionist:
- View, add, delete, and update patient records.
- View, add, delete, and update doctor records.

## Doctor:
- View patient records.
- View, add, delete, and update medical reports.

## Manager/Admin:
- Full access to all features, including user management and system settings.

# Features

## Patient Management
- **View Patients**: Navigate to the "Patients" section to view a list of all registered patients.
- **Add New Patient**: Click on "Add New Patient" and fill in the required details to register a new patient.
- **Edit Patient**: Select a patient from the list and click "Edit" to update their information.
- **Delete Patient**: Select a patient from the list and click "Delete" to remove their record from the system.

## Doctor Management
- **View Doctors**: Navigate to the "Doctors" section to view a list of all registered doctors.
- **Add New Doctor**: Click on "Add New Doctor" and fill in the required details to register a new doctor.
- **Edit Doctor**: Select a doctor from the list and click "Edit" to update their information.
- **Delete Doctor**: Select a doctor from the list and click "Delete" to remove their record from the system.

## Medical Report Management
- **View Medical Reports**: Navigate to the "Medical Reports" section under a patient's profile to view a list of all medical reports for that patient.
- **Add New Medical Report**: Click on "Add New Medical Report" and fill in the required details to create a new medical report.
- **Edit Medical Report**: Select a medical report from the list and click "Edit" to update its information.
- **Delete Medical Report**: Select a medical report from the list and click "Delete" to remove it from the system.

# Authentication and Authorization

The system uses Keycloak for authentication and authorization. Each user must log in with their credentials to access the system. Depending on their role, users will have access to different features. Keycloak ensures secure and centralized management of user identities and permissions.

# Troubleshooting

If you encounter any issues while using the system, please refer to the following steps:

- **Check Docker Containers**: Ensure all Docker containers are running without errors.
- **Database Migrations**: Verify that all database migrations have been applied successfully.
- **Logs**: Check the application logs for any error messages that can help diagnose the issue.






# Developpement

## Explication migration with alembic

Before running the migration, you need to  launch the docker-compose file with the following command:

```bash
docker compose up
```

Use the following command to generate a migration script:

```bash
docker compose exec back alembic revision --autogenerate -m "<your name of migration>"
```

Then, apply the migration with the following command:

```bash
docker compose exec back alembic upgrade head
```

if you want to downgrade the migration, use the following command:

```bash
docker compose exec back alembic downgrade -1
```





