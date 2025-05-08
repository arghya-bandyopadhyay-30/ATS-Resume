# GO TO PROJECT ROOT DIR
>> docker-compose -f .\docker\docker-compose.yml up -d

# Go to project root directory to stop containers
>> docker-compose -f .\docker\docker-compose.yml down

# Go to project root directory to spin specific container
>> docker build -t containername . -f .\docker\filename.Dockerfile


################################################################################3



### Step-by-Step Command Sequence



1. Stop and Remove Existing Containers:
   ```bash
   docker-compose -f .\docker\docker-compose.yml down
   ```
   - This stops and removes all containers, networks, and volumes defined in the `docker-compose.yml` file.



2. Take Pull from respective branch [ development/production ]



3. Rebuild Containers:
   ```bash
   docker-compose -f .\docker\docker-compose.yml build --no-cache
   ```
   - `--no-cache`: Ensures the images are built without using any cached layers.



4. Start the Containers:
   ```bash
   docker-compose -f .\docker\docker-compose.yml up -d
   ```
   - `-d`: Runs the containers in detached mode (in the background).



---



### Explanation of Commands
1. `docker-compose down`:
   - Stops all running containers and removes them along with their associated networks and volumes.



2. `docker-compose build --no-cache`:
   - Rebuilds the container images from scratch, ignoring previously cached layers.



3. `docker-compose up -d`:
   - Starts the services as defined in the `docker-compose.yml` file in detached mode.



---
migrate tables for the first time

    go to docker tunnel-backend
    go to exec 
    >> cd src/backend
    >> python manage.py makemigrations <<table-names>>
    >> python manage.py migrate
    >> python manage.py createsuperuser

---
rever migration in case required due to conflicts

    >> find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
    >> find . -path "*/migrations/*.pyc" -delete