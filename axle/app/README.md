# axle Assessment Dashboard


## Running the App locally

Install `requirements.txt` in chosen virtual environment. In the `src` directory run `python app.py` and navigate to http://127.0.0.1:8080/

## Running the App in Docker

Build the image with `docker build -t axle-app -f Dockerfile ../..` and run with `docker run -p 8050:8050 axle-app`. Navigate to http://127.0.0.1:8050/


## Deploying the App to AWS

To deploy on AWS App Runner, first need to push a docker image to ECR. This can be done by running `./build_deploy_silicon.sh` (for Silicon Macs only).

