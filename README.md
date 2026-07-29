# Recipe & Meal Planner

A full-stack recipe and meal planning app. Users can register, create and browse recipes, track exact ingredient quantities per recipe, and manage their own content. Admins manage the shared ingredient catalogue and can moderate any recipe.

Built as a capstone project demonstrating relational data modeling (1:1, 1:many, many:many), JWT authentication with role-based authorization, paginated and deeply-queried REST endpoints, and a React frontend consuming the API with custom hooks.

## Tech Stack

**Backend:** Flask, Flask-RESTful, Flask-SQLAlchemy, Flask-Migrate, Flask-JWT-Extended, PostgreSQL, sqlalchemy-serializer

**Frontend:** React (Vite), React Router, fetch API

## Project Structure

```
recipe-planner/
├── backend/
│   ├── models/          # SQLAlchemy models (User, Settings, Recipe, Ingredient, RecipeIngredient)
│   ├── controllers/     # Flask-RESTful resources (auth, recipe, ingredient, deep queries)
│   ├── migrations/       # Flask-Migrate schema history
│   ├── main.py           # App factory, route registration
│   ├── config.py         # Environment-based configuration
│   ├── extensions.py     # Shared extension instances (db, migrate, jwt, api)
│   └── seed.py           # Seed script with Faker-generated data
└── frontend/
    └── src/
        ├── components/    # Navbar, ProtectedRoute
        ├── pages/         # Login, Register, RecipeList, RecipeDetail, RecipeForm
        ├── hooks/         # useAuth, useFetch
        └── context/       # AuthContext
```

## Data Model

| Relationship | Entities | Notes |
|---|---|---|
| 1:1 | User ↔ Settings | Each user has exactly one settings record (dietary preference, unit system) |
| 1:many | User → Recipe | A user authors many recipes; each recipe has one author |
| many:many | Recipe ↔ Ingredient | Via `RecipeIngredient`, which carries `quantity` and `unit` as an association object |

## Setup

### Prerequisites
- Python 3.12+
- Node.js 20+ (LTS)
- PostgreSQL

### 1. Database

```bash
sudo -u postgres psql
```
```sql
CREATE USER recipe_user WITH PASSWORD 'recipe_pass';
CREATE DATABASE recipe_planner OWNER recipe_user;
\q
```

### 2. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create `backend/.env`:
```
FLASK_APP=main.py
DATABASE_URI=postgresql://recipe_user:recipe_pass@localhost:5432/recipe_planner
JWT_SECRET_KEY=change-this-to-something-random
SECRET_KEY=change-this-too
```

Run migrations and seed the database:
```bash
export FLASK_APP=main.py
flask db upgrade
python seed.py
```

Start the server:
```bash
python3 main.py
```
Backend runs at `http://localhost:5000`.

**Seeded accounts** (all created by `seed.py`):

| Username | Password | Role |
|---|---|---|
| `admin` | `admin123` | admin |
| any Faker-generated username (see `SELECT username FROM users;`) | `password123` | user |

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```
Frontend runs at `http://localhost:5173`.

## API Routes

| Method | Route | Auth | Description |
|---|---|---|---|
| POST | `/register` | — | Create a new user account, returns JWT |
| POST | `/login` | — | Log in, returns JWT |
| GET | `/me` | JWT required | Returns current user's id and role |
| GET | `/admin/ping` | Admin only | Test route proving role-based authorization |
| GET | `/recipes?page=&per_page=` | — | Paginated list of all recipes |
| POST | `/recipes` | JWT required | Create a recipe with ingredients |
| GET | `/recipes/<id>` | — | Get one recipe |
| PATCH | `/recipes/<id>` | Owner or admin | Update a recipe |
| DELETE | `/recipes/<id>` | Owner or admin | Delete a recipe |
| GET | `/ingredients?page=&per_page=` | — | Paginated list of ingredients |
| POST | `/ingredients` | Admin only | Add a new ingredient |
| GET | `/ingredients/<id>` | — | Get one ingredient |
| PATCH | `/ingredients/<id>` | Admin only | Update an ingredient |
| DELETE | `/ingredients/<id>` | Admin only | Delete an ingredient |
| GET | `/recipes/search?ingredient=` | — | Deep query: recipes filtered by ingredient name |
| GET | `/ingredients/most-used?limit=` | — | Deep query: ingredient usage counts, aggregated and ranked |
| GET | `/users/stats?min_recipes=` | — | Deep query: recipe count and average prep time per user |

## Mandatory Feature Checklist

- [x] JWT authentication + role-based authorization (user/admin)
- [x] All three relationship types (1:1, 1:many, many:many with association object)
- [x] Pagination with metadata on all list endpoints
- [x] Frontend: fetch + custom hooks (`useAuth`, `useFetch`), full CRUD, loading/error/success states, protected routes
- [x] Deep querying: filtering across relationships, aggregation with `func.count`/`func.avg`, joins
- [x] Migrations via Flask-Migrate, seed script covering every table