# InsightHub – Data Ingestion & Analytics Backend

## FastAPI + PostgreSQL + MongoDB + AWS S3 + Docker + Pandas

InsightHub is a modern backend platform for uploading CSV/JSON datasets,
storing them securely on AWS S3, managing metadata in PostgreSQL, and
generating automatic descriptive analytics via a Pandas-based processing
engine. All services are orchestrated via Docker Compose and ready for
cloud deployment.

### Features

-   Dataset upload (CSV/JSON)
-   AWS S3 storage
-   PostgreSQL metadata tracking
-   Pandas-based background analytics
-   MongoDB analytics storage
-   REST API (upload, list datasets, fetch analytics)
-   Docker-based deployment

### Architecture

[Client → FastAPI] → S3 → PostgreSQL → Background Analyzer → MongoDB →
API consumer

### Setup

1.  Copy .env.example → .env
2.  Fill AWS + DB config
3.  Run: docker-compose up --build

### API

- POST /upload 
- GET /datasets and /datasets/{id}
- GET /analytics/{id}
- GET /health

### AWS

-   Private S3 bucket
-   IAM group: insighthub-uploaders
-   Least-privilege policy (Put/Get/List in uploads/*)
-   One IAM user per developer

### Future Enhancements

-   JWT auth
-   Presigned URL uploads
-   Celery + Redis
-   Alembic migrations
-   Monitoring stack
