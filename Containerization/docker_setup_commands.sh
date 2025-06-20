PythonProject/
├── Containerization/
│   └── Dockerfile
├── Requirements/
│   └── requirements.txt
└── (other project files)


Step-by-Step Commands to Build and Run Your Streamlit App with Docker

# Step 1: Go to your project directory
cd /home/kirito/PycharmProjects/PythonProject

# Step 2: Build the Docker image using the Dockerfile located in Containerization/
# -f specifies the Dockerfile path
# -t tags the image as 'my_streamlit_app'
docker build -f Containerization/Dockerfile -t my_streamlit_app .

# Step 3: Run the Docker container and expose port 8501
# -p maps host port 8501 to container port 8501
# 'my_streamlit_app' is the name of the image to run
docker run -p 8501:8501 my_streamlit_app




Bonus: Clean Up Containers and Images (Optional)
If you want to stop and remove the container later:

# List running containers
docker ps

# Stop a container (replace <container_id> with actual ID)
docker stop <container_id>

# Remove stopped containers
docker container prune -f


If you want to remove the image:

docker rmi my_streamlit_app