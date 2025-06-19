# -----------------------------------------------
# Grafana Manual Setup Reference for Fedora/Linux
# -----------------------------------------------

# 1. Go to Downloads folder
cd ~/Downloads

# 2. Download latest Grafana enterprise .tar.gz
# (Replace URL with latest version if needed)
curl -LO https://dl.grafana.com/enterprise/release/grafana-enterprise-11.0.0.linux-amd64.tar.gz

# 3. Extract the downloaded archive
tar -xvzf grafana-enterprise-11.0.0.linux-amd64.tar.gz

# 4. Move extracted folder to Tools and rename for convenience
mv grafana-v11.0.0 ~/Tools/grafana

# 5. Change directory to Grafana binaries
cd ~/Tools/grafana/bin

# 6. Start Grafana server manually
./grafana-server web

# 7. Open browser and go to Grafana UI at:
#    http://localhost:3000
#    Default login:
#      Username: admin
#      Password: admin
#    (You will be prompted to change password on first login)

# -----------------------------------------------
# Optional: Add this script to Monitoring folder
# and include in .dockerignore to avoid Docker build issues
# -----------------------------------------------
