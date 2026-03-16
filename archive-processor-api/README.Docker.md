### Building and Running for Development

When you are ready, start your application by running:
`docker compose up --build`

Your FastAPI application will be available at http://localhost:8000.

**Live Reload Enabled:** The `compose.yaml` is configured to map your local directory to the container and run Uvicorn with the `--reload` flag. Any changes you make to the Python files in the `app/` directory will automatically restart the server inside the container.

### Stopping the Application

To stop the running container, press `Ctrl+C` in your terminal. 

To completely remove the containers and the internal network, run:
`docker compose down`

### Deploying your application to the cloud

First, build your production image without the development overrides: 
`docker build -t archive-processor-api .`

If your cloud uses a different CPU architecture than your development machine (e.g., you are on a Mac M1 and your cloud provider is amd64), you will want to build the image for that platform:
`docker build --platform=linux/amd64 -t archive-processor-api .`

Then, push it to your registry: 
`docker push myregistry.com/archive-processor-api`

Consult Docker's [getting started](https://docs.docker.com/go/get-started-sharing/) docs for more detail on building and pushing.

### References
* [Docker's Python guide](https://docs.docker.com/language/python/)
* [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/docker/)