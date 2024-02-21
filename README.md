## Starting the server 
To start the FastAPI and MongoDB containers, run
```
docker compose up -d --build
```

## Paths
|`path`|Description|
|-|-|
|`http://localhost:3000/docs`|Swagger UI|
|`http://localhost:3000/openapi.json`|OpenAPI JSON Documentation|

## Assumptions
1. To enable ease of testing (spinning up the containers using only docker compose) db connection string is written within the service file which would otherwise be written in an environment variable.
2. Persistent volume for MongoDB has been attached given the assumption that the service is to be used for production.
3. Directory has been set up using a structure that allows for extensibility. Segregating default paths such as `/`, `/metrics`, `/health` endpoints from `/v1/*` service paths that are more prone to changes.
4. Graceful shutdown and Access Logs is ensured using the feature implemented in [Uvicorn](https://www.uvicorn.org/server-behavior/)