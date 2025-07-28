# Deployment Setup Guide

## Prerequisites Setup in Google Cloud Shell

### Step 1: Create Telemetry Service Account
```bash
gcloud iam service-accounts create telemetry-gsa \
  --project=mlopsweek1 \
  --display-name="Telemetry Service Account"
```

### Step 2: Grant Cloud Trace Agent Permissions
```bash
gcloud projects add-iam-policy-binding mlopsweek1 \
  --member="serviceAccount:telemetry-gsa@mlopsweek1.iam.gserviceaccount.com" \
  --role="roles/cloudtrace.agent"
```

### Step 3: Create Kubernetes Service Account
```bash
kubectl create serviceaccount telemetry-access
```

### Step 4: Bind Kubernetes SA to Google Cloud SA (Workload Identity)
```bash
gcloud iam service-accounts add-iam-policy-binding \
  telemetry-gsa@mlopsweek1.iam.gserviceaccount.com \
  --role="roles/iam.workloadIdentityUser" \
  --member="serviceAccount:mlopsweek1.svc.id.goog[default/telemetry-access]"
```

### Step 5: Annotate Kubernetes Service Account
```bash
kubectl annotate serviceaccount telemetry-access \
  iam.gke.io/gcp-service-account=telemetry-gsa@mlopsweek1.iam.gserviceaccount.com
```

## How Workload Identity Works

Here's a breakdown of the process:

1. **Create an Identity in Google Cloud**: We created a Google Service Account (`telemetry-gsa`) and gave it the specific permission to send telemetry data (`roles/cloudtrace.agent`) to your project.

2. **Create an Identity in Kubernetes**: We created a Kubernetes Service Account (`telemetry-access`) inside your GKE cluster. This is the identity that your `deployment.yaml` assigns to your application pods.

3. **Link the Two Identities**: The binding command creates a link between the Kubernetes identity and the Google Cloud identity.

Now, when the application pod starts, it will use the `telemetry-access` identity, which GKE allows to securely "impersonate" the `telemetry-gsa` identity and inherit its permission to send trace data to Google Cloud. This is all done without needing any secret key files inside our cluster.

## Next Steps

1. Create/update Kubernetes manifests:
   - `deployment.yaml` - Main application deployment with telemetry SA
   - `service.yaml` - LoadBalancer service with BackendConfig
   - `hpa.yaml` - Horizontal Pod Autoscaler

2. Update `.github/workflows/main.yml` with enhanced CI/CD pipeline

3. Test deployment and verify observability features in Google Cloud Console

## Verification Commands

After deployment, verify the setup:

```bash
# Check if service account is properly bound
kubectl describe serviceaccount telemetry-access

# Check deployment status
kubectl get deployments

# Check pods
kubectl get pods -l app=iris-api

# Check service
kubectl get svc iris-api-service

# Check HPA
kubectl get hpa iris-api-hpa
```

