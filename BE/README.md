# Coffee Shop Backend API

A coffee shop backend API service developed with FastAPI.

## Environment Requirements

- Python 3.10
- MySQL 5.7+
- Docker & Docker Compose (for containerized deployment)

## Project Setup

### Local Development

1. Create and activate a virtual environment:

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables:

   - Copy `.env.example` to `.env`:

   ```bash
   cp .env.example .env
   ```

   - Edit `.env` file with your configuration:

   ```
   # Database configuration
   DB_HOST=localhost     # Database host
   DB_PORT=3306          # Database port
   DB_USER=your_user     # Database username
   DB_PASSWORD=your_pass # Database password
   DB_NAME=coffee_shop   # Database name

   # Redis configuration
   REDIS_HOST=localhost  # Redis host
   REDIS_PORT=6379       # Redis port
   REDIS_DB=0            # Redis database number
   REDIS_PASSWORD=       # Redis password (if any)

   # Security configuration
   SECRET_KEY=your-secret-key-here           # JWT secret key
   ALGORITHM=HS256                           # JWT algorithm
   ACCESS_TOKEN_EXPIRE_MINUTES=43200        # Token expiration (30 days)

   # Application configuration
   DEBUG=true                # Enable debug mode
   ENVIRONMENT=development   # Environment (development/production)
   ```
4. Configure the database:

   - Create a database: `coffee_shop`
   - Modify database connection information in `.env` file
5. Initialize the database:

   - Execute `Data/SQL/create_table.sql` to create table structures
   - Execute `Data/SQL/insert_data.sql` to insert basic data and product specifications
6. Run the service:

```bash
uvicorn main:app --reload
```

### Docker Deployment

The project supports multi-node deployment with Docker Compose:

1. Configure environment variables:

   - Review and modify environment variables in `docker-compose.yml` file
   - For production deployment, update the following values:
     - `SECRET_KEY`: Use a strong, unique secret key
     - `DB_PASSWORD`: Use a secure database password
     - `ENVIRONMENT`: Set to `production`
     - `DEBUG`: Set to `false`
2. Build and start the services:

```bash
docker-compose up -d
```

3. Access the service:

   - The API will be available at http://localhost:8000
   - Nginx handles load balancing across three backend instances using least connections strategy
   - Health checks are configured for all services to ensure reliability
4. Stop the services:

```bash
docker-compose down
```

## System Architecture

The system is designed with a multi-tier architecture focusing on performance, scalability, and reliability:

1. **Multi-Node Deployment**

   - Three FastAPI instances running in parallel
   - Nginx load balancer distributing traffic using least connections strategy
   - Health checks ensuring high availability
2. **Data Synchronization**

   - Seatunnel for real-time data synchronization between MySQL and Redis
   - Change Data Capture (CDC) monitoring database changes
   - Automatic cache invalidation when data changes
3. **Caching Strategy**

   - Redis used for high-speed data caching
   - Frequently accessed data (products, user info, promotions) cached
   - Configurable expiration times (default: 24 hours)
4. **Monitoring and Observability**

   - Prometheus for metrics collection
   - Grafana for visualization and dashboards
   - Comprehensive alerting for system health

## API Documentation

After starting the service, access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
├── main.py              # Main program entry
├── config.py            # Configuration file
├── database.py          # Database connection
├── redis_utils.py       # Redis utilities
├── requirements.txt     # Project dependencies
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose configuration
├── Data/                # Data files
│   └── SQL/             # SQL scripts
│       ├── create_table.sql
│       └── insert_data.sql
├── models/              # Data models
│   └── models.py
├── schemas/             # Request/response models
│   └── schemas.py
├── routers/             # Route handlers
│   ├── auth.py          # Authentication
│   ├── users.py         # User related
│   ├── products.py      # Product related
│   └── promotions.py    # Promotion related
├── monitoring/          # Monitoring system
│   └── README.md        # Monitoring documentation
└── nginx/               # Nginx configuration
    └── conf.d/          # Nginx site configurations
```

## Implemented API Endpoints

1. Authentication

   - POST `/auth/register` - User registration
   - POST `/auth/login` - User login
2. User Related

   - GET `/users/findMy` - Get current user information
3. Product Related

   - GET `/products/type` - Get product category list
   - GET `/products/typeProducts/{type_name}` - Get product list by category
   - GET `/products/productDetail/{pid}` - Get product details
4. Promotion Related

   - GET `/promotions/searchguess` - Get promotion content list

## Database Structure

The system includes the following main tables:

1. `users` - User table

   - Stores user accounts, passwords, personal information, etc.
2. `product_types` - Product category table

   - Stores product type information (e.g., latte, coffee, rena ice, fruit tea, etc.)
3. `products` - Product table

   - Stores detailed product information, including name, price, description, images, etc.
4. `product_specs` - Product specification table

   - Stores product specification options (e.g., temperature, sweetness, dairy products, etc.)
5. `promotions` - Promotion content table

   - Stores marketing promotion information

## Monitoring System

The project includes a monitoring system based on Prometheus and Grafana:

1. Monitored metrics include:

   - HTTP request metrics (total requests, request duration)
   - Database metrics (connections in use, total connections)
   - Redis metrics (connection status, operations count)
   - System resource metrics (memory usage, CPU usage)
   - Business metrics (product views, active users, orders)
2. To start the monitoring system:

```bash
cd monitoring
docker-compose up -d
```

3. Access monitoring interfaces:
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3000 (default username/password: admin/admin)

## Important Notes

1. Ensure you are using Python 3.10
2. Database character set must support UTF-8
3. All authenticated API endpoints require a token in the request header:
   ```
   Authorization: Bearer <your_token>
   ```
4. For production environments, please:
   - Modify the `SECRET_KEY` in `config.py`
   - Configure appropriate CORS policies
   - Use secure database passwords
   - Enable HTTPS
   - Set up proper monitoring and alerting
