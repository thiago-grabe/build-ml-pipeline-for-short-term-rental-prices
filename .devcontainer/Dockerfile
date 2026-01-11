# Multi-stage build for efficiency
FROM condaforge/mambaforge:24.3.0-0 AS conda-builder

# Copy environment files
COPY environment.yml /tmp/environment.yml
COPY conda.yml /tmp/conda.yml
COPY components/conda.yml /tmp/components-conda.yml

# Create main development environment
RUN mamba env create -f /tmp/environment.yml && \
    mamba clean -afy

# Final stage - based on Debian Bookworm
FROM mcr.microsoft.com/devcontainers/base:bookworm

# Install system dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        build-essential \
        libopenblas-dev \
        liblapack-dev \
        git-lfs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy conda from builder stage
COPY --from=conda-builder /opt/conda /opt/conda

# Set up conda for all users
ENV PATH="/opt/conda/bin:$PATH"

# Initialize conda for system-wide use
RUN /opt/conda/bin/conda init bash && \
    /opt/conda/bin/conda init zsh && \
    echo "conda activate nyc_airbnb_dev" >> /etc/bash.bashrc && \
    echo "conda activate nyc_airbnb_dev" >> /etc/zsh/zshrc

# Set working directory
WORKDIR /workspace

# Default to bash (zsh will be set by devcontainer.json)
CMD ["/bin/bash"]
