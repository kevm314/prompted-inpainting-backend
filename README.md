# prompted-inpainting-backend

## Rapid prototyping (dev)

- while in the `app/` directory run the fastAPI server using the `python main.py` command ensuring to have an appropriate environment with the requirements packages installed. This command will 
automatically use the `dev.env` file. 

## Running using docker (dev - dockerfile currently overfitted to aws lambda build)

- run `docker build -f backend.dockerfile -t inpainting-backend .` while in the `app/` directory to build the project backend docker image
- run `docker compose up` to start up the backend service for debugging
- to attach to the running container for debugging purposes
    - run `docker compose up -d` to start the container in detached mode
    - run `docker exec -it prompted-inpainting-backend-backend-1 bash` to start a bash session

## Production deployment (prod)

Note that the AWS lambda production deployment involves a custom docker image (based off of a AWS lambda python image). This makes it
more convenient to install custom libraries/packages but has the downside of needing aws ECR for image storage. The built image is also
constrained to running the aws lambda handler comand instead of the default uvicorn server command. From the root of the project:

- run `sam validate` to validate the AWS SAM template file
- run `sam build` to build the AWS lambda image based function
- run `sam local start-api --debug --host 127.0.0.8 --port 8000 --env-vars app/prod_env.json` to run the AWS lambda function locally before pushing to production
- run `sam deploy --guided` to perform a guided deployment of the build (with the build command being performed first - exclude `--guided` to perform without prompts)

## ML endpoint deployment

- the Stable diffusion 2 model is used out of the box via the hugginface inference endpoints service (using the below repo):
  - https://huggingface.co/philschmid/stable-diffusion-2-inpainting-endpoint

## Project - lessons learnt

- AWS SAM can build a serverless lambda function using a zip file or docker image -> a custom docker image allows more flexibility in installing 3rd party libraries in a known environment (e.g. benefit of using docker)
  - ensure to have the correct function handler path into the docker image (i.e. ensure to mount correct path)
  - always run the local debug api start before deploying the lambda function to ensure correct operation
- AWS gateway API needs CORS enabled if resource access from frontend/service that is hosted from another origin
  - ensure to enable the correct domain names in the allowed CORS values of the relevant backend (in this case python fastAPI)