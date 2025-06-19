# 🔧 Run Prometheus UI (Manual Setup Reference)

# 1. Go to Prometheus extracted directory
cd ~/Tools/prometheus

# 2. Kill any previously running Prometheus process
sudo pkill -9 prometheus

# 3. Make sure port 9090 is free (should return nothing)
sudo lsof -i :9090

# 4. [Optional] If any PID is returned, kill it:
# sudo kill -9 <PID>

# 5. Edit prometheus.yml to make sure correct targets are configured
nano prometheus.yml

# Paste this inside prometheus.yml:
# -------------------------------------
# global:
#   scrape_interval: 15s
#   evaluation_interval: 15s
#
# scrape_configs:
#   - job_name: "prometheus"
#     static_configs:
#       - targets: ["localhost:9090"]
#
#   - job_name: "streamlit-app"
#     metrics_path: "/metrics"
#     static_configs:
#       - targets: ["localhost:8000"]
# -------------------------------------

# 6. Save and exit nano (Ctrl+O → Enter → Ctrl+X)

# 7. Start Prometheus with the config file
./prometheus --config.file=prometheus.yml

# 8. Open browser and visit:
# Prometheus UI: http://localhost:9090
# Target status: http://localhost:9090/targets
