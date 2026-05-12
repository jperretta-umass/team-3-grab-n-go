# Minute Meals

Grab and Go delivered by students for students on the UMass Amherst campus.

## Tech Stack

- Backend: FastAPI, Uvicorn, SQLAlchemy, PostgreSQL
- Frontend: Vue 3, TypeScript, Vite, Vue Router, Tailwind CSS
- Payments: Stripe Checkout and Stripe webhooks
- Testing: Pytest, Vitest, Playwright
- Infrastructure: Docker Compose, Nginx

## Project Structure

```text
team-3-grab-n-go/
├── backend/              # FastAPI app, database models, routers, and backend tests
├── frontend/             # Vue/Vite frontend app, routes, components, and unit tests
├── end2endTest/          # Playwright end-to-end tests
├── nginx/                # Local Nginx reverse proxy configuration
├── secrets/              # Local Stripe secret files; do not commit real secrets
├── docker-compose.yml    # Main local development Docker stack
├── docker-compose.test.yml
├── .env                  # Local development environment variables
├── .env.test             # Test environment variables
└── README.md
```

## Authors

Team 3 of CS320 at UMass Amherst, Spring 2026.

- Manager: Dr. Perretta
- Team: Ayman Blanco, Alex Murdock, Colin Kirn, Grace Huang, Gruia Pascale, Isabelle Neves, Rama Bachimanchi, Samuel Parkin

## Prerequisites

Install these before running the app locally:

- Docker
- Docker Compose
- Python 3.14 for backend-only development
- Node.js and npm for frontend-only development
- Stripe CLI for local payment testing

## Environment Setup

Create a `.env` file in the project root:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=myapp
DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/myapp
AUTH_SECRET_KEY=replace-this-for-local-dev
```

For Stripe, create these files locally:

```text
secrets/stripe_secret_key.txt
secrets/stripe_webhook_secret.txt
```

Each file should contain only the secret value, with no variable name prefix.

## Running the App

Start the full app:

```sh
docker compose up --build
```

Open the app:

```text
http://localhost
```

Useful local URLs:

```text
Frontend through Nginx: http://localhost
Backend API docs:       http://localhost:8000/docs
Backend health check:   http://localhost:8000/health
Vite dev server:        http://localhost:5173
```

Stop the stack:

```sh
docker compose down
```

Reset local database data:

```sh
docker compose down -v
docker compose up --build
```

## Demo Accounts

Seed data is created when the backend starts.

```text
Customer:
email: demo_customer@example.com
password: string3214

Deliverer:
email: demo_deliverer@example.com
password: string3214
```

## Frontend Routes

```text
/Login
/Register
/CustomerLanding
/DelivererLanding
/DelivererPage
/ItemPage
/success
/UserProfile
```

## Backend API Overview

Auth:

```text
POST /auth/register
POST /auth/login
GET  /auth/me
POST /auth/change-password
```

Menus:

```text
GET /api/menu-items
GET /api/menu-items?hall=Worcester
GET /api/dining-menu?hall=worcester
GET /api/dining-menu?hall=worcester&date=05/12/2026
```

Customer cart and orders:

```text
GET    /api/customers/{user_id}/profile
GET    /api/customers/{user_id}/cart
POST   /api/customers/{user_id}/cart/items
PUT    /api/customers/{user_id}/cart/items/{menu_item_id}
DELETE /api/customers/{user_id}/cart/items/{menu_item_id}
GET    /api/customers/{user_id}/orders
POST   /api/customers/{user_id}/orders
```

Deliverer/orders:

```text
GET   /api/orders
POST  /api/orders/claim/{order_id}
PATCH /api/orders/{order_id}/status
```

Payments:

```text
POST /api/payments/create-checkout-session
POST /api/payments/webhook
```

Full generated API documentation is available at:

```text
http://localhost:8000/docs
```

## Backend Development

Create and activate a backend virtual environment:

```sh
cd backend
python -m venv .venv
source .venv/bin/activate
pip install pip-tools
pip-sync requirements.txt requirements-dev.txt
```

Run the backend locally:

```sh
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Run backend checks:

```sh
cd backend
./lint.sh
pytest -vv
```

## Frontend Development

Run the frontend locally:

```sh
cd frontend
npm ci
npm run dev -- --host 0.0.0.0 --port 5173
```

Run frontend checks:

```sh
cd frontend
npm run lint
npm run test
npm run build
```

## End-to-End Tests

Run Playwright end-to-end tests:

```sh
cd end2endTest
npm ci
npm run test
```

Run plain Playwright:

```sh
npm run test:plain
```

Open the Playwright UI:

```sh
npm run test:ui
```

## Payment Integration

### Initial Stripe Setup

Create a Stripe account at Stripe.com and stay in test mode.

Install the Stripe CLI:

```sh
# macOS
brew install stripe/stripe-cli/stripe
```

For Windows and Linux, download the Stripe CLI from the Stripe GitHub page.

Log in:

```sh
stripe login
```

### Create Local Secrets

Docker Compose looks for secrets in a `secrets` folder at the project root. Create these two files:

```text
secrets/stripe_secret_key.txt
secrets/stripe_webhook_secret.txt
```

For `secrets/stripe_secret_key.txt`, copy your Stripe test secret key from the Stripe Dashboard. The value should start with `sk_test_`.

For `secrets/stripe_webhook_secret.txt`, run:

```sh
stripe listen --forward-to localhost/api/payments/webhook
```

Copy the webhook signing secret from the terminal output. The value should start with `whsec_`.

### Test the Payment Flow

Start the full stack:

```sh
docker compose up --build
```

Then:

1. Go to `http://localhost/ItemPage`.
2. Add items to your cart.
3. Click Checkout.
4. Use the Stripe test card `4242 4242 4242 4242` with any future expiration date and any CVC.
5. After success, you should be redirected to `http://localhost/success`.
6. Check `http://localhost/DelivererPage` to verify the order moved from the cart to the orders table.

If payments stop populating the database, check whether `secrets/stripe_webhook_secret.txt` needs to be updated.

## Troubleshooting

If the app fails to start, check whether ports `80`, `8000`, or `5173` are already in use.

If database data looks stale, reset the Docker volume:

```sh
docker compose down -v
docker compose up --build
```

If Stripe checkout succeeds but no order appears, check:

- `secrets/stripe_secret_key.txt`
- `secrets/stripe_webhook_secret.txt`
- `stripe-tunnel` container logs
- `backend` container logs

If the frontend cannot reach the backend, prefer opening the app through `http://localhost` instead of the raw Vite URL.
