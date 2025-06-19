# ===================== 1. INSTALL DEPENDENCIES =====================

# Install kubectl (already installed in your case, but just in case)
sudo dnf install -y kubernetes-client

# Minikube is not available via dnf in Fedora by default. Install via script instead:
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-latest.x86_64.rpm
sudo rpm -Uvh minikube-latest.x86_64.rpm

# ===================== 2. START MINIKUBE =====================

# Start Minikube with Docker as the driver
minikube start --driver=docker

# Confirm everything is running
minikube status

# ===================== 3. BUILD DOCKER IMAGE INSIDE MINIKUBE =====================

# Go to project root (very important for Docker context)
cd ~/PycharmProjects/PythonProject

# Make sure you're connected to Minikube’s Docker daemon
eval $(minikube docker-env)

# OPTIONAL: Remove old image to avoid cache issues
docker rmi my_streamlit_app:latest || true

# Build the Docker image with correct path to Dockerfile
docker build -t my_streamlit_app:latest -f Containerization/Dockerfile .

# Verify the image is built and available
docker images | grep streamlit

# ===================== 4. APPLY KUBERNETES CONFIGURATION =====================

# Apply deployment and service YAMLs
kubectl apply -f Orchestration/kubernetes_deployment.yaml
kubectl apply -f Orchestration/kubernetes_service.yaml

# Monitor pod status (watch until it's Running)
kubectl get pods -w

# ===================== 5. ACCESS THE STREAMLIT APP =====================

# Get the external URL for the service
minikube service streamlit-service --url
# Open the given URL in your browser to access your app
