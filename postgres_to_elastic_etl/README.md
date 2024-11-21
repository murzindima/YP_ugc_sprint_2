# Overview

The service is designed to fetch data from a PostgreSQL database, 
transform it, and then load it into Elasticsearch for indexing. 
It supports state management through either a JSON file or Redis,
allowing flexibility and persistence across runs.

# Configuration

## PostgreSQL Settings
**POSTGRES_HOST**: Hostname of the PostgreSQL server. Default is "localhost".

**POSTGRES_PORT**: Port number for the PostgreSQL server. Default is 5432.

**POSTGRES_USER**: Username for PostgreSQL authentication.

**POSTGRES_PASSWORD**: Password for PostgreSQL authentication.

**POSTGRES_DBNAME**: Name of the database to connect to.

## Elasticsearch Settings
**ELASTIC_HOST**: Hostname of the Elasticsearch server. Default is `"localhost"".

**ELASTIC_PORT**: Port number for the Elasticsearch server. Default is 9200.

## State Management Settings
STATE_STORAGE: Type of storage to be used for state management. Options are "json" or "redis".

# Running the Service
Ensure that PostgreSQL and Elasticsearch are running and accessible.
Set up the desired configuration parameters in the settings classes.
Start the ETL service. 
It will automatically connect to the specified PostgreSQL and Elasticsearch instances,
and manage state according to the provided settings.

# Customization

You can customize the service by modifying the settings in the respective configuration. 
This includes changing database connection details, Elasticsearch index, 
batch processing size, and the type of state management storage.

# Dependencies

PostgreSQL server (configured as per PostgresSettings).
Elasticsearch server (configured as per ElasticsearchSettings).
Redis server (optional, only if Redis is used for state management).

# Troubleshooting

If you encounter issues, check the log files based on the set log_level.
Ensure all services (PostgreSQL, Elasticsearch, Redis) 
are running and network configurations are correctly set in the service settings.
