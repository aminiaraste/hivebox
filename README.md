# HiveBox

A DevOps learning project .

## Features

- FastAPI REST API
- Docker
- GitHub Actions
- Kubernetes
- Monitoring
- Infrastructure as Code

## Run locally

```bash
uvicorn app.main:app --reload
```

## API

### Version

GET /version

Response:

```json
{
  "version": "0.0.1"
}
```