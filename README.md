# prompted-inpainting-backend

## Build

- run `docker build -f backend.dockerfile -t inpainting-backend .` while in the `app/` directory to build the project backend docker image

## Run

- run `docker compose up` to start up the backend service for debugging
- to attach to the running container for debugging purposes
    - run `docker compose up -d` to start the container in detached mode
    - run `docker exec -it prompted-inpainting-backend-backend-1 bash` to start a bash session

## Production deployment

- run `sam build` to build the AWS lambda image based function
- run `sam local start-api --debug` to run the AWS lambda function locally before pushing to production
- run `sam deploy --guided` to perform a guided deployment of the build (with the build command being performed first)