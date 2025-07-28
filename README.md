# MLOps Week 7: Iris Classifier API with Advanced Observability on GKE

## 📋 Project Overview

This project demonstrates a **complete MLOps pipeline** for deploying a machine learning model (Iris flower classifier) as a **REST API** on **Google Kubernetes Engine (GKE)** with **advanced observability features**. The project showcases containerized deployment, automated CI/CD with GitHub Actions, comprehensive monitoring with Google Cloud Trace, structured logging, and production-ready Kubernetes orchestration with auto-scaling capabilities.

## 🏗️ Project Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GitHub Repo   │───▶│  GitHub Actions  │───▶│  Google Cloud   │
│   (Source Code) │    │   (CI/CD Pipeline)│    │   Infrastructure│
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                        ┌──────────────────┐    ┌─────────────────┐
                        │ Docker Registry  │    │ Google Cloud    │
                        │ (Artifact Registry)│   │ Storage (GCS)   │
                        └──────────────────┘    └─────────────────┘
                                │                        │
                                └────────┬───────────────┘
                                         ▼
                                ┌─────────────────┐
                                │ Google          │
                                │ Kubernetes      │      ┌─────────────────┐
                                │ Engine (GKE)    │ ────▶│ Google Cloud    │
                                │                 │      │ Trace & Logging │
                                │ ┌─────────────┐ │      └─────────────────┘
                                │ │ Iris API    │ │
                                │ │ (FastAPI +  │ │      ┌─────────────────┐
                                │ │ Observability)│ ────▶│ Load Balancer   │
                                │ └─────────────┘ │      │ + Auto Scaling  │
                                └─────────────────┘      └─────────────────┘
```

## 📁 Project Structure

```
mlops_week7/
├── .github/
│   └── workflows/
│       └── main.yml                # GitHub Actions CI/CD pipeline
├── api/
│   ├── Dockerfile                 # Container configuration
│   ├── iris_fastapi.py            # FastAPI app with observability
│   ├── model.joblib              # Pre-trained ML model
│   └── requirements.txt          # Python dependencies + observability libs
├── deployment.yaml               # Kubernetes deployment with telemetry SA
├── service.yaml                  # LoadBalancer service + BackendConfig
├── hpa.yaml                      # Horizontal Pod Autoscaler
├── wrk_script.lua               # Load testing script for performance
├── deploy.MD                    # GCP setup instructions
├── .gitignore                   # Git ignore rules
└── key files (encoded)          # GCP service account credentials
```

## 🚀 **NEW in Week 7: Advanced Observability Features**

### 📊 **Google Cloud Trace Integration**
- **Distributed Tracing**: Every API request gets a unique trace ID for end-to-end tracking
- **Performance Monitoring**: Detailed latency analysis for model inference
- **Request Correlation**: Link logs and traces for better debugging

### 📝 **Structured JSON Logging**
- **Cloud-Native Format**: Logs compatible with Google Cloud Logging
- **Rich Context**: Each log entry includes trace IDs, request details, and performance metrics
- **Severity Levels**: Proper logging levels (INFO, WARNING, ERROR) for different events

### 🔍 **Enhanced Health Monitoring**
- **Separate Probes**: Distinct liveness (`/live_check`) and readiness (`/ready_check`) endpoints
- **Startup Simulation**: Realistic model loading time simulation for testing
- **State Management**: App-level state tracking for better health reporting

### ⚡ **Performance Instrumentation**
- **Request Timing**: Every response includes `X-Process-Time-ms` header
- **Model Inference Latency**: Detailed timing for ML model predictions
- **Load Testing**: Automated 5-minute load test with detailed performance reporting

## 🔧 File Functionalities

### 🚀 Core Application Files

#### `api/iris_fastapi.py`
**Enhanced with Observability Features:**
- **OpenTelemetry Integration**: Full tracing with Google Cloud Trace
- **Structured Logging**: JSON-formatted logs with trace correlation
- **Health Probes**: Kubernetes-ready liveness and readiness checks
- **Performance Monitoring**: Request timing and inference latency tracking
- **Error Handling**: Comprehensive exception handling with trace IDs
- **API Endpoints**:
  - `GET /`: Welcome message
  - `GET /live_check`: Liveness probe for Kubernetes
  - `GET /ready_check`: Readiness probe for Kubernetes  
  - `POST /predict/`: Iris species prediction with full observability

#### `api/model.joblib`
- **Purpose**: Pre-trained scikit-learn Decision Tree Classifier
- **Features**: 
  - Trained on the Iris dataset
  - Accepts 4 features: sepal_length, sepal_width, petal_length, petal_width
  - Classifies into 3 species: setosa, versicolor, virginica

#### `api/requirements.txt`
**Updated Dependencies for Observability:**
- **Core FastAPI**: `fastapi`, `uvicorn`, `scikit-learn`, `joblib`, `numpy`, `pandas`
- **Observability Stack**: 
  - `opentelemetry-api`: Core OpenTelemetry API
  - `opentelemetry-sdk`: OpenTelemetry SDK
  - `opentelemetry-exporter-cloud-trace`: Google Cloud Trace integration

#### `api/Dockerfile`
- **Purpose**: Container configuration for the API
- **Features**:
  - Based on `python:3.10-slim` for optimal size
  - Installs all dependencies including observability libraries
  - Exposes port 8200 and runs FastAPI with uvicorn

### ☸️ Kubernetes Configuration

#### `deployment.yaml`
**Enhanced for Observability:**
- **Service Account**: Uses `telemetry-access` service account for Google Cloud integration
- **Health Probes**: Updated to use new `/live_check` and `/ready_check` endpoints
- **Resource Management**: Optimized CPU/memory requests and limits
- **Security**: Non-root container execution

#### `service.yaml`
- **LoadBalancer**: External access with Google Cloud Load Balancer
- **BackendConfig**: Health check configuration for load balancer
- **Port Mapping**: External port 80 → internal port 8200

#### `hpa.yaml` ⭐ **NEW**
- **Auto-Scaling**: Horizontal Pod Autoscaler configuration
- **Scale Range**: 2-5 replicas based on CPU utilization (50% target)
- **High Availability**: Ensures minimum 2 replicas for redundancy

#### `wrk_script.lua` ⭐ **NEW**
- **Load Testing**: Lua script for wrk load testing tool
- **Performance Metrics**: Detailed latency percentiles and throughput analysis
- **Request Simulation**: POST requests to `/predict/` endpoint with sample data

### 🔄 CI/CD Pipeline

#### `.github/workflows/main.yml`
**Enhanced CI/CD with Performance Testing:**
- **Comprehensive Pipeline**:
  1. Code checkout and GCP authentication
  2. Model download from Google Cloud Storage
  3. Docker build and push to Artifact Registry
  4. Kubernetes deployment with rolling updates
  5. **NEW**: 5-minute load testing with wrk
  6. **NEW**: Automated performance reporting with CML
- **Performance Testing**: Automated load test with 4 threads, 100 connections for 5 minutes
- **Reporting**: CML-generated reports with deployment status and performance metrics

### 🔐 Security & Configuration

#### `deploy.MD`
**GCP Setup Instructions:**
- **Workload Identity**: Setup instructions for `telemetry-gsa` service account
- **Permissions**: Google Cloud Trace agent role assignment
- **Kubernetes Integration**: Service account binding for secure access

#### `.gitignore`
**Enhanced Security:**
- Protects all credential files and sensitive data
- Excludes generated reports and temporary files
- Maintains clean repository structure

## 🎯 Observability Achievement

### **Complete Production Monitoring Stack:**

1. **🔍 Distributed Tracing**: 
   - Every request tracked end-to-end with Google Cloud Trace
   - Correlation between requests, logs, and performance metrics
   - Visual service map in Google Cloud Console

2. **📊 Structured Logging**: 
   - JSON-formatted logs compatible with Google Cloud Logging
   - Automated log correlation with trace IDs
   - Searchable and filterable log analysis

3. **⚡ Performance Monitoring**: 
   - Real-time latency tracking for API responses
   - Model inference performance analysis
   - Automated load testing with detailed reporting

4. **🔧 Health Monitoring**: 
   - Kubernetes health probes for container lifecycle management
   - Load balancer health checks for traffic routing
   - Application state monitoring and reporting

5. **📈 Auto-Scaling**: 
   - CPU-based horizontal pod autoscaling
   - Automatic traffic handling during load spikes
   - Resource optimization based on demand

## 🚀 API Usage

Once deployed, the API provides the following endpoints:

### **Health & Monitoring Endpoints:**
- **Liveness Check**: `GET http://<EXTERNAL_IP>/live_check`
- **Readiness Check**: `GET http://<EXTERNAL_IP>/ready_check`

### **Prediction Endpoint:**
- **Iris Prediction**: `POST http://<EXTERNAL_IP>/predict/`

### Example Prediction Request:
```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

### Example Response (with observability headers):
```json
{
  "predicted_class": "setosa"
}
```
**Headers include:**
- `X-Process-Time-ms`: Request processing time
- `X-Trace-Id`: Google Cloud Trace ID for request correlation

## 🏋️‍♀️ Performance Testing

The automated CI/CD pipeline includes comprehensive load testing:

- **Test Configuration**: 4 threads, 100 concurrent connections, 5-minute duration
- **Target Endpoint**: POST `/predict/` with realistic Iris data
- **Metrics Collected**: Throughput, latency percentiles (50th, 90th, 99th), error rates
- **Reporting**: Automated performance reports in GitHub PR comments

## 🏆 Key MLOps Principles Demonstrated

1. **Infrastructure as Code**: Complete Kubernetes manifests and Docker configuration
2. **Observability**: Comprehensive monitoring, logging, and tracing
3. **Automated Testing**: Health checks, load testing, and deployment verification
4. **Continuous Deployment**: Fully automated pipeline from code to production
5. **Model Versioning**: Model artifacts managed in Google Cloud Storage
6. **Scalability**: Auto-scaling based on CPU utilization and traffic patterns
7. **Security**: Workload Identity, least privilege access, secure credential management
8. **Performance**: Latency tracking, load testing, and performance optimization
9. **Reliability**: Health probes, rolling updates, and high availability
10. **Monitoring**: Production-ready observability with Google Cloud operations suite

## 📊 Monitoring & Observability in Production

### **Google Cloud Console Integration:**
- **Trace Timeline**: Visualize request flows and identify bottlenecks
- **Log Explorer**: Search and analyze structured application logs
- **Metrics Dashboard**: Monitor API performance and resource utilization
- **Error Reporting**: Automatic error aggregation and alerting

### **Performance Insights:**
- Average response time tracking
- Error rate monitoring
- Resource utilization analysis
- Auto-scaling trigger insights

This project represents a **complete, production-ready MLOps pipeline** with **enterprise-grade observability** that can serve as a template for deploying machine learning models at scale in cloud environments with comprehensive monitoring and performance optimization.

## 🔧 File Functionalities

### 🚀 Core Application Files

#### `api/iris_fastapi.py`
- **Purpose**: Main FastAPI application serving the Iris classifier
- **Key Features**:
  - RESTful API with Pydantic data validation
  - Model loading on application startup
  - Three endpoints:
    - `GET /`: Welcome message
    - `GET /health`: Health check for Kubernetes probes
    - `POST /predict/`: Iris species prediction endpoint
  - Input validation for sepal/petal measurements
  - Error handling for missing models

#### `api/model.joblib`
- **Purpose**: Pre-trained scikit-learn Decision Tree Classifier
- **Features**: 
  - Trained on the Iris dataset
  - Accepts 4 features: sepal_length, sepal_width, petal_length, petal_width
  - Classifies into 3 species: setosa, versicolor, virginica

#### `api/requirements.txt`
- **Purpose**: Python dependencies specification
- **Dependencies**:
  - `fastapi`: Web framework for building APIs
  - `uvicorn`: ASGI server for FastAPI
  - `scikit-learn`: Machine learning library
  - `numpy`, `pandas`: Data manipulation
  - `joblib`: Model serialization

#### `api/Dockerfile`
- **Purpose**: Container configuration for the API
- **Features**:
  - Based on `python:3.10-slim` for optimal size
  - Installs dependencies and exposes port 8200
  - Runs FastAPI with uvicorn server
  - Production-ready container setup

### ☸️ Kubernetes Configuration

#### `deployment.yaml`
- **Purpose**: Complete Kubernetes deployment configuration
- **Components**:
  1. **Deployment**: 
     - 2 replicas for high availability
     - Rolling update strategy for zero-downtime deployments
     - Resource limits and requests
     - Security context (non-root user)
     - Health probes (readiness, liveness, startup)
  2. **Service**: 
     - LoadBalancer type for external access
     - Port mapping (80 → 8200)
  3. **BackendConfig**: 
     - GKE-specific health check configuration

### 🔄 CI/CD Pipeline

#### `.github/workflows/main.yml`
- **Purpose**: Automated CI/CD pipeline for GKE deployment
- **Workflow Steps**:
  1. **Code Checkout**: Download repository code
  2. **GCP Authentication**: Decode and activate service account
  3. **Model Download**: Fetch trained model from Google Cloud Storage
  4. **GKE Setup**: Configure kubectl for cluster access
  5. **Docker Operations**: Build and push images to Artifact Registry
  6. **Deployment**: Apply Kubernetes configurations
  7. **Verification**: Wait for deployment and get external IP
  8. **Cleanup**: Remove sensitive credentials

- **Environment Variables**:
  - `GCP_PROJECT_ID`: mlopsweek1
  - `GKE_CLUSTER`: mlopsweek6
  - `GKE_REGION`: us-central1
  - `MODEL_BUCKET_URI`: GCS path to the trained model

### 🔐 Security & Configuration

#### `.gitignore`
- **Purpose**: Prevents sensitive files from being committed
- **Protections**:
  - Python cache files and virtual environments
  - API keys and credentials
  - IDE-specific files
  - Temporary and log files

#### Service Account Keys
- **Files**: `new_key`, `new_key1`, `key.json`, etc.
- **Purpose**: Base64-encoded GCP service account credentials
- **Usage**: Enables GitHub Actions to authenticate with Google Cloud services

## 🎯 Final Achievement

### **Complete MLOps Solution Achieved:**

1. **🤖 Model Serving**: 
   - Pre-trained Iris classifier deployed as a REST API
   - Real-time predictions via HTTP endpoints
   - Production-ready FastAPI application

2. **📦 Containerization**: 
   - Docker-based deployment for consistency
   - Lightweight Python container optimized for production

3. **☸️ Kubernetes Orchestration**: 
   - High-availability deployment with 2 replicas
   - Auto-scaling and self-healing capabilities
   - Health monitoring and zero-downtime updates

4. **🔄 CI/CD Automation**: 
   - Fully automated deployment pipeline
   - Triggered on code commits to main branch
   - Model synchronization from Google Cloud Storage

5. **☁️ Cloud Infrastructure**: 
   - Google Kubernetes Engine for container orchestration
   - Google Cloud Storage for model artifacts
   - Google Artifact Registry for container images

6. **🔒 Production Security**: 
   - Non-root container execution
   - Service account-based authentication
   - Secrets management through GitHub Secrets

7. **📊 Monitoring & Health**: 
   - Kubernetes health probes
   - LoadBalancer with external IP access
   - Automated rollout verification

## 🚀 API Usage

Once deployed, the API provides the following endpoints:

- **Health Check**: `GET http://<EXTERNAL_IP>/health`
- **Prediction**: `POST http://<EXTERNAL_IP>/predict/`

### Example Prediction Request:
```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

### Example Response:
```json
{
  "predicted_class": "setosa"
}
```

## 🏆 Key MLOps Principles Demonstrated

1. **Infrastructure as Code**: Kubernetes manifests and Dockerfiles
2. **Automated Testing**: Health checks and deployment verification
3. **Continuous Deployment**: Automated pipeline from code to production
4. **Model Versioning**: Model artifacts stored in cloud storage
5. **Scalability**: Kubernetes-based horizontal scaling
6. **Monitoring**: Health probes and service monitoring
7. **Security**: Least privilege access and secure credential management

This project represents a complete, production-ready MLOps pipeline that can serve as a template for deploying machine learning models at scale in cloud environments.


## 📝 Deployment Instructions

### **Prerequisites:**
1. Google Cloud Project with GKE API enabled
2. GitHub repository with required secrets configured
3. Google Cloud Storage bucket with trained model

### **Setup Steps:**

#### 1. **GCP Service Account Setup** (run in Google Cloud Shell):
```bash
# Create service account for telemetry
gcloud iam service-accounts create telemetry-gsa \
  --project=mlopsweek1 \
  --display-name="Telemetry Service Account"

# Grant Cloud Trace Agent permissions
gcloud projects add-iam-policy-binding mlopsweek1 \
  --member="serviceAccount:telemetry-gsa@mlopsweek1.iam.gserviceaccount.com" \
  --role="roles/cloudtrace.agent"

# Create Kubernetes service account
kubectl create serviceaccount telemetry-access

# Bind Kubernetes SA to Google Cloud SA (Workload Identity)
gcloud iam service-accounts add-iam-policy-binding \
  telemetry-gsa@mlopsweek1.iam.gserviceaccount.com \
  --role="roles/iam.workloadIdentityUser" \
  --member="serviceAccount:mlopsweek1.svc.id.goog[default/telemetry-access]"

# Annotate Kubernetes service account
kubectl annotate serviceaccount telemetry-access \
  iam.gke.io/gcp-service-account=telemetry-gsa@mlopsweek1.iam.gserviceaccount.com
```

#### 2. **GitHub Secrets Configuration:**
Configure the following secrets in your GitHub repository:
- `GCP_SA_KEY_B64`: Base64-encoded service account key

#### 3. **Deploy:**
Push to the `main` branch to trigger automated deployment via GitHub Actions.

### **Monitoring Access:**
- **Google Cloud Trace**: https://console.cloud.google.com/traces
- **Google Cloud Logging**: https://console.cloud.google.com/logs
- **GKE Workloads**: https://console.cloud.google.com/kubernetes/workload

## 🔧 Local Development

### **Run Locally:**
```bash
cd api
pip install -r requirements.txt
uvicorn iris_fastapi:app --host 0.0.0.0 --port 8200 --reload
```

### **Test Endpoints:**
```bash
# Health checks
curl http://localhost:8200/live_check
curl http://localhost:8200/ready_check

# Prediction
curl -X POST http://localhost:8200/predict/ \
  -H "Content-Type: application/json" \
  -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
```

### **Load Testing:**
```bash
# Install wrk
sudo apt-get install wrk  # Ubuntu/Debian
# or
brew install wrk         # macOS

# Run load test
wrk -t4 -c100 -d30s -s wrk_script.lua http://localhost:8200/predict/
```

## 🐛 Troubleshooting

### **Common Issues:**

1. **Pod stuck in `Pending`**: Check resource quotas and node capacity
2. **Authentication errors**: Verify Workload Identity setup and service account permissions
3. **Model loading failures**: Ensure model file exists in GCS bucket
4. **Trace not appearing**: Check service account has `roles/cloudtrace.agent`

### **Debugging Commands:**
```bash
# Check pod status
kubectl get pods -l app=iris-api

# View pod logs
kubectl logs -l app=iris-api -f

# Describe deployment
kubectl describe deployment iris-api-deployment

# Check service endpoints
kubectl get svc iris-api-service

# View HPA status
kubectl get hpa iris-api-hpa
```