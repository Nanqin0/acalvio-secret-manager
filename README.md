# Secret Manager

A secure, production-ready secret management service built with FastAPI and MongoDB. This service provides encrypted storage and retrieval of sensitive data using AES-GCM encryption.

## 🚀 Features

- **Secure Encryption**: AES-256-GCM encryption with random nonces for each secret
- **RESTful API**: FastAPI-based REST API with automatic documentation
- **MongoDB Storage**: Persistent storage with MongoDB
- **Base64 Input**: Accepts secrets in Base64 format for binary data support
- **UUID-based Access**: Secrets are identified by UUIDs for security
- **Production Ready**: Includes Gunicorn for production deployment

## 🏗️ Architecture

```
secret-manager/
├── app/
│   ├── main.py          # FastAPI application and endpoints
│   ├── schemas.py       # Pydantic models for request/response
│   ├── crypto_utils.py  # AES-GCM encryption utilities
│   ├── db.py           # MongoDB database operations
│   ├── config.py       # Configuration management
│   └── audit.py        # Audit logging (if implemented)
├── scripts/
│   ├── create_secret.sh # Example script to create secrets
│   └── fetch_secret.sh  # Example script to fetch secrets
└── tests/              # Test files
```

## 🛠️ Technology Stack

- **Backend**: FastAPI 0.111.0
- **Database**: MongoDB with PyMongo 4.7.2
- **Encryption**: Cryptography 42.0.7 (AES-GCM)
- **Server**: Uvicorn (development) / Gunicorn (production)
- **Configuration**: python-dotenv for environment management

## 📋 Prerequisites

- Python 3.8+
- MongoDB instance (local or remote)
- 32-byte master encryption key

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd secret_manager
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```bash
   # Required: 32-byte master key (base64 encoded or 32-character string)
   MASTER_KEY=your_32_byte_master_key_here
   
   # Optional: MongoDB connection string
   MONGO_URI=mongodb://localhost:27017
   ```

   **Generate a secure master key:**
   ```bash
   python -c "import secrets, base64; print(base64.b64encode(secrets.token_bytes(32)).decode())"
   ```

5. **Start MongoDB**
   
   Make sure MongoDB is running on your system or use a cloud instance.

## 🏃‍♂️ Running the Application

### Development Mode
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

The API will be available at `http://localhost:8000`

Interactive API documentation: `http://localhost:8000/docs`

## 📚 API Documentation

### Create Secret

**Endpoint:** `POST /vault/secret/create/`

**Request:**
```json
{
  "secret": "cGFzc3dvcmQxMjM="  // Base64 encoded secret
}
```

**Response:**
```json
{
  "secret_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

### Fetch Secret

**Endpoint:** `POST /vault/secret/fetch`

**Request:**
```json
{
  "secret_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

**Response:**
```json
{
  "secret": "cGFzc3dvcmQxMjM="  // Base64 encoded secret
}
```

## 💡 Usage Examples

### Using cURL

**Create a secret:**
```bash
# Encode your secret to base64 first
echo -n "password123" | base64
# Output: cGFzc3dvcmQxMjM=

# Create the secret
curl -X POST http://localhost:8000/vault/secret/create/ \
  -H "Content-Type: application/json" \
  -d '{"secret":"cGFzc3dvcmQxMjM="}'
```

**Fetch a secret:**
```bash
curl -X POST http://localhost:8000/vault/secret/fetch \
  -H "Content-Type: application/json" \
  -d '{"secret_id":"YOUR_SECRET_ID_HERE"}'
```

### Using the provided scripts

**Create a secret:**
```bash
chmod +x scripts/create_secret.sh
./scripts/create_secret.sh "cGFzc3dvcmQxMjM="
```

**Fetch a secret:**
```bash
chmod +x scripts/fetch_secret.sh
./scripts/fetch_secret.sh "YOUR_SECRET_ID_HERE"
```

### Using Python

```python
import requests
import base64

# Encode your secret
secret = base64.b64encode(b"password123").decode()

# Create secret
response = requests.post(
    "http://localhost:8000/vault/secret/create/",
    json={"secret": secret}
)
secret_id = response.json()["secret_id"]

# Fetch secret
response = requests.post(
    "http://localhost:8000/vault/secret/fetch",
    json={"secret_id": secret_id}
)
retrieved_secret = base64.b64decode(response.json()["secret"]).decode()
```

## 🔒 Security Features

- **AES-256-GCM Encryption**: Industry-standard authenticated encryption
- **Random Nonces**: Each encryption uses a unique 96-bit nonce
- **Master Key Protection**: Encryption key stored as environment variable
- **Input Validation**: Base64 validation and proper error handling
- **UUID-based Access**: Cryptographically secure secret identifiers
- **No Plaintext Storage**: Secrets are never stored in plaintext

## ⚙️ Configuration

| Environment Variable | Description | Default | Required |
|---------------------|-------------|---------|----------|
| `MASTER_KEY` | 32-byte master encryption key | None | Yes |
| `MONGO_URI` | MongoDB connection string | `mongodb://localhost:27017` | No |

## 🧪 Testing

```bash
# Run tests (if test files are present)
python -m pytest tests/

# Test the API manually
python -c "
import requests
import base64

# Test create
secret = base64.b64encode(b'test_secret').decode()
resp = requests.post('http://localhost:8000/vault/secret/create/', json={'secret': secret})
print('Create:', resp.json())

# Test fetch
secret_id = resp.json()['secret_id']
resp = requests.post('http://localhost:8000/vault/secret/fetch', json={'secret_id': secret_id})
print('Fetch:', resp.json())
"
```

## 🚀 Production Deployment

1. **Set secure environment variables**
2. **Use a production MongoDB instance**
3. **Configure proper logging and monitoring**
4. **Use HTTPS with reverse proxy (nginx/Apache)**
5. **Implement rate limiting**
6. **Regular key rotation procedures**

### Docker Deployment (if Dockerfile exists)
```bash
docker build -t secret-manager .
docker run -p 8000:8000 --env-file .env secret-manager
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

[Specify your license here]

## ⚠️ Security Considerations

- **Master Key Security**: Store the master key securely (e.g., AWS Secrets Manager, HashiCorp Vault)
- **Key Rotation**: Implement regular key rotation procedures
- **Access Control**: Add authentication and authorization layers
- **Audit Logging**: Implement comprehensive audit logging
- **Network Security**: Use HTTPS in production
- **Database Security**: Secure MongoDB with authentication and encryption

## 🐛 Troubleshooting

**Common Issues:**

1. **"MASTER_KEY environment variable not set"**
   - Ensure your `.env` file contains a valid `MASTER_KEY`
   - The key must be exactly 32 bytes

2. **"Connection refused" when connecting to MongoDB**
   - Verify MongoDB is running
   - Check the `MONGO_URI` configuration

3. **"Invalid base64" error**
   - Ensure your secret is properly base64 encoded
   - Use `echo -n "your_secret" | base64` to encode

For more issues, check the application logs or create an issue in the repository.
