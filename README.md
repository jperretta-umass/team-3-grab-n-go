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

    
    #runing linter:

        black --check .
        isort --check-only .
        pycodestyle .
        pyright

    #Running pytest 
        docker run -d  -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -p 9003:5432 postgres:16
        DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:9003/postgres pytest -vv

    Frontend (Vite)
```Frontend 
    cd frontend

    npm ci

    npm run dev -- --host 0.0.0.0 --port 5173

```

should be accessable at 
http://localhost:5173

To view API docs: 
http://localhost:8000/docs while the docker stack is running.
# Running Dev Stack

    ```docker compose up --build backend #rebuilds one service entirely```
    In the browser visit localhost:80 to visit the running site.
    
    docker Compose Commands(Most useful once everything is approved on PRs)
    docker compose up --build # builds whole app 
    docker compose up [WHICH THING YOU WANT RUNNING] # This will start just one container call can be made once to start multiple containers eg. 
    "docker compose up backend db"
    would start the backend and database containers respectively.
    docker compose down #stops everything 
    docker compose stop [thing] # stops the specifc container
    docker compose restart [thing] #stops then starts container you want 

    Other Docker Commands that may be useful: 
    docker ps #lists running containers
    docker ps # all containers 
    docker logs -f backend #follows logs 
    docker exec -it backend bash #shell into container 
    docker stop backend #stops container (backend used as example)
    docker rm backend #removes container (backend used as example)

    docker images # lists docker images
    docker network ls #networks 


##Payment Integration (Stripe)
1. Initial Stripe Setup
- Create a Stripe Account: Sign up at Stripe.com and stay in Test Mode.
- Install Stripe CLI:
    Mac: brew install stripe/stripe-cli/stripe

    Windows/Linux: Download from the Stripe GitHub.

    Login: Open your terminal and run stripe login. Follow the browser instructions to authenticate.

2. Create Local Secrets
Docker Compose looks for secrets in a ./secrets folder at the project root. You MUST CREATE this folder and the following two files:

./secrets/stripe_secret_key.txt:

Go to your Stripe Dashboard -> Developers -> API Keys.

Copy the Secret key (starts with sk_test_). ONLY PASTE THE KEY ITSELF INTO THE FILE, NOT THE "STRIPE_SECRET_KEY=" PART.
SO IT MUST START WITH : sk_test...

Paste it into this file.

./secrets/stripe_webhook_secret.txt:

Open a terminal and run: stripe listen --forward-to localhost/api/payments/webhook

The terminal will output: Ready! Your webhook signing secret is whsec_...

Copy that whsec_ string and paste it into this file. AGAIN DO NOT PREFIX THIS WITH ANYTHING JUST SIMPLY COPY PASTE.

3. Running with Payments
Once your secrets are in place, the stripe-tunnel service in Docker will automatically handle the connection.

Bash
# Start the full stack
docker compose up --build
How to test the flow:

Go to http://localhost/ItemPage and add items to your cart.

Click Checkout. You will be redirected to a Stripe-hosted page.

USE TEH TEST CARD: 4242 4242 4242 4242 (any future expiry and any CVC).

Upon success, you'll be redirected to http://localhost/success.

Check http://localhost/DelivererPage to verify the order was moved from the Cart to the Orders table.

Note: Every time you stop and restart your Stripe listener, the whsec_ key MIGHT change. If payments stop populating in the DB, check if you need to update your stripe_webhook_secret.txt.