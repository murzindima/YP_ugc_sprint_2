# Sprint 9

[![CI](https://github.com/IlyasDevelopment/ugc_sprint_2/actions/workflows/github-actions.yml/badge.svg)](https://github.com/IlyasDevelopment/ugc_sprint_2/actions/workflows/github-actions.yml)

## Repository Link

https://github.com/IlyasDevelopment/ugc_sprint_2

## Description

The project is a monorepo with multiple services. 
The services are:

- auth api service
- movie api service
- admin panel service
- redis
- postgres (one for auth and one for movie)
- elasticsearch
- jaeger
- ETL service
- UGC service (for analytics)
- UGC operations service
- NGINX

The infrastructure is set up using Docker Compose:

```bash
docker-compose up --build
```

All ports but NGINX are not exposed to the host. The services are only accessible through the NGINX proxy.
Configuration made by .env files. Each service has its own .env file in the root of the service directory.

## About the repo structure

admin_panel_service is a Django admin panel service.
auth_api_service is a FastAPI service for authentication and authorization.
content_api_service is a FastAPI service for movies.
postgres_to_elasticsearch is a Python service that listens to the Postgres database and indexes the data in Elasticsearch.
nginx is the NGINX proxy.

so, you can find the .env.example file in auth_api_service, content_api_service, and admin_panel_service.

About the NGINX hosts. The NGINX is set up to listen to the following hosts:

- admin-panel
- auth-api
- content-delivery-api
- jaeger-ui
- ugc
- ugc-operations

You must add the following line to your /etc/hosts file:

```bash
127.0.0.1 admin-panel auth-api content-delivery-api jaeger-ui ugc ugc-operations
```

The services are accessible through the following URLs:

- admin-panel: http://admin-panel:8080/admin/
- auth-api: http://auth-api:8080/api/openapi
- content-delivery-api: http://content-delivery-api:8080/api/openapi
- jaeger-ui: http://jaeger-ui:8080/
- ugc: http://ugc:8080/api/openapi
- ugc-operations http://ugc-operations:8080/api/openapi

## How to prepare the databases

The databases are created automatically. But you must create tables and so on manually.

To create the tables for the auth service, you must run the following command:

```bash
docker exec -it auth_service_spr9 alembic upgrade head
docker exec -it auth_service_spr9 python src/tools/init_db.py create-permissions
docker exec -it auth_service_spr9 python src/tools/init_db.py create-roles
docker exec -it auth_service_spr9 python src/tools/init_db.py assign-permissions-to-roles
docker exec -it auth_service_spr9 python src/tools/init_db.py create-admin a@b.com 123qwe Joe Doe
```

To create the tables for the content service, you must run the following command:

```bash
docker exec -it ugc_sprint_2-admin-panel-service-1 python manage.py migrate movies 0001 --fake
docker exec -it ugc_sprint_2-admin-panel-service-1 python manage.py migrate movies 0002
docker exec -it ugc_sprint_2-admin-panel-service-1 python manage.py migrate
```

After that ETL service will start indexing the data in Elasticsearch.

## About the authorization and authentication

Django and movies API are authenticated by the auth service. 
So, you must create a user in the auth service to access the admin panel and the movies API.

You can create a local user or use the OAuth2 flow to get the access and refresh tokens.
