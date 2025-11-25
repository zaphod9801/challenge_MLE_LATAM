# Flight Delay Prediction API - Solution Documentation

## Overview

This project implements a Machine Learning API for predicting flight delays at Santiago de Chile Airport (SCL). The solution includes a trained Logistic Regression model, a FastAPI REST API, and complete CI/CD pipeline deployed to Google Cloud Platform.

## Solution Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   Data.csv      │─────▶│  DelayModel      │─────▶│  model.joblib   │
│  (Training)     │      │  (scikit-learn)  │      │  (Artifact)     │
└─────────────────┘      └──────────────────┘      └─────────────────┘
                                                            │
                                                            ▼
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  Client         │─────▶│  FastAPI         │─────▶│  Predictions    │
│  (HTTP Request) │      │  (/predict)      │      │  (JSON Response)│
└─────────────────┘      └──────────────────┘      └─────────────────┘
```

## Technology Stack

### Backend
- **Python 3.11**: Core programming language
- **FastAPI**: Modern web framework for building APIs
- **Pydantic**: Data validation using Python type hints
- **uvicorn**: ASGI server for running the API

### Machine Learning
- **scikit-learn**: Machine learning library
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **joblib**: Model serialization

### Infrastructure
- **Docker**: Containerization
- **Google Cloud Platform**:
  - Cloud Run: Serverless container hosting
  - Cloud Build: Build automation
  - Artifact Registry: Container registry
- **GitHub Actions**: CI/CD automation

## Model Details

### Selected Model: Logistic Regression

**Rationale**:
- **Simplicity**: Linear model, easy to interpret and debug
- **Performance**: Adequate accuracy with class balancing
- **Compatibility**: No external dependencies (XGBoost not in requirements)
- **Speed**: Fast training and inference times

### Features
The model uses **10 key features** identified from exploratory analysis:
1. `OPERA_Latin American Wings`
2. `MES_7` (July)
3. `MES_10` (October)
4. `OPERA_Grupo LATAM`
5. `MES_12` (December)
6. `TIPOVUELO_I` (International)
7. `MES_4` (April)
8. `MES_11` (November)
9. `OPERA_Sky Airline`
10. `OPERA_Copa Air`

### Feature Engineering
- **Period of Day**: Morning/Afternoon/Night classification
- **High Season**: Binary flag for peak travel periods
- **Min Diff**: Time difference calculation
- **One-Hot Encoding**: Categorical variables transformation

## API Endpoints

### Health Check
```http
GET /health
```

**Response**:
```json
{
  "status": "OK"
}
```

### Predict Flight Delays
```http
POST /predict
```

**Request Body**:
```json
{
  "flights": [
    {
      "OPERA": "Aerolineas Argentinas",
      "TIPOVUELO": "N",
      "MES": 3
    }
  ]
}
```

**Response**:
```json
{
  "predict": [0]
}
```

**Valid Values**:
- `OPERA`: Airline operator (see list below)
- `TIPOVUELO`: `I` (International) or `N` (National)
- `MES`: Month (1-12)

**Supported Airlines**:
- American Airlines, Air Canada, Air France, Aeromexico
- Aerolineas Argentinas, Austral, Avianca, Alitalia
- British Airways, Copa Air, Delta Air, Gol Trans
- Iberia, K.L.M., Qantas Airways, United Airlines
- Grupo LATAM, Sky Airline, Latin American Wings
- Plus Ultra Lineas Aereas, JetSmart SPA
- Oceanair Linhas Aereas, Lacsa

## How to Use

### Production API

**Deployed URL**: `https://challenge-mle-pnjgibpoeq-uc.a.run.app`

**Example Request**:
```bash
curl -X POST https://challenge-mle-pnjgibpoeq-uc.a.run.app/predict \
  -H "Content-Type: application/json" \
  -d '{
    "flights": [
      {
        "OPERA": "Grupo LATAM",
        "TIPOVUELO": "I",
        "MES": 7
      }
    ]
  }'
```

### Local Development

#### Prerequisites
- Python 3.11+
- pip

#### Installation
```bash
# Clone the repository
git clone https://github.com/zaphod9801/challenge_MLE_LATAM.git
cd challenge_MLE_LATAM

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-test.txt
```

#### Running Locally
```bash
# Start the API
uvicorn challenge.api:app --host 0.0.0.0 --port 8000

# In another terminal, test it
curl http://localhost:8000/health
```

#### Running Tests
```bash
# Model tests
make model-test

# API tests
make api-test

# Build wheel
make build

# Stress test (requires API running)
make stress-test
```

### Docker

#### Build Image
```bash
docker build -t challenge-mle .
```

#### Run Container
```bash
docker run -p 8080:8080 challenge-mle
```

## CI/CD Pipeline

### Continuous Integration
**Trigger**: Push or Pull Request to `main` or `develop`

**Steps**:
1. Checkout code
2. Set up Python 3.11
3. Install dependencies
4. Run model tests
5. Run API tests

### Continuous Deployment
**Trigger**: Push to `main`

**Steps**:
1. Checkout code
2. Authenticate to GCP
3. Configure Docker for Artifact Registry
4. Build and push Docker image
5. Deploy to Cloud Run

## Performance Metrics

### Model
- **Accuracy**: Balanced with `class_weight='balanced'`
- **Features**: 10 key features (reduced from 100+)
- **Training Time**: < 1 minute

### API
- **Response Time (p50)**: 120ms
- **Response Time (p95)**: 240ms
- **Throughput**: ~14,000 requests in stress test

## Project Structure

```
challenge_MLE/
├── challenge/
│   ├── __init__.py
│   ├── model.py          # DelayModel implementation
│   ├── api.py            # FastAPI application
│   ├── train.py          # Model training script
│   └── model.joblib      # Trained model artifact
├── data/
│   └── data.csv          # Training dataset
├── tests/
│   ├── model/            # Model tests
│   └── api/              # API tests
├── .github/
│   └── workflows/
│       ├── ci.yml        # CI pipeline
│       └── cd.yml        # CD pipeline
├── Dockerfile            # Container definition
├── requirements.txt      # Python dependencies
├── requirements-test.txt # Test dependencies
└── Makefile             # Development commands
```

## Security & Best Practices

- **Input Validation**: Strict Pydantic validation for all inputs
- **Error Handling**: Proper HTTP status codes (400 for bad requests)
- **Logging**: Structured logging for debugging
- **Stateless**: No session state, fully scalable
- **Health Checks**: `/health` endpoint for monitoring

## Troubleshooting

### API Returns 400 Error
- Check that `OPERA` is in the supported airlines list
- Ensure `TIPOVUELO` is either `I` or `N`
- Verify `MES` is between 1 and 12

### Model Predictions Always Same
- Check if data is balanced in training set
- Verify feature engineering is applied correctly

### Docker Build Fails
- Ensure you're using Python 3.11 base image
- Check all dependencies are in `requirements.txt`

## Future Improvements

1. **Model Enhancement**:
   - Experiment with XGBoost or other ensemble methods
   - Add more features (weather, holidays, etc.)
   - Implement A/B testing framework

2. **API Enhancement**:
   - Add batch prediction endpoint
   - Implement caching for frequent requests
   - Add rate limiting

3. **Infrastructure**:
   - Set up monitoring and alerting (Prometheus/Grafana)
   - Implement auto-scaling policies
   - Add staging environment

## License

This project was created as part of a technical challenge.

## Contact

For questions or issues, please open an issue in the GitHub repository.
