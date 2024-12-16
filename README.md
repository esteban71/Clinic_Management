# Interopérabilité Avancée

## Nom des membres du groupe

- Esteban Arroyo
- Radhwane Namaoui

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

3. **Access the Application:**  
   Open your web browser and navigate to [http://localhost:3000](http://localhost:3000) to access the frontend of the application.

   Note: Please wait 2 to 3 minutes before connecting to the site to ensure all services are fully initialized.

4. **Login Credentials**:

Use the following credentials to log in as an admin:
   
   Username: `admin`
   
   Password: `password`


# User Roles and Permissions

The system supports different user roles, each with specific permissions:

## Receptionist:
- View, add, delete, and update patient records.
- View, add, delete, and update doctor records.

## Doctor:
- View patient records.
- View medical device reports.
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

## Medical Device Management
- **View Medical Device Report**: Navigate to the "Dispositif" section under a patient's profile to view a list of all dispositif's report for that patient.
- **Delete Medical Device Report**: Select a medical device report from the list and click "Delete" to remove it from the system.

## Multi-Cabinet Support  
The frontend of the application is designed to work with multiple medical cabinets. This allows users to manage patient records, appointments, and staff information across different medical facilities seamlessly.  

As we manage multiple cabinets, you can also switch patients between different cabinets while preserving their data.  

# Authentication and Authorization

The system uses Keycloak for authentication and authorization. Each user must log in with their credentials to access the system. Depending on their role, users will have access to different features. Keycloak ensures secure and centralized management of user identities and permissions.

# Troubleshooting

If you encounter any issues while using the system, please refer to the following steps:

- **Check Docker Containers**: Ensure all Docker containers are running without errors.
- **Database Migrations**: Verify that all database migrations have been applied successfully.
- **Logs**: Check the application logs for any error messages that can help diagnose the issue.


# Relation Diagram

[![](https://mermaid.ink/img/pako:eNqtVs1upDAMfhWUc_sCHPaw6j7B9rRCQp7EBbeQICdU7VZ99zUMpJACMxrtZTTj-Ofz58_JfCjtDKpc6Qa8fyCoGNrCGmLUgZzNfj4WtrDjaabhRBZD2aIhDU32Udgsy07ONQg2Awl4xdH0Cqxr4MxCuzYEbFC7dmUDYxi9X_u9d-dAsgEr5IxMYT8jDtd2AX3JaE3vJzj924RnDjHOe0Ke0ZZDCjk2EHD8WDlDH7Dn2SfCoNCsG9BOAmw4wmaDMOETMB0Ekri0AGMDA82-pu6YOWGJBk9p5GZWK-ELeWVyXIGlvyOI_aYmKn0JpiVLPrAEPF3oMRJdasavAs9eVGWc7lvx9VfU3BnvddWWgipBazyo2JB9udDTbHahTog8Vqz0gJrsnD2Ov-v88dh9J3HQUFibsQVqdjUwQ0j2NRVf75FjwU3YU_f-P236Qn_juE7EoS7jLh5JtwWmIC34AKFPjyxUZKtyV8sT--kQL9DzxfEmNx5FaEFgQUim-o2L79OqpbQM9bz7N8_saPYTVkG7c1ne3__Y2LF889o8yhGlnS8v0XgNDi5RRvlqn_ZulWtCVhB2nM_7nDhMm7t5tgyObQ0-6cOXb44pZroxZMHkUrFLoV2fWd2pFlmEZ-RxH_VZKGldlKNy-WqAXwolEhE_GZv7_W61ygP3eKfY9VWt8idovPzqu2FBp38GifWXvEmOo7ED-8e52enzHzZnCF8?type=png)](https://mermaid.live/edit#pako:eNqtVs1upDAMfhWUc_sCHPaw6j7B9rRCQp7EBbeQICdU7VZ99zUMpJACMxrtZTTj-Ofz58_JfCjtDKpc6Qa8fyCoGNrCGmLUgZzNfj4WtrDjaabhRBZD2aIhDU32Udgsy07ONQg2Awl4xdH0Cqxr4MxCuzYEbFC7dmUDYxi9X_u9d-dAsgEr5IxMYT8jDtd2AX3JaE3vJzj924RnDjHOe0Ke0ZZDCjk2EHD8WDlDH7Dn2SfCoNCsG9BOAmw4wmaDMOETMB0Ekri0AGMDA82-pu6YOWGJBk9p5GZWK-ELeWVyXIGlvyOI_aYmKn0JpiVLPrAEPF3oMRJdasavAs9eVGWc7lvx9VfU3BnvddWWgipBazyo2JB9udDTbHahTog8Vqz0gJrsnD2Ov-v88dh9J3HQUFibsQVqdjUwQ0j2NRVf75FjwU3YU_f-P236Qn_juE7EoS7jLh5JtwWmIC34AKFPjyxUZKtyV8sT--kQL9DzxfEmNx5FaEFgQUim-o2L79OqpbQM9bz7N8_saPYTVkG7c1ne3__Y2LF889o8yhGlnS8v0XgNDi5RRvlqn_ZulWtCVhB2nM_7nDhMm7t5tgyObQ0-6cOXb44pZroxZMHkUrFLoV2fWd2pFlmEZ-RxH_VZKGldlKNy-WqAXwolEhE_GZv7_W61ygP3eKfY9VWt8idovPzqu2FBp38GifWXvEmOo7ED-8e52enzHzZnCF8)



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

## Sources d'inspiration

- [Frontend](https://github.com/sagnik26/Clinic-Management-System-frontend)




