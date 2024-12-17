# Interopérabilité Avancée

## Member's name

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
- View, and delete dispositif reports.

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

## Dispositif Management
- **View Dispositif Report**: Navigate to the "Dispositif" section under a patient's profile to view a list of all dispositif's report for that patient.
- **Delete Dispositif Report**: Select a Dispositif report from the list and click "Delete" to remove it from the system.

## Multi-Cabinet Support  
The frontend of the application is designed to work with multiple medical cabinets. This allows users to manage patient records, appointments, and staff information across different medical facilities seamlessly.  

As we manage multiple cabinets, you can also switch patients between different cabinets while preserving their data.  

# Additional Feature

We utilize an FHIR server. You can access it to [http://localhost:8082](http://localhost:8082).

# Data Simulation at App Launch

At the launch of the application, we create fictitious data. Observations are updated every 2 minutes with new data to mimic real-time updates from medical devices. 

However, some parts of the interface do not work with the simulated data. To ensure full functionality, new data must be created manually using the admin interface.

# Authentication and Authorization

The system uses Keycloak for authentication and authorization. Each user must log in with their credentials to access the system. Depending on their role, users will have access to different features. Keycloak ensures secure and centralized management of user identities and permissions.

# Troubleshooting

If you encounter any issues while using the system, please refer to the following steps:

- **Check Docker Containers**: Ensure all Docker containers are running without errors.
- **Database Migrations**: Verify that all database migrations have been applied successfully.
- **Logs**: Check the application logs for any error messages that can help diagnose the issue.


# Relation Diagram

[![](https://mermaid.ink/img/pako:eNq9V1tv2jAU_iuRn2lVoFCaNwpByigXkXSaJqTITVywltiR41TtoP99JyGQmym065YHSM7F5_g7N3uDXO4RpCMihhSvBA6WTINn0L8zp4btTIyhOejfa5sdOXlMJsmKCI162nyck-849wlmGnYlfSY53ZKCspXGcFAnSuITlwc1OvY8QaKoLv8aZou87f7APWNgTq0z_MuWEGEYnedcHBGhZEQhcSn2qayzSICpf3qbexdd_EgZkU5APOpi3wGXR-PSBud92zSmtvWfA6Dex4owj4icPMSSaI9UyLXjYQUax8IYYEElbDeSWMYqNsMreHG4WGFGf2NJOatvH0CDOLAiaB_DdjizLNNYWFmSP_w4A-Q9OQSnCJNV4ykiCRaOK0jF70IOO9h1SaR2pj-cmFPTshcQ-ZH1b136Zs2mmsfdOADFsj-D2WRuG5azMKbDh09B5PEookSoAlAUw7EksTjqdR0_Kv061eWwHJNlSE1rPrNMgPEj7r9bLof-U1oA_sUzrtfL8fyOn6BKY1Espr0OEdBbHBYHjwquz2WNlUJVWLNSiymbvIRUpMGvcN9JngzF2Z1lLL5DMs7OarOJOZsGWcpJGqhi5RWII59jqQF8saIFMyrPRRXaWMhZsgfV-jlXbSnnl20ekpk8U5co4LGMwcKw-wuzb_9lch2dN2cOlYy-hr4HsykNdvSZtnhvTsdf0Hf2bC7X8Dsanx7mg9nU7g_sL7C9n_XE38GwpuF5MYCJRRONpAK_4sBSnZgZuT7YAAL1wWu7vbjg2_ygoysi-K7m4QTxYc1iaquVK4ewRG-7KVrMZ7RCFEwcmzJ6PhbUiqreftpcqZeVxSvHrb2Z2hFBL-TcCZ3KJD-hCcCpN3VKa1evp-UO5VUWPXYWOmgdi1B9vh8WU-xDHYFDW10y1EABEdDqPLiNpB1giaB1QBEiHV49LH4t0ZK9gRzkBrdemYt0KWLSQILHqzXSn7AfwVccJqMnu83sRULMfnJ--ASXJReT3dUnvQGlIkjfoBekd9qX7avrTrPbvbluttqtTgO9Iv2i2768bd10u-028K5ur1qdtwb6na7avGzddpqt3k3nun3b6_WA9QdVswcF?type=png)](https://mermaid.live/edit#pako:eNq9V1tv2jAU_iuRn2lVoFCaNwpByigXkXSaJqTITVywltiR41TtoP99JyGQmym065YHSM7F5_g7N3uDXO4RpCMihhSvBA6WTINn0L8zp4btTIyhOejfa5sdOXlMJsmKCI162nyck-849wlmGnYlfSY53ZKCspXGcFAnSuITlwc1OvY8QaKoLv8aZou87f7APWNgTq0z_MuWEGEYnedcHBGhZEQhcSn2qayzSICpf3qbexdd_EgZkU5APOpi3wGXR-PSBud92zSmtvWfA6Dex4owj4icPMSSaI9UyLXjYQUax8IYYEElbDeSWMYqNsMreHG4WGFGf2NJOatvH0CDOLAiaB_DdjizLNNYWFmSP_w4A-Q9OQSnCJNV4ykiCRaOK0jF70IOO9h1SaR2pj-cmFPTshcQ-ZH1b136Zs2mmsfdOADFsj-D2WRuG5azMKbDh09B5PEookSoAlAUw7EksTjqdR0_Kv061eWwHJNlSE1rPrNMgPEj7r9bLof-U1oA_sUzrtfL8fyOn6BKY1Espr0OEdBbHBYHjwquz2WNlUJVWLNSiymbvIRUpMGvcN9JngzF2Z1lLL5DMs7OarOJOZsGWcpJGqhi5RWII59jqQF8saIFMyrPRRXaWMhZsgfV-jlXbSnnl20ekpk8U5co4LGMwcKw-wuzb_9lch2dN2cOlYy-hr4HsykNdvSZtnhvTsdf0Hf2bC7X8Dsanx7mg9nU7g_sL7C9n_XE38GwpuF5MYCJRRONpAK_4sBSnZgZuT7YAAL1wWu7vbjg2_ygoysi-K7m4QTxYc1iaquVK4ewRG-7KVrMZ7RCFEwcmzJ6PhbUiqreftpcqZeVxSvHrb2Z2hFBL-TcCZ3KJD-hCcCpN3VKa1evp-UO5VUWPXYWOmgdi1B9vh8WU-xDHYFDW10y1EABEdDqPLiNpB1giaB1QBEiHV49LH4t0ZK9gRzkBrdemYt0KWLSQILHqzXSn7AfwVccJqMnu83sRULMfnJ--ASXJReT3dUnvQGlIkjfoBekd9qX7avrTrPbvbluttqtTgO9Iv2i2768bd10u-028K5ur1qdtwb6na7avGzddpqt3k3nun3b6_WA9QdVswcF)



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




