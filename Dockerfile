FROM python:3.11-slim

# Prevent Python from creating .pyc files
# and ensure logs appear immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Production environment
ENV ENVIRONMENT=production

WORKDIR /app

# System dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       gcc \
    && rm -rf /var/lib/apt/lists/*

# Install pip
RUN pip install --no-cache-dir --upgrade pip

# Install CPU-only PyTorch first.
# This prevents sentence-transformers from pulling
# the large CUDA/NVIDIA dependency stack.
RUN pip install --no-cache-dir \
    torch \
    --index-url https://download.pytorch.org/whl/cpu

# Install application dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade \
    pip \
    setuptools \
    wheel \
    && pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Container listens on FastAPI port
EXPOSE 8000

# Production server
CMD ["uvicorn", "services.api:app", "--host", "0.0.0.0", "--port", "8000"]