# Use the official Python base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Copy the entire project into the container's working directory
COPY ../ /app/

# Install system dependencies (if any)
RUN apt-get update && apt-get install -y \
    build-essential \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*


# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r Requirements/requirements.txt

# Expose the default Streamlit port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "PRODUCT_APP/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
