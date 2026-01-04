# AI Music Evaluation Framework - Development Docker Container
# Provides Jupyter environment with all dependencies for Phase 1

FROM python:3.11-slim

# Set working directory for the project
WORKDIR /workspace

# Install system dependencies required at runtime
RUN apt-get update && apt-get install -y \
  git \
  build-essential \
  sudo \
  && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt

# Create non-root user for runtime execution
RUN groupadd --gid 1000 node || true && \
  useradd --uid 1000 --gid node --create-home --shell /bin/bash node || true && \
  passwd -d node

# Copy project files and ensure node owns the workspace
COPY . /workspace/
RUN chown -R node:node /workspace

# Add Tini for proper signal handling and the shared entrypoint helper
ENV TINI_VERSION=v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini

COPY docker/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
RUN printf "node ALL=(root) NOPASSWD: /bin/chown -R node:node /workspace\n" > /etc/sudoers.d/node-workspace-chown && \
  chmod 440 /etc/sudoers.d/node-workspace-chown

# Configure Jupyter defaults for the node user
RUN mkdir -p /home/node/.jupyter && \
  cat <<'EOF' > /home/node/.jupyter/jupyter_lab_config.py
c.ServerApp.ip = '0.0.0.0'
c.ServerApp.allow_root = False
c.ServerApp.open_browser = False
EOF
RUN chown -R node:node /home/node/.jupyter

# Expose Jupyter port and establish environment variables
EXPOSE 8888

ENV PYTHONPATH=/workspace \
  JUPYTER_ENABLE_LAB=yes \
  HOME=/home/node

# Run the permission fix before launching Jupyter
USER node
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--ServerApp.token=", "--ServerApp.password="]
