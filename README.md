# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.8+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

You can check poetry is installed by running `poetry --version` from a terminal.

**Please note that after installing poetry you may need to restart VSCode and any terminals you are running before poetry will be recognised.**

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/2.3.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.


## Setting up Trello Integration 

This app uses trello API for storing the todo items

Set up trello account

Set up trello board 

Create API key and token

Update env file to include details

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app 'todo_app/app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 113-666-066
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.


## Testing

Pytest is used to test functionality

To run all tests , run `poetry run python3 -m pytest`
To run individual tests, run `poetry run python3 -m pytests <testfile>`

## Deploying application to machine with ansible

To deploy the application:
Copy the ansible folder to the host node
Update the inventory file with the control nodes to deploy to
Run the following command:
    ansible-playbook playbook.yaml -i inventory.yaml

## Deploying application using docker

To create a development sever which allows for flasks detailed logging and rapid changes:

```bash
docker build --target development --tag todo-app:dev .
docker run -dit --env-file .env --publish 8000:5000 --mount "type=bind,source=$(pwd)/todo_app,target=/todo-app/todo_app" todo-app:dev
```

This will run on localhost:8000

To create a production server:

```bash
docker build --target production --tag todo-app:prod .
docker run -dit --env-file .env --publish 8100:5100 todo-app:prod
```

This will run on localhost:8100


To run the unit and integration tests using docker: 

```bash
docker build --target test --tag todo-app:test .
docker run todo-app:test
```

## Uploading production docker image to container registery

Log into docker, then build and push the image
(add --platform if on mac)

```bash
docker login
docker build --platform=linux/amd64 --target production --tag agib1/todo-app:prod .
docker push agib1/todo-app:prod
```

You can find this here: https://hub.docker.com/repository/docker/agib1/todo-app/general


## To deploy the container to azure manually

Create an app service plan and a web app through azure cli

```bash
az appservice plan create --resource-group <resource_group_name> -n <appservice_plan_name> --sku B1 --is-linux
az webapp create --resource-group <resource_group_name> --plan <appservice_plan_name> --name <webapp_name> --deployment-container-image-name docker.io/agib1/todo-app:prod
```

You can find this here: https://wa-ag-todoapp.azurewebsites.net/

To manually redeploy, send a request to the webhook using the <webhook_url> for the webapp found in the azure portal under deployment center

```bash
curl -X POST '<webhook_url>'
```

