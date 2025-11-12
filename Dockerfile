# Use Python slim as base
FROM python:3.11-slim

# Prevent interactive prompts during package install
ENV DEBIAN_FRONTEND=noninteractive

# Install a minimal TeX Live subset sufficient for most documents.
# This keeps size smaller than texlive-full but still may take time.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ca-certificates \
      wget \
      xz-utils \
      fontconfig \
      lmodern \
      texlive-latex-base \
      texlive-latex-recommended \
      texlive-fonts-recommended && \
    rm -rf /var/lib/apt/lists/*

# Create app directory, copy requirements, install Python deps
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy app source
COPY . /app

# Expose port (Flask will read PORT env)
EXPOSE 5000

# Default command
CMD ["python", "app.py"]
