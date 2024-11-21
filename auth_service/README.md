# Auth Service

## Description

Auth Service is a FastAPI-based service
designed to provide secure and efficient authentication and authorization solutions.
It simplifies user management and secures access using JWT tokens,
backed by a robust PostgreSQL database and Redis for caching.

## Features

* User authentication (signup, login, logout)
* JWT-based access and refresh tokens 
* Role-based access control 
* In-memory caching with Redis 
* Persistent storage with PostgreSQL

## Tech Stack

* Framework: FastAPI
* Migration: Alembic
* Database: PostgreSQL, Redis
* Containerization: Docker

## Getting Started

### Prerequisites

* Git
* Docker
* Docker Compose

### Installation

#### Clone the repository

```shell
git clone https://github.com/murzindima/Auth_sprint_1.git
```

#### Poetry

This project uses Poetry for managing its dependencies and packaging.
Poetry provides an easy way to declare, manage, and install dependencies,
ensuring consistent environments and simplifying the process of publishing the project.

##### Installation
If you don't have Poetry installed,
you can install it with the following command (see the official documentation for more details):

```shell
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

##### Install dependencies
With Poetry installed, run the following command in the project root directory to install the project dependencies:

```shell
poetry install
```

##### Activate the virtual environment
To activate the virtual environment, use:

```shell
poetry shell
```

##### Running the application
Once the dependencies are installed, you can run the application using:

```shell
poetry run uvicorn app.main:app --reload
```

##### Adding new dependencies
To add a new dependency to the project, use:

```shell
poetry add [package-name]
```
This will update your pyproject.toml and poetry.lock files accordingly.

##### Updating dependencies
To update all dependencies to their latest versions, use:

```shell
poetry update
```

#### Environment setup

Create a .env file in the project root.

##### Environment variables:

###### Application Settings

* APP_LOG_LEVEL
  * Define the logging level of the application. 
  * Default value: "INFO"
* APP_PROJECT_NAME 
  * Specify the name of the application.
  * Default value: "Auth Service"
* APP_AUTHJWT_SECRET_KEY
  * The secret key used for encoding JWT tokens.
  * Default value: "secretsecret"
* APP_AUTHJWT_DENYLIST_ENABLED
  * Indicates whether JWT revocation is enabled.
  * Default value: True
* APP_AUTHJWT_DENYLIST_TOKEN_CHECKS
  * Specify the type of tokens to check against the denylist.
  * Default value: {"access"}
* APP_ACCESS_TOKEN_EXPIRES
  * The expiration time for access tokens in seconds.
  * Default value: 900 (15 minutes)
* APP_REFRESH_TOKEN_EXPIRES
  * The expiration time for refresh tokens in seconds.
  * Default value: 2592000 (30 days)

###### Postgres Settings

* POSTGRES_DB
  * The name of the PostgreSQL database.
  * Default value: "auth_database"
* POSTGRES_USER
  * Username for accessing the PostgreSQL database.
  * Default value: "app"
* POSTGRES_PASSWORD
  * Password for the PostgreSQL database user.
  * Default value: "pass"
* POSTGRES_HOST
  * Hostname or IP address where the PostgreSQL server is running.
  * Default value: "localhost"
* POSTGRES_PORT
  * Port number on which the PostgreSQL server is listening to.
  * Default value: 5432

###### Redis Settings

* REDIS_HOST
  * Hostname or IP address of the Redis server.
  * Default value: "localhost"
* REDIS_PORT
  * Port number on which the Redis server is listening to.
  * Default value: 6379
* REDIS_DB
  * Redis database number.
  * Default value: 0

### Running the application

#### Start the services with Docker Compose

```shell
docker-compose up -d
```

This command will set up and run the following services:
* PostgreSQL (postgres)
* Redis (redis)
* FastAPI application (api)

#### Accessing the application

The API will be accessible at http://localhost:8000/

Swagger UI for API documentation can be found at 
* http://localhost:8000/api/openapi
* http://localhost:8000/redoc

### Testing

```shell
docker-compose -f docker-compose.tests.yaml up --build --abort-on-container-exit
```

This command will set up and run the following services:
* PostgreSQL (postgres)
* Redis (redis)
* FastAPI application (api)
* Test runner (tests)

## API endpoints

The auth service exposes several RESTful endpoints under /api/v1/ for user authentication,
role and permission management, and user details.

### Authentication endpoints
#### POST /api/v1/auth/signup
* Registers a new user.
* Body: User details including email, password, first name, last name, and role ID.
* Response: Details of the created user.
#### POST /api/v1/auth/login
* Authenticates a user and returns access and refresh tokens.
* Body: User credentials (email and password).
* Response: A pair of JWT tokens (access and refresh).
#### POST /api/v1/auth/logout
* Logs out the user and invalidates the current access token.
* Body: None (token provided in the header).
* Response: Confirmation of logout.
#### POST /api/v1/auth/refresh-tokens
* Refresh the user's access and refresh tokens.
* Body: Refresh token.
* Response: A new pair of JWT tokens.
### User management endpoints
#### GET /api/v1/users
* Retrieve a list of users.
* Response: Array of user details.
#### GET /api/v1/users/{user_id}
* Retrieve details of a specific user by user ID.
* Parameters: user_id (UUID)
* Response: User details.
#### PATCH /api/v1/users/{user_id}
* Updates details of a specific user by user ID.
* Parameters: user_id (UUID)
* Body: User details to update.
* Response: Updated user details.
#### GET /api/v1/users/{user_id}/login-history
* Retrieve the login history of a specific user.
* Parameters: user_id (UUID)
* Response: Array of login history records.
### Permission management endpoints
#### GET /api/v1/permissions
* Retrieve a list of all permissions.
* Response: Array of permissions.
#### POST /api/v1/permissions
* Create a new permission.
* Body: Permission details (name).
* Response: Details of the created permission.
#### GET /api/v1/permissions/{permission_id}
* Fetches details of a specific permission by its ID.
* Parameters: permission_id (UUID)
* Response: Details of the specified permission.
#### DELETE /api/v1/permissions/{permission_id}
* Deletes a specific permission by its ID.
* Parameters: permission_id (UUID)
* Response: Confirmation of deletion.
#### PATCH /api/v1/permissions/{permission_id}
* Updates details of a specific permission.
* Parameters: permission_id (UUID)
* Body: Updated permission details.
* Response: Details of the updated permission.
### Role management endpoints
#### GET /api/v1/roles
* Retrieve a list of all roles.
* Response: Array of roles.
#### POST /api/v1/roles
* Creates a new role.
* Body: Role details (name and description).
* Response: Details of the created role.
#### GET /api/v1/roles/{role_id}
* Fetches details of a specific role by its ID.
* Parameters: role_id (UUID)
* Response: Details of the specified role.
#### DELETE /api/v1/roles/{role_id}
* Deletes a specific role by its ID.
* Parameters: role_id (UUID)
* Response: Confirmation of deletion.
#### PATCH /api/v1/roles/{role_id}
* Updates details of a specific role.
* Parameters: role_id (UUID)
* Body: Updated role details (name and description).
* Response: Details of the updated role.

## Managing database migrations with Alembic

### Overview
This project uses Alembic for database schema migrations.
Alembic provides a robust system
to evolve the database schema over time in a way that allows for modifications to be made without losing data.
It's essential for applying, reverting, and managing changes to the database schema.

### Initial setup
Ensure you have Alembic installed. If not, install it using pip:

```shell
pip install alembic
```

### Creating migrations
Whenever you modify your SQLAlchemy models,
you'll need to create a new migration to reflect those changes in the database:

### Generate a new migration file:

```shell
alembic revision --autogenerate -m "Description of your changes"
```

This command will create a new script in the alembic/versions directory containing the changes.
Review the generated script to ensure the changes match your expectations.

### Applying migrations
To apply the latest migrations to your database, execute:

```shell
alembic upgrade head
```

This command will apply all new migrations up to the latest ('head').

### Reverting Migrations
If you need to undo the latest migration, you can use:

```shell
alembic downgrade -1
```

Be cautious with this command in a production environment as it can lead to data loss.

### Notes
* It's crucial to review the autogenerated migration scripts for accuracy.
* Keep your migration scripts under version control.
* Never modify a migration script after it has been applied to a production database.

### Initial migration
The migration sets up the initial database schema including tables for permissions,
roles, role-permissions associations, users, and user login histories.

#### Database structure
##### Permissions table
* id: UUID, primary key, unique.
* name: String (100 characters), represents the name of the permission, unique.
##### Roles table
* id: UUID, primary key, unique.
* name: Enum, represents role types (ADMIN, MODERATOR, MEMBER, SUBSCRIBER), unique.
* description: String (500 characters), a descriptive text for the role, nullable.
##### Role_permissions table
* role_id: UUID, foreign key linked to the roles table, part of the primary key.
* permission_id: UUID, foreign key linked to the permissions table, part of the primary key.
* Unique constraint: (role_id, permission_id), ensures unique combinations of roles and permissions.
##### Users table
* id: UUID, primary key, unique.
* email: String (255 characters), user's email, unique.
* password: String (255 characters), user's hashed password.
* first_name: String (50 characters), user's first name, nullable.
* last_name: String (50 characters), user's last name, nullable.
* created_at: DateTime, the timestamp when the user was created, nullable.
* role_id: UUID, foreign key linked to the roles table.
* is_deleted: Boolean, flag to mark soft deletion of the user, nullable.
##### Login_histories table
* id: UUID, primary key, unique.
* user_id: UUID, foreign key linked to the users table.
* timestamp: DateTime, the timestamp of the login attempt, nullable.
* ip_address: String (50 characters), IP address of the user at login, nullable.
* location: String (255 characters), location of the user at login, nullable.
* os: String (50 characters), operating system of the user's device, nullable.
* browser: String (50 characters), browser used for login, nullable.
* device: String (50 characters), device used for login, nullable.
* refresh_token: String (255 characters), refresh token issued at login.
* is_active: Boolean, flag to mark if the login is active, nullable.

### How to initialize the database
There is a command-line utility developed using Typer and SQLAlchemy ORM.
It's designed to interact with the database to set up initial roles, permissions, and an admin user.

#### Functionality:
* Create predefined permissions.
* Create roles based on the RoleType enum.
* Assign specific permissions to each role.
* Create an initial admin user.
#### Key Functions
##### _create_permissions():
Creates a list of predefined permissions such as viewing or editing user information and login history.
Checks if each permission already exists in the database; if not, it creates and saves the new permission.
##### _create_roles():
Iterates through the RoleType enum (ADMIN, MODERATOR, MEMBER, SUBSCRIBER)
and creates these roles in the database if they don't already exist.
##### _assign_permissions_to_roles():
Assigns specific permissions to each role.
It ensures that each role has the appropriate permissions, like an ADMIN having edit and view permissions,
whereas a MEMBER might only have view permissions.
##### _create_admin(email, password, first_name, last_name):
Creates an admin user with the provided credentials.
Checks if an admin with the given email already exists to avoid duplicates.
Assigns the admin role to the new user.

#### How to run the utility
Each of these functions is wrapped in a Typer command, making them executable from the command line.
* create_permissions: Runs _create_permissions() to set up initial permissions.
* create_roles: Executes _create_roles() to create user roles.
* assign_permissions_to_roles: Invokes _assign_permissions_to_roles() to assign permissions to roles.
* create_admin: Calls _create_admin(email, password, first_name, last_name) to create an admin user.

##### Examples:
```shell
python python src/tools/init_db.py create_roles
python python src/tools/init_db.py create_permissions
python python src/tools/init_db.py assign_permissions_to_roles
python python src/tools/init_db.py create_admin create-admin 'a@b.c' '123qwe' Admin Default
```

## Contributing

We welcome contributions!

Please fork the repository, make your changes, and submit a pull request.

Code style could be found in STYLEGUIDE.md

# License

MIT
