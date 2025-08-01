# Secret Manager

A secure, production-ready secret management service built with FastAPI and MongoDB. Designed for Docker Swarm deployment with high availability and scalability.

## 🚀 Features

- **🔐 Advanced Encryption**: AES-256-GCM encryption with random 96-bit nonces for each secret
- **🌐 RESTful API**: FastAPI-based REST API with automatic OpenAPI documentation
- **📊 MongoDB Storage**: Persistent storage with MongoDB and connection pooling
- **📝 Audit Logging**: Comprehensive audit trail for all operations with configurable retention
- **🔍 Input Validation**: Strict Base64 validation and error handling
- **🆔 UUID-based Access**: Cryptographically secure secret identifiers
- **⚡ High Performance**: Async request handling with built-in concurrency support
- **🐳 Docker Swarm Ready**: Optimized for container orchestration and scaling
- **🔄 High Availability**: Multi-replica deployment with automatic failover

## 🏗️ Architecture

### Application Structure
```
secret-manager/
├── app/
│   ├── main.py          # FastAPI application and API endpoints
│   ├── schemas.py       # Pydantic models for request/response validation
│   ├── crypto_utils.py  # AES-GCM encryption/decryption utilities
│   ├── db.py           # MongoDB database operations and connection management
│   ├── config.py       # Environment configuration management
│   └── audit.py        # Comprehensive audit logging system
├── scripts/
│   ├── create_secret.sh # Shell script to create secrets via API
│   └── fetch_secret.sh  # Shell script to fetch secrets via API
├── tests/
│   ├── conftest.py     # Pytest configuration and fixtures
│   └── test_api.py     # Comprehensive API test suite
├── Dockerfile          # Container image definition
├── stack.yml           # Docker Swarm deployment configuration
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

### Docker Swarm Deployment
```
┌─────────────────────────────────────────┐
│           Docker Swarm Cluster          │
├─────────────────────────────────────────┤
│  Manager Node          Worker Nodes     │
│  ┌─────────────┐     ┌─────────────┐   │
│  │  MongoDB    │     │Secret-Mgr 1 │   │
│  │   :27017    │◄────┤   :8000     │   │
│  └─────────────┘     └─────────────┘   │
│                      ┌─────────────┐   │
│                      │Secret-Mgr 2 │   │
│                      │   :8000     │   │
│                      └─────────────┘   │
└─────────────────────────────────────────┘
         │                    │
    overlay network      load balancing
     (encrypted)        (ingress routing)
```

## 🛠️ Technology Stack

- **Backend**: FastAPI, Gunicorn, Uvicorn
- **Database**: MongoDB, PyMongo
- **Encryption**: AES-256-GCM (Cryptography)
- **Delopyment**: Docker Swarm
- **Testing**: pytest

## 📋 Prerequisites

- **Docker 20.10+ with Swarm**
- **Docker Compose 2.0+**
- **2GB RAM, 5GB storage minimum**

## 🚀  Quick Demo Instructions

### 1. **Clone Repository**
```bash
git clone <repository-url>
cd secret_manager
```

### 2. **Initialize Docker Swarm**
```bash
# Initialize Swarm (if not already done)
docker swarm init

# Check swarm status
docker info | grep Swarm
```

### 3. **Build Application Image**
```bash
# Build the Secret Manager image
docker build -t secret-manager:latest .
```

### 4. **Set MASTER_KEY**
```bash
# Generate a secure master key
export MASTER_KEY=$(python3 -c "import secrets, base64; print(base64.b64encode(secrets.token_bytes(32)).decode())")

```

### 5. **Deploy to Swarm**
```bash
# Deploy the stack
docker stack deploy -c stack.yml secret-manager

# Check deployment status
docker service ls
docker service ps secret-manager_secret-manager
```

### 6. **Demonstrate API**
```bash
# Access API documentation
curl http://localhost:8000/docs

# Create a secret using：
curl -X POST http://localhost:8000/vault/secret/create/ \
-d '{"secret":"<base64-secret>"}'   #"secret": "cGFzc3dvcmQxMjM="  // Base64 encoded plaintext

# Retrieve the secret:
curl -X POST http://localhost:8000/vault/secret/fetch \
-d '{"secret_id":"<secret-id>"}'
```

**Service Endpoints:**
- 📖 **API Documentation**: http://localhost:8000/docs
- 🔗 **API Endpoint**: http://localhost:8000
- 🗄️ **MongoDB**: localhost:27017 (internal)



## 🔒 Security Features

### Encryption
- **Algorithm**: AES-256-GCM (Galois/Counter Mode)
- **Key Size**: 256-bit master key
- **Nonce**: 96-bit random nonce per encryption
- **Authentication**: Built-in authentication tag prevents tampering
- **Key Management**: Master key stored as environment variable

### Data Protection
- **Encryption at Rest**: All secrets encrypted before database storage
- **No Plaintext Storage**: Plaintext never persists to disk
- **Secure Random**: Cryptographically secure random number generation
- **Input Validation**: Strict Base64 format validation
- **Error Handling**: No sensitive data leaked in error messages

### Audit & Monitoring
- **Operation Logging**: All create/fetch operations logged
- **IP Tracking**: Client IP addresses recorded
- **Timestamps**: UTC timestamps for all operations
- **Status Tracking**: Success/failure status for each operation
- **Configurable Retention**: TTL-based automatic log cleanup

## ⚙️ Configuration

| Environment Variable | Description | Default | Required |
|---------------------|-------------|---------|----------|
| `MASTER_KEY` | 32-byte master encryption key (base64 or raw) | None | **Yes** |
| `MONGO_URI` | MongoDB connection string | `mongodb://localhost:27017` | No |
| `AUDIT_ENABLED` | Enable/disable audit logging | `true` | No |
| `AUDIT_TTL_DAYS` | Audit log retention in days (0=forever) | `0` | No |


## 🧪 Testing

```bash
pytest tests/
```

## 🚀Scaling & Maintenance
```bash
# Scale
 docker service scale secret-manager_secret-manager=5

# Update
 docker service update --image secret-manager:v2.0 secret-manager_secret-manager
```



## 🔧 Troubleshooting

### Check service status:

```bash
docker service logs secret-manager_secret-manager
```

### MongoDB connectivity:
```bash
docker service logs secret-manager_mongodb
```

## 🤝 Contributing
 Fork, create branch, submit PR with tests

## ⚠️ Security Considerations
- Secure MASTER_KEY management
- Enable Docker Swarm encrypted networks
- Regular updates and monitoring


