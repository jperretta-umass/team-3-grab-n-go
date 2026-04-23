# **Minute Meals!**

    Doordash but for Grab and go on Umass campus 

## Tech Stack
    - **Backend:** FastAPI, Uvicorn
    - **Frontend:** Vite
    - **Database:** PostgresSQL 
    - **Containers:** Docker, Docker Compose
    - **Reverse Proxy:** Nginx 

## File Structure 
    Will add full file structure once everything has settled a bit (likely will just autogenerate it using tree)
## Authors
    Team 3 of CS320 @ Umass Amherst Spring 2026: 
    Manager: Dr. Perretta
    Team:  Ayman Blanco, Alex Murdock, Colin Kirn, Grace Huang, Gruia Pascale, Isabelle Neves, Rama Bachimanchi, Samuel Parkin 


## How to install
    Make sure to have installed: 
        -Docker
        -Docker Compose 
        -Python 3.14

    One must create a '.env\ file in the project root. 

    Eg. 
        '''env
        POSTGRES_USER=postgres
        POSTGRES_PASSWORD=postgres
        POSTGRES_DB=myapp
        DATABASE_URL=postgresql://postgress:postgres@db:5432/myapp
        VITE_API_URL=http://localhost:8000
## How to Use
    Once features have started to populate will add doccuentation, so it can be used//understood here. (Ideally they will never need to see this)

    Backend (Start FastAPI + UVIcorn) no one should have to do this once docker is set up, but in case something breaks here's the command sequence to do, also running locally can be faster for rapid prototyping//debugging. 

    ```CommandLine for backend
    cd backend 
    #create environment for the first time
    python -m venv .venv
    source .venv/bin/activate #mac/linux 
    # .venv\Scripts\activate #windows
    pip install pip-tools
    pip-sync requirements.txt requirements-dev.txt

    #run locally 
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

    #if code change is made 
    uvicorn --reload 
    ``` 
    If steps followed correctly should be accessable at 
    https://localhost:8000
    https://localhost:8000/docs

    #runing linter:

        black --check .
        isort --check-only .
        pycodestyle .
        pyright


    Frontend (Vite)
```Frontend 
    cd frontend

    npm install

    npm run dev -- --host 0.0.0.0 --port 5173

```

should be accessable at 
htttps://localhost:5173

# Docker Image Building 
    ```
    docker build -t my-backend ./backend 
    docker build -t my-frontend ./frontend
    ```

    ```
    docker run -d \ 
    -e POSTGRES_USER=postgres \ 
    -e POSTGRES_PASSWORD=postgres \ 
    -e POSTGRES_DB=myapp \ 
    -p 5432:5432 \ 
    postgres:16-alpine
    ```
    Docker Compose Commands(Most useful once everything is approved on PRs)
    docker compose up --build # builds whole app 
    docker compose up [WHICH THING YOU WANT RUNNING] # This will start just one container call can be made once to start multiple containers eg. 
    "docker compose up backend db"
    would start the backend and database containers respectively.
    docker compose down #stops everything 
    docker compose stop [thing] # stops the specifc container
    docker compose restart [thing] #stops then starts container you want 

    docker compose up --build backend #rebuilds one service entirely 

    Other Docker Commands that may be useful: 
    docker ps #lists running containers
    docker ps # all containers 
    docker logs -f backend #follows logs 
    docker exec -it backend bash #shell into container 
    docker stop backend #stops container (backend used as example)
    docker rm backend #removes container (backend used as example)

    docker images # lists docker images
    docker network ls #networks 