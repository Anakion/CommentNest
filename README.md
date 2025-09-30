# CommentNest

A real-time comment system built with FastAPI, PostgreSQL, and Redis, featuring WebSocket support for live updates.

## Prerequisites

- Docker and Docker Compose
- Python 3.10+
- Git

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/Anakion/CommentNest.git
   cd CommentNest
   ```

2. **Build and start the services**
   ```bash
   docker-compose up --build
   ```

4. **Apply database migrations**
   In a new terminal, run:
   ```bash
   docker-compose exec web alembic upgrade head
   ```

5. **Access the application**
   - API documentation: http://localhost:8000/docs
   - Web interface: http://localhost:8000

## Development Setup

1. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -e .
   ```

3. **Start services**
   ```bash
   docker-compose up -d 
   ```

4. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

5. **Start the development server**
   ```bash
   uvicorn src.main:app --reload
   ```

## Project Structure

```
CommentNest/
├── src/                    # Application source code
│   ├── api/                # API routes
│   ├── core/               # Core functionality
│   ├── db/                 # Database models and migrations
│   └── services/           # Business logic
├── static/                # Frontend static files
├── migrations/            # Database migrations
├── .dev.env              # Development environment variables
├── docker-compose.yml    # Docker Compose configuration
└── pyproject.toml       # Project metadata and dependencies
```

## API Documentation

Once the application is running, you can access:
- Interactive API documentation: http://localhost:8000/docs
- Alternative documentation: http://localhost:8000/redoc

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.