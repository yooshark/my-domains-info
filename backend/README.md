# Backend Documentation

[![codecov](https://codecov.io/github/yooshark/my-domains-info/graph/badge.svg?token=UFO08MBNY9)](https://codecov.io/github/yooshark/my-domains-info)

Technical documentation for the My Domains Info backend service.

## 🏗 Architecture

### Technology Stack

**Backend:**

- **Framework**: FastAPI (Python 3.12+)
- **Database**: SQLite with SQLAlchemy ORM
- **Async Runtime**: AsyncIO with uvloop (Linux)
- **Dependency Injection**: aioinject
- **HTTP Client**: httpx for external API calls
- **DNS Resolution**: dnspython
- **Domain Parsing**: tldextract

**Infrastructure Clients:**

- **crt.sh**: Certificate transparency logs for subdomain discovery
- **IPWhois**: IP geolocation and network information
- **IPInfo**: IP information and anycast detection

**Development Tools:**

- **Testing**: pytest + pytest-asyncio + coverage
- **Linting**: ruff (Python)
- **Type Checking**: mypy (Python)
- **Database Migrations**: Alembic

### Project Structure

```
backend/
├── app/
│   ├── adapters/           # API adapters and routes
│   │   └── api/
│   │       ├── routes/     # API route handlers
│   │       └── main.py     # API router configuration
│   ├── application/        # Business logic services
│   │   └── domain_info.py  # Domain info service
│   ├── core/               # Core configuration and DI
│   │   ├── di/             # Dependency injection setup
│   │   ├── enums.py        # Domain enums
│   │   ├── server.py       # FastAPI app factory
│   │   ├── settings.py     # Configuration settings
│   │   └── utils.py        # Utility functions
│   ├── db/                 # Database layer
│   │   ├── models/         # SQLAlchemy models
│   │   ├── repositories/  # Data access layer
│   │   └── providers.py    # Database session provider
│   ├── infrastructure/     # External service clients
│   │   ├── crt_sh_client.py
│   │   ├── ipinfo_client.py
│   │   └── ipwhois_client.py
│   ├── migrations/         # Alembic database migrations
│   ├── schemas/            # Pydantic models
│   │   └── domain_info.py  # API request/response schemas
│   └── run.py              # Application entry point
├── tests/                  # Test suite
├── bin/                    # Scripts
│   └── entrypoint.sh      # Docker entrypoint (runs migrations automatically)
├── pyproject.toml          # Python dependencies
├── alembic.ini             # Migration configuration
└── Makefile                # Development commands
```

## 🚀 Local Development Setup

### Prerequisites

- **Python 3.12+**
- **uv** (recommended) or **pip**

### Installation

1. **Install dependencies:**
   ```bash
   cd backend
   # Using uv (recommended)
   uv sync
   # OR using pip
   pip install -e .
   ```

2. **Run migrations:**
   ```bash
   alembic upgrade head
   ```

3. **Start the development server:**
   ```bash
   python -m app.run
   # Or with uv
   uv run python -m app.run
   ```

The backend will be available at `http://localhost:8000`

### Development Commands

```bash
make lint          # Run linter (ruff)
make format        # Format code (ruff)
make typecheck     # Run type checker (mypy)
make test          # Run tests with coverage
make check         # Run all checks (lint + typecheck + test)
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

#### Application Settings (`APP_*`)

```bash
APP_DEBUG=true                    # Enable debug mode
APP_DEVELOP=true                  # Development mode (disables static file serving)
APP_PROJECT_NAME=My Domains Info  # Project name
APP_VERSION=0.1.0                 # Application version
APP_ENVIRONMENT=local              # Environment (local/production)
APP_ALLOW_ORIGINS=http://localhost:8000  # CORS allowed origins
```

#### Database Settings (`DB_*`)

```bash
DB_DRIVER=sqlite+aiosqlite        # Database driver
DB_NAME=db.sqlite3                # Database filename (default: db.sqlite3)
DB_ECHO=false                     # SQLAlchemy echo mode
DB_TIMEOUT=5                      # Connection timeout
```

> **Note:** The database file is stored in the application directory (`/app` in Docker). Migrations run automatically on
> container startup.

#### External API Settings

**IPWhois (`API_IP_WHOIS_*`):**

```bash
API_IP_WHOIS_BASE_URL=http://ipwho.is/
API_IP_WHOIS_TIMEOUT=10
```

**IPInfo (`API_IP_INFO_*`):**

```bash
API_IP_INFO_BASE_URL=https://ipinfo.io
API_IP_INFO_TIMEOUT=10
```

**crt.sh (`API_CRT_SH_*`):**

```bash
API_CRT_SH_BASE_URL=https://crt.sh
API_CRT_SH_TIMEOUT=10
```

## 📚 API Documentation

### Endpoints

| Method | Endpoint                   | Description                             |
|--------|----------------------------|-----------------------------------------|
| `GET`  | `/api/domain-info/`        | Get paginated list of domains           |
| `POST` | `/api/domain-info/`        | Add a new domain (discovers subdomains) |
| `POST` | `/api/domain-info/refresh` | Refresh all domain information          |

### Query Parameters

**GET `/api/domain-info/`:**

- `limit` (int, 1-100, default: 25): Number of results per page
- `offset` (int, >=0, default: 0): Pagination offset

### Request/Response Examples

#### Add a Domain

**Request:**

```bash
POST /api/domain-info/
Content-Type: application/json

{
  "domain_name": "example.com"
}
```

**Response:**

```json
[
  {
    "domain_name": "example.com",
    "domain_type": "root",
    "ip_address": "93.184.216.34",
    "geo_city": "Norwalk",
    "geo_country": "US",
    "network_owner_name": "Edgecast Inc",
    "is_active": true,
    "is_anycast_node": false,
    "dns_settings": {
      "A": [
        "93.184.216.34"
      ],
      "NS": [
        "a.iana-servers.net",
        "b.iana-servers.net"
      ]
    }
  },
  {
    "domain_name": "www.example.com",
    "domain_type": "subdomain",
    ...
  }
]
```

#### Get All Domains (Paginated)

**Request:**

```bash
GET /api/domain-info/?limit=25&offset=0
```

**Response:**

```json
{
  "total": 42,
  "items": [
    {
      "domain_name": "example.com",
      "ip_address": "93.184.216.34",
      "geo_city": "Norwalk",
      "geo_country": "US",
      "network_owner_name": "Edgecast Inc",
      "is_active": true,
      "is_anycast_node": false,
      "dns_settings": {
        ...
      }
    }
  ]
}
```

#### Refresh All Domains

**Request:**

```bash
POST /api/domain-info/refresh
```

**Response:**

```json
{
  "status": "ok"
}
```

### Interactive API Documentation

When running in development mode (`APP_DEBUG=true`), interactive API documentation is available at:

- **Swagger UI**: `http://localhost:8000/api/docs`
- **ReDoc**: `http://localhost:8000/api/redoc`

## 🗄️ Database Migrations

### Create a New Migration

```bash
cd backend
alembic revision --autogenerate -m "description"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback Migration

```bash
alembic downgrade -1
```

### Migration History

```bash
alembic history
```

## 🧪 Testing

### Running Tests

```bash
cd backend
make test
# Or directly
uv run pytest
```

### Running Tests with Coverage

```bash
make test
# Coverage report will be displayed
```

### Test Structure

```
tests/
├── conftest.py          # Pytest configuration and fixtures
└── unit/                # Unit tests
    ├── test_domain_info_service.py
    ├── test_repositories.py
    └── ...
```

## 🔧 Code Quality

### Linting

```bash
make lint
# Or directly
ruff check app
```

### Formatting

```bash
make format
# Or directly
ruff format .
```

### Type Checking

```bash
make typecheck
# Or directly
uv run mypy app
```

### All Checks

```bash
make check
# Runs: lint + typecheck + test
```

## 📦 Deployment

### Docker Entrypoint Behavior

The Docker entrypoint script (`bin/entrypoint.sh`) automatically runs database migrations on every container startup.
This ensures your database schema is always up to date without requiring manual intervention.

**Entrypoint flow:**

1. Runs `alembic upgrade head` to apply any pending migrations
2. Starts the FastAPI application

This means you don't need to set any environment variables or run migrations manually when using Docker.

### Production Deployment

1. **Build the Docker image:**
   ```bash
   docker build -t my-domains-info:latest \
     --build-arg VITE_API_URL=https://your-domain.com/api .
   ```

2. **Run with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

3. **Or run directly:**
   ```bash
   docker run -d \
     --name my-domains-info \
     -p 80:80 \
     --env-file .env \
     -v my-domains-data:/app \
     my-domains-info:latest
   ```

   > **Note:** Migrations run automatically on container startup. The database file is stored in `/app` directory, so
   mounting `/app` will persist your data.

### Docker Compose Configuration

The `docker-compose.yml` file can be customized:

```yaml
services:
  app:
    image: 'my-domains-app'
    build:
      context: .
      dockerfile: Dockerfile
      args:
        VITE_API_URL: http://your-domain.com/api  # Set API URL at build time
    container_name: my-domains-info
    restart: always
    env_file:
      - .env
    ports:
      - "80:80"  # Change port if needed
    volumes:
      - ./data:/app  # Persist database and application data
```

## 🏛️ Architecture Patterns

### Dependency Injection

The project uses `aioinject` for dependency injection. Services and repositories are registered in
`app/core/di/container.py` and injected via decorators:

```python
from aioinject import Injected
from aioinject.ext.fastapi import inject


@router.post("/")
@inject
async def add_domain(
        service: Injected[DomainInfoService]
) -> list[DomainInfo]:
    return await service.add_domain(data.domain_name)
```

### Repository Pattern

Data access is abstracted through repositories in `app/db/repositories/`. This provides a clean separation between
business logic and database operations.

### Service Layer

Business logic is implemented in services under `app/application/`. Services orchestrate domain operations and
coordinate between repositories and infrastructure clients.

### Infrastructure Clients

External API clients are located in `app/infrastructure/`. These clients handle communication with third-party services
like crt.sh, IPWhois, and IPInfo.

## 🔍 How It Works

### Domain Addition Flow

1. User submits a domain name via API or web interface
2. Service validates the domain and checks for duplicates
3. Service queries crt.sh to discover all subdomains
4. For each domain/subdomain:
    - Resolve IP address
    - Query DNS records (A, AAAA, MX, NS, CNAME, SOA, TXT)
    - Get geolocation from IPWhois
    - Get network information from IPInfo
    - Detect anycast configuration
5. Store all information in database
6. Return results to user

### Refresh Flow

1. User triggers refresh via API or web interface
2. Service retrieves all root domains from database
3. Re-queries crt.sh for each root domain to get updated subdomain list
4. For each domain (existing and new):
    - Collect fresh information from all sources
    - Update database records
5. Return success status

## 🐛 Troubleshooting

### Database Issues

If you encounter database errors:

1. Check database file permissions
2. Ensure migrations are up to date: `alembic upgrade head`
3. Verify database path in `.env` file

### External API Issues

If external APIs are failing:

1. Check network connectivity
2. Verify API endpoints are accessible
3. Check rate limits (especially for IPInfo)
4. Review timeout settings in environment variables

### Migration Issues

If migrations fail:

1. Check Alembic configuration in `alembic.ini`
2. Verify database connection string
3. Review migration files for errors
4. Use `alembic history` to check migration state
