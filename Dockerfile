# Step 1: Build the React Frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /ui
COPY ui/package*.json ./
RUN npm install
COPY ui/ ./
RUN npm run build

# Step 2: Set up Python Backend & Runtime
FROM python:3.10-slim
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy built frontend assets to the expected UI dist location
COPY --from=frontend-builder /ui/dist ./ui/dist

# Copy backend application source code
COPY app/ ./app/
COPY ingestion/ ./ingestion/
COPY scheduler/ ./scheduler/
COPY config/ ./config/
COPY start.sh ./

# Ensure start.sh has executable permissions
RUN chmod +x start.sh

# Expose server port
EXPOSE 8000

# Set environment defaults
ENV PORT=8000
ENV HOST=0.0.0.0
ENV CHROMA_PERSIST_DIR=/workspace/data/index

# Start command
CMD ["./start.sh"]
