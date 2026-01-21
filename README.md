# Ecommerce Wagtail

A modern e-commerce platform built with Django (Wagtail CMS) for the backend, Vue.js for the frontend, and Nginx for reverse proxy. The application uses Docker containers for streamlined development and production deployment.

## Project Overview

This repository contains a full-stack e-commerce application with:
- **Backend**: Django with Wagtail CMS, Django Ninja API framework, and PostgreSQL database
- **Frontend**: Vue.js 3 with Vite and TypeScript
- **Proxy**: Nginx reverse proxy for routing and serving static assets

## Project Structure

### Backend (`/backend`)

The backend is a Django application with Wagtail CMS integration for content management and an API-first design using Django Ninja.

**Key Apps:**
- **`accounts/`** - User authentication and authorization
  - Custom user model with profile management
  - User address/shipping information
  - Custom authentication backends (email/username login)
  - Tests for user API endpoints and admin functionality

- **`blog/`** - Blog and content publishing system
  - BlogPostPage model for Wagtail pages
  - BlogIndexPage for listing blog posts
  - Author snippets for blog post attribution
  - Blog tagging system using django-taggit
  - Gallery images for blog posts
  - Headless preview support for frontend integration

- **`store/`** - Product catalog and shopping functionality
  - Product models and management
  - Category organization
  - API endpoints for product browsing

- **`cart/`** - Shopping cart management
  - Cart item tracking
  - API for cart operations (add, remove, update)
  - Cart session management

- **`payments/`** - Payment processing and order management
  - Payment integration
  - Order tracking
  - Transaction management
  - Tests for payment workflows

- **`home/`** - Homepage and landing pages
  - Home page content management via Wagtail
  - Hero sections and featured content

- **`core/`** - Shared utilities and base functionality
  - Utility functions used across apps
  - Management commands
  - Common schemas

- **`app/`** - Django project configuration
  - `settings.py` - Project settings with environment variable support
  - `urls.py` - Main URL routing
  - `wsgi.py` / `asgi.py` - Application entry points
  - `api.py` - Ninja API configuration

**Key Features:**
- Django 6.0 with PostgreSQL
- Wagtail CMS for content management
- Django Ninja for high-performance APIs
- Django Storages for cloud file storage (S3-compatible)
- Email notifications with SMTP integration
- CORS support for cross-origin requests
- Custom authentication backends

**Dependencies:**
- Django & Wagtail ecosystem
- Django Ninja & DRF
- Django REST Framework
- PostgreSQL driver (psycopg2)
- Boto3 for AWS S3 integration
- Email validators and phone number fields
- See `requirements.txt` for complete list

### Frontend (`/frontend`)

A modern Vue.js application with Vite, TypeScript, and Tailwind CSS for styling.

**Structure:**
- **`src/`** - Source code
  - `main.ts` - Application entry point
  - `App.vue` - Root component
  - `components/` - Reusable Vue components
  - `router/` - Vue Router configuration for client-side routing
  - `stores/` - Pinia state management stores
  - `assets/` - Images, fonts, and other static assets
  - `__tests__/` - Unit and integration tests

- **`e2e/`** - End-to-end tests with Playwright
  - Browser automation tests
  - Critical user journey testing

- **`public/`** - Public assets served directly

**Build & Development Tools:**
- Vite for fast development and optimized builds
- Vue 3 with Composition API
- TypeScript for type safety
- Tailwind CSS for styling
- ESLint and Oxlint for code quality
- Prettier for code formatting
- Vitest for unit testing
- Playwright for E2E testing

**Key Dependencies:**
- Vue 3 & Vue Router
- Pinia (state management)
- Tailwind CSS (styling)
- HeadlessUI Vue components
- Motion for animations

### Proxy (`/proxy`)

Nginx reverse proxy that serves the frontend and routes API requests to the backend.

**Configuration (`nginx.conf`):**
- Serves Vue.js frontend from `/` (SPA routing)
- Proxies `/api/` requests to Django backend
- Serves static files from `/files/static/`
- Serves media uploads from `/files/media/`
- Handles CORS headers for cross-origin requests

**Dockerfile Stages:**
- **Stage 1 (Builder)**: Builds the Vue.js frontend in production mode
- **Stage 2 (Runtime)**: Nginx Alpine image serving built frontend and proxying requests

---

## Development Setup

### Prerequisites

- **Docker** and **Docker Compose** (version 3.8+)
- **Git** for version control
- Optional: Python 3.13+, Node.js 20+, and PostgreSQL if running locally without Docker

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ecommerce-wagtail
   ```

2. **Copy environment file**
   ```bash
   cp .env.sample .env
   ```
   Update `.env` with your development settings (defaults are provided).

3. **Build and start containers**
   ```bash
   docker compose build
   docker compose up
   ```

4. **Access the application**
   - **Frontend**: http://localhost (Nginx proxy)
   - **Backend API**: http://localhost/api/
   - **Django Admin**: http://localhost/cms/admin/
   - **Wagtail CMS**: http://localhost/cms/
   - **Postgres DB**: localhost:5432 (if exposed in development)

### Development Workflow

#### Running Services

**Start all services:**
```bash
docker compose up
```

**Start services in background:**
```bash
docker compose up -d
```

**View logs:**
```bash
docker compose logs -f backend      # Backend logs
docker compose logs -f proxy        # Proxy logs
docker compose logs -f db           # Database logs
```

**Stop services:**
```bash
docker compose down
```

**Remove volumes (resets database):**
```bash
docker compose down -v
```

#### Backend Development

**Run migrations:**
```bash
docker compose exec backend python manage.py migrate
```

**Create superuser:**
```bash
docker compose exec backend python manage.py createsuperuser
```

**Collect static files:**
```bash
docker compose exec backend python manage.py collectstatic
```

**Run tests:**
```bash
docker compose exec backend python manage.py test
# or with coverage:
docker compose exec backend coverage run --source='.' manage.py test
docker compose exec backend coverage report
```

**Access Django shell:**
```bash
docker compose exec backend python manage.py shell
```

**Shell script commands:**
```bash
docker compose exec backend sh scripts/run.sh
```

#### Frontend Development

**The frontend runs in development mode** when using the development docker-compose. To work on frontend code:

1. **Access frontend container:**
   ```bash
   docker compose exec proxy sh
   ```

2. **Run frontend dev server** (from proxy container or locally):
   ```bash
   cd frontend && npm run dev
   ```
   Frontend dev server will be available at http://localhost:5173

3. **Build frontend:**
   ```bash
   docker compose exec proxy npm run build
   ```

4. **Run tests:**
   ```bash
   docker compose exec proxy npm run test:unit  # Unit tests with Vitest
   docker compose exec proxy npm run test:e2e   # E2E tests with Playwright
   ```

**Frontend environment variables** (in `frontend/.env`):
- `VITE_API_URL` - Backend API URL (default: `http://localhost:8000`)

#### Database Access

**Connect to PostgreSQL:**
```bash
docker compose exec db psql -U devuser -d devdb
```

**Common commands:**
```sql
\dt                    -- List tables
\d table_name         -- Describe table
SELECT * FROM table;  -- Query data
```

---

## Production Deployment

### Prerequisites for Production

- **Docker** and **Docker Compose** on production server
- **Environment variables** configured in `.env` file
- **Domain name** and SSL certificate (recommended)
- **S3-compatible storage** for media uploads (AWS S3, DigitalOcean Spaces, MinIO, etc.)
- **SMTP email service** for transactional emails
- **PostgreSQL database** (can be containerized or managed service)

### Environment Configuration

Create a `.env` file in the project root with production values:

```bash
# Database Configuration
DB_NAME=production_db
DB_USER=db_user
DB_PASS=strong_password_here
DB_HOST=db              # or external database host

# Django Configuration
DJANGO_SECRET=your-secret-key-here
DJANGO_HOSTS=yourdomain.com,www.yourdomain.com
DEBUG=0

# S3 / Cloud Storage (if using USE_SPACES=1)
SB_KEY=spaces_access_key
SB_NAME=bucket-name
SB_SECRET=spaces_secret_key
SB_ENDPOINT_URL=https://region.digitaloceanspaces.com

# Email Configuration
MAIL_USER=noreply@yourdomain.com
MAIL_PASS=email_password
MAIL_HOST=mail.yourdomain.com
ADMIN_NAMES=Admin User
ADMIN_EMAILS=admin@yourdomain.com

# Gunicorn / Application Server
WORKERS=4              # Number of Gunicorn workers
```

### Production Docker Compose

The production configuration is in `docker-compose.prod.yaml`. It includes:

**Key Differences from Development:**
- Backend runs with **Gunicorn** (production WSGI server) instead of Django dev server
- Frontend is **pre-built** and served via Nginx
- **Health checks** on all services
- **Restart policies** for automatic recovery
- Static files collected and served via Nginx
- No exposed database port
- Environment variables loaded from `.env`

### Deployment Steps

1. **Prepare server and clone repository**
   ```bash
   ssh user@production-server
   cd /opt/ecommerce-wagtail
   git clone <repository-url> .
   ```

2. **Set up environment**
   ```bash
   cp .env.sample .env
   # Edit .env with production values
   nano .env
   ```

3. **Build production containers**
   ```bash
   docker compose -f docker-compose.prod.yaml build
   ```

4. **Start services**
   ```bash
   docker compose -f docker-compose.prod.yaml up -d
   ```

5. **Run migrations and setup**
   ```bash
   docker compose -f docker-compose.prod.yaml exec backend \
     python manage.py migrate

   docker compose -f docker-compose.prod.yaml exec backend \
     python manage.py collectstatic --noinput

   docker compose -f docker-compose.prod.yaml exec backend \
     python manage.py createsuperuser
   ```

6. **Verify services are healthy**
   ```bash
   docker compose -f docker-compose.prod.yaml ps
   ```

### Production Monitoring

**View logs:**
```bash
docker compose -f docker-compose.prod.yaml logs -f backend
docker compose -f docker-compose.prod.yaml logs -f proxy
docker compose -f docker-compose.prod.yaml logs -f db
```

**Check service health:**
```bash
docker compose -f docker-compose.prod.yaml ps
```

**Health endpoints:**
- Backend: `http://yourdomain.com/api/health/` (returns 200 if healthy)
- Proxy: `http://yourdomain.com/` (returns 200 if healthy)
- Database: Checked via `pg_isready` command

### Scaling and Performance

**Increase Gunicorn workers** (in `.env`):
```bash
# For 4 CPU cores, use 4-9 workers
WORKERS=8
```

**Database backups:**
```bash
# Backup database
docker compose -f docker-compose.prod.yaml exec db \
  pg_dump -U $DB_USER -d $DB_NAME > backup.sql

# Restore database
docker compose -f docker-compose.prod.yaml exec -T db \
  psql -U $DB_USER -d $DB_NAME < backup.sql
```

**Update and redeploy:**
```bash
git pull origin main
docker compose -f docker-compose.prod.yaml build
docker compose -f docker-compose.prod.yaml up -d
docker compose -f docker-compose.prod.yaml exec backend \
  python manage.py migrate
```

### SSL/HTTPS Configuration

For HTTPS support, update the Nginx configuration:

1. **Obtain SSL certificate** (Let's Encrypt recommended):
   ```bash
   certbot certonly --standalone -d yourdomain.com
   ```

2. **Mount certificate in docker-compose.prod.yaml**:
   ```yaml
   proxy:
     volumes:
       - /etc/letsencrypt/live/yourdomain.com:/etc/ssl/certs
   ```

3. **Update nginx.conf** to handle HTTPS and redirect HTTP

### Rollback Procedure

If something goes wrong in production:

```bash
# Stop current deployment
docker compose -f docker-compose.prod.yaml down

# Checkout previous commit
git checkout <previous-commit-hash>

# Rebuild and restart
docker compose -f docker-compose.prod.yaml build
docker compose -f docker-compose.prod.yaml up -d
```

---

## API Documentation

### Backend API Endpoints

The backend uses Django Ninja for API endpoints. All APIs are available at `/api/` path:

**Key Endpoints:**
- `/api/accounts/` - User and authentication endpoints
- `/api/blog/` - Blog posts and content
- `/api/store/` - Products and categories
- `/api/cart/` - Shopping cart operations
- `/api/payments/` - Payment and order endpoints

**Authentication:**
- Token-based authentication available
- CORS enabled for frontend requests (all origins in dev, restricted in prod)

### Viewing API Documentation

- **OpenAPI/Swagger**: Available via Django Ninja auto-documentation
- **API Explorer**: Access through backend admin interface

---

## Key Technology Stack

### Backend
- **Django 6.0** - Web framework
- **Wagtail CMS** - Content management system
- **Django Ninja** - API framework
- **PostgreSQL** - Primary database
- **Gunicorn** - Production WSGI server (production only)
- **Python 3.13** - Runtime

### Frontend
- **Vue.js 3** - Progressive JavaScript framework
- **Vite** - Next generation build tool
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **Pinia** - State management
- **Vue Router** - Client-side routing
- **Vitest** - Unit testing
- **Playwright** - E2E testing
- **Node.js 20+** - Runtime

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Container orchestration
- **Nginx** - Reverse proxy and web server
- **PostgreSQL 17** - Database (Alpine Linux)

---

## Troubleshooting

### Container Issues

**Backend container won't start:**
```bash
# Check logs
docker compose logs backend

# Common issues:
# - Database connection: ensure db service is running
# - Port already in use: change port in docker-compose.yaml
# - Missing migrations: run migrations manually
```

**Database connection errors:**
```bash
# Verify database is running
docker compose ps db

# Wait for database to be ready
docker compose exec backend python manage.py wait_for_db
```

**Proxy/Nginx errors:**
```bash
# Check Nginx configuration
docker compose exec proxy nginx -t

# View Nginx logs
docker compose logs proxy
```

### Development Issues

**Port conflicts:**
- Frontend dev server: 5173
- Backend API: 8000
- Nginx proxy: 80
- PostgreSQL: 5432

Change ports in `docker-compose.yaml` if needed.

**Volume mount issues (macOS/Windows):**
- Ensure Docker Desktop has sufficient resources
- Check file permissions on mounted directories
- Consider using named volumes instead of bind mounts for better performance

### Database Issues

**Reset database:**
```bash
docker compose down -v
docker compose up
# Database will be initialized with new migrations
```

**Migrate data:**
```bash
docker compose exec backend python manage.py migrate [app_name]
```

---

## Contributing

1. Create a feature branch
2. Make changes and test locally
3. Run tests and linting
4. Submit pull request

**Code quality tools:**
- Backend: Django test framework, coverage
- Frontend: ESLint, Prettier, Vitest

---

## License

[Specify your license here]

---

## Support

For issues and questions:
- Check existing documentation in code comments
- Review Django/Wagtail official documentation
- Check Vue.js and Vite documentation

---

## Additional Resources

### Official Documentation
- [Django Documentation](https://docs.djangoproject.com/)
- [Wagtail CMS](https://wagtail.io/)
- [Django Ninja](https://django-ninja.rest-framework.com/)
- [Vue.js 3](https://vuejs.org/)
- [Vite](https://vitejs.dev/)
- [PostgreSQL](https://www.postgresql.org/docs/)

### Deployment Resources
- [Docker Documentation](https://docs.docker.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Gunicorn Documentation](https://gunicorn.org/)
- [Let's Encrypt SSL](https://letsencrypt.org/)
