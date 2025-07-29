# MLOps: Automated CI/CD Pipeline for an Iris Classifier API

This project demonstrates a complete, production-grade MLOps pipeline that automates the deployment of a machine learning model. It uses a FastAPI application, containerized with Docker, and deployed to a scalable, observable environment on Google Kubernetes Engine (GKE). The entire process is orchestrated by a GitHub Actions CI/CD workflow.

## 🚀 Final Achievement

This project successfully builds an end-to-end, automated system that takes code from a Git commit to a live, publicly accessible, scalable, and observable API on the internet. Key achievements include:
- **Continuous Deployment**: Every push to the `main` branch automatically builds, tests, and deploys the latest version of the application with zero downtime.
- **Scalability**: The application is deployed on GKE and configured with a Horizontal Pod Autoscaler (HPA) to automatically scale based on CPU load.
- **Observability**: The application is instrumented with structured logging and distributed tracing (OpenTelemetry), providing deep insights into its performance and behavior in a production environment via Google Cloud Logging and Trace.
- **Infrastructure as Code**: All application and infrastructure configurations (Docker, Kubernetes, CI/CD) are defined as code within this repository, making the setup repeatable and version-controlled.

---

## 🏗️ Project Architecture

The architecture is designed for automation, scalability, and resilience.


+-----------------+      +----------------------+      +-------------------------+
|                 |      |                      |      |                         |
|   Developer     +----->+    GitHub Repo       +----->+   GitHub Actions CI/CD  |
| (git push)      |      | (main branch)        |      |   (Workflow runs)       |
|                 |      |                      |      |                         |
+-----------------+      +----------------------+      +-------------------------+
|
| 1. Authenticate
| 2. Download Model
| 3. Build & Push Image
| 4. Deploy to GKE
| 5. Load Test
v
+-------------------------+      +-------------------------+      +-------------------------+
|                         |      |                         |      |                         |
| Google Cloud Storage    |<-----+  Google Artifact Registry +----->+ Google Kubernetes Engine|
| (Model Artifacts)       |      |  (Docker Images)        |      |   (GKE Cluster)         |
|                         |      |                         |      |                         |
+-------------------------+      +-------------------------+      +-----------+-------------+
|
| Observability
v
+-------------------------+-------------------------+
|                         |                         |
|   Google Cloud Logging  |   Google Cloud Trace    |
|   (Structured Logs)     |   (Distributed Traces)  |
|                         |                         |
+-------------------------+-------------------------+


The workflow follows these steps:

1.  **Code Push**: A developer pushes a code change to the `main` branch of the GitHub repository.
2.  **Trigger GitHub Actions**: The push automatically triggers the CI/CD workflow defined in `.github/workflows/main.yml`.
3.  **Authentication & Setup**: The workflow authenticates with Google Cloud using a service account key and sets up the necessary tools (`gcloud`, `kubectl`, `docker`).
4.  **Build Docker Image**: A Docker image is built using the `api/Dockerfile`. This image packages the FastAPI application, all its Python dependencies, and the trained model into a self-contained, runnable unit.
5.  **Push to Artifact Registry**: The new image is tagged with the unique commit SHA and pushed to Google Artifact Registry for secure storage and versioning.
6.  **Deploy to GKE**: The workflow connects to the GKE cluster and applies the Kubernetes manifests (`deployment.yaml`, `service.yaml`, `hpa.yaml`), triggering a zero-downtime rolling update of the application.
7.  **Expose & Scale**: The Kubernetes Service exposes the application via a public IP, and the HPA monitors the pods, scaling them up or down as needed.
8.  **Load Test & Report**: The pipeline runs a `wrk` load test against the newly deployed application and posts a summary report, including the public IP and test results, as a comment on the Git commit.

---

## 📁 File Functionalities & Objectives

Each file in this project has a specific and crucial role in the pipeline.

### `api/iris_fastapi.py`
- **Objective**: To serve the machine learning model as a robust, observable, and high-performance web API.
- **Functionality**:
    - Uses **FastAPI** to create a high-performance web server.
    - Implements **OpenTelemetry** for structured logging to Google Cloud Logging and distributed tracing to Google Cloud Trace.
    - Loads the pre-trained `model.joblib` on startup.
    - Defines a `/predict/` endpoint for model inference.
    - Includes `/live_check` and `/ready_check` endpoints for robust Kubernetes health probes, ensuring traffic is only sent to healthy and fully initialized application instances.

### `api/Dockerfile`
- **Objective**: To create a standardized, portable, and self-contained package of the application.
- **Functionality**:
    - Starts from a slim Python base image to keep the final image size small.
    - Copies the application code and dependencies into the image.
    - Installs the required Python libraries via `requirements.txt`.
    - Exposes port `8200` and specifies the `uvicorn` command to start the server, making the container runnable in any Docker-compatible environment.

### `api/requirements.txt`
- **Purpose**: To define the application's Python dependencies.
- **Functionality**: Ensures a consistent and reproducible Python environment by listing all required libraries, including `fastapi`, `pandas`, and the `opentelemetry` packages for observability.

### `deployment.yaml`
- **Objective**: To declaratively manage the application's lifecycle and health within the Kubernetes cluster.
- **Functionality**: Defines the `Deployment` object, which manages the application's pods. It specifies the number of replicas, the container image to use (which is updated by the CI/CD pipeline), resource requests/limits, and the crucial `startupProbe`, `readinessProbe`, and `livenessProbe` for ensuring the application is healthy and resilient.

### `service.yaml`
- **Objective**: To provide a stable network endpoint to access the application from the internet.
- **Functionality**: Defines the `Service` of type `LoadBalancer`, which tells Google Cloud to provision an external IP address and forward traffic to the application pods. It also includes a `BackendConfig` for GKE-native health checking, which integrates more efficiently with Google's load balancers.

### `hpa.yaml`
- **Objective**: To enable automatic, demand-based scaling of the application.
- **Functionality**: Defines the `HorizontalPodAutoscaler`, which monitors the CPU utilization of the pods and automatically increases or decreases the number of replicas (between 2 and 5) to handle traffic spikes and reduce costs during idle periods.

### `.github/workflows/main.yml`
- **Objective**: To automate the entire build, test, and deployment process.
- **Functionality**:
    - **Trigger**: Runs on every `push` to the `main` branch.
    - **Authentication**: Securely logs into Google Cloud using a stored secret.
    - **Build & Push**: Runs `docker build` and `docker push` to create the application image and store it in Artifact Registry.
    - **Deploy**: Connects to the GKE cluster and applies all `.yaml` files, triggering the rolling update.
    - **Test & Report**: Runs a 5-minute `wrk` load test and posts a detailed summary as a comment on the commit using CML.

---

## 🚧 Common Roadblocks & Solutions

This project involved solving several common MLOps challenges. Here is a summary of the key roadblocks and their solutions:

- **Problem**: `PermissionDenied` errors when running `gcloud` commands from the VM's SSH terminal.
  - **Solution**: The VM's default service account lacks project-level permissions. The fix was to run administrative commands (like setting IAM policies) from the **Google Cloud Shell**, which is authenticated as a user with the necessary permissions.

- **Problem**: GitHub Actions failing with `failed to parse service account key JSON credentials`.
  - **Solution**: The base64-encoded secret was corrupted by newlines. The fix was to use the `base64 -w 0 <key-file>` command to generate a single, unbroken line of text for the GitHub secret.

- **Problem**: `kubectl` commands failing with `gke-gcloud-auth-plugin not found`.
  - **Solution**: Modern GKE clusters require this plugin for authentication. The fix was to add a step to the `main.yml` workflow to explicitly install it using `sudo apt-get install google-cloud-cli-gke-gcloud-auth-plugin`.

- **Problem**: Docker build failing with `Dockerfile not found` or `COPY failed`.
  - **Solution**: This was a pathing issue. The `docker build` command in the workflow was corrected to use the `./api` directory as its context, and the `Dockerfile`'s `COPY` command was changed from `COPY app/ /app` to `COPY . .` to reflect the new context.

- **Problem**: Deployment timing out with `exceeded its progress deadline`.
  - **Solution**: The application pods were crashing or not becoming ready in time. This was solved by:
    1.  Fixing syntax errors in `iris_fastapi.py`.
    2.  Ensuring the health probe paths in `deployment.yaml` (`/ready_check`, `/live_check`) exactly matched the endpoints in the Python code.
    3.  Adding a `startupProbe` to the `deployment.yaml` to give the application a longer grace period to load the model before readiness checks begin.

- **Problem**: Traces not appearing in the Trace Explorer.
  - **Solution**: This required a multi-step fix:
    1.  Granting the user account the `Cloud Trace User` role in IAM.
    2.  Explicitly enabling the `Cloud Trace API` on the project.
    3.  Adding the `opentelemetry-instrumentation-fastapi` library to `requirements.txt` and instrumenting the app to automatically create traces.
    4.  Fixing the `PermissionDenied` error from the pod by correctly configuring **Workload Identity**, linking the Kubernetes and Google service accounts with the proper IAM bindings and annotations.

---

## ⚙️ Running Instructions

### One-Time Setup in Google Cloud
These commands should be run once from the **Google Cloud Shell**.

1.  **Enable APIs**:
    ```bash
    gcloud services enable container.googleapis.com artifactregistry.googleapis.com cloudtrace.googleapis.com
    ```

2.  **Create Artifact Registry Repository**:
    ```bash
    gcloud artifacts repositories create iris-repo --repository-format=docker --location=us-central1
    ```

3.  **Create GKE Cluster**:
    ```bash
    gcloud container clusters create mlopsweek6 --region us-central1 --num-nodes=2 --machine-type=e2-small
    ```

4.  **Create Service Accounts & Permissions**:
    ```bash
    # For the CI/CD pipeline
    gcloud iam service-accounts create cicd-deployer --display-name="CI/CD Deployer"
    gcloud projects add-iam-policy-binding mlopsweek1 --member="serviceAccount:cicd-deployer@mlopsweek1.iam.gserviceaccount.com" --role="roles/artifactregistry.writer"
    gcloud projects add-iam-policy-binding mlopsweek1 --member="serviceAccount:cicd-deployer@mlopsweek1.iam.gserviceaccount.com" --role="roles/container.developer"
    gcloud projects add-iam-policy-binding mlopsweek1 --member="serviceAccount:cicd-deployer@mlopsweek1.iam.gserviceaccount.com" --role="roles/storage.objectViewer"

    # For the application's telemetry
    gcloud iam service-accounts create telemetry-gsa --display-name="Telemetry Service Account"
    gcloud projects add-iam-policy-binding mlopsweek1 --member="serviceAccount:telemetry-gsa@mlopsweek1.iam.gserviceaccount.com" --role="roles/cloudtrace.agent"
    ```

5.  **Configure Workload Identity**:
    ```bash
    # Create the in-cluster service account
    kubectl create serviceaccount telemetry-access

    # Link the GSA and KSA
    gcloud iam service-accounts add-iam-policy-binding telemetry-gsa@mlopsweek1.iam.gserviceaccount.com --role="roles/iam.workloadIdentityUser" --member="serviceAccount:mlopsweek1.svc.id.goog[default/telemetry-access]"
    
    # Annotate the KSA
    kubectl annotate serviceaccount telemetry-access --namespace default iam.gke.io/gcp-service-account=telemetry-gsa@mlopsweek1.iam.gserviceaccount.com --overwrite
    ```

### GitHub Setup

1.  **Create a Service Account Key**:
    - In the GCP Console, go to the `cicd-deployer` service account, create a new JSON key, and download it.

2.  **Create GitHub Secret**:
    - Go to your GitHub repository's **Settings > Secrets and variables > Actions**.
    - Create a new secret named `GCP_SA_KEY_B64`.
    - For the value, paste the base64-encoded content of the JSON key file. Use this command to encode it: `base64 -w 0 your-key-file.json`.

### Deployment

-   Deployment is fully automated. Simply commit and push your code to the `main` branch to trigger the workflow.

### How to Test

-   Find the external IP address in the CML report comment on your commit or by running `kubectl get service iris-api-service`.
-   Use the following `curl` command to test the prediction endpoint:
    ```bash
    curl -X 'POST' 'http://YOUR_EXTERNAL_IP/predict/' \
      -H 'Content-Type: application/json' \
      -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
    ```

### Manual Load Testing (from Cloud Shell)

1.  **Install `wrk`**:
    ```bash
    sudo apt-get update && sudo apt-get install -y wrk
    ```
2.  **Create a Lua script** named `post_script.lua` to define the POST request:
    ```lua
    wrk.method = "POST"
    wrk.body   = '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
    wrk.headers["Content-Type"] = "application/json"
    ```
3.  **Run the test** (replace `YOUR_EXTERNAL_IP`):
    ```bash
    wrk -t4 -c100 -d30s -s ./post_script.lua http://YOUR_EXTERNAL_IP/predict/
    ```
