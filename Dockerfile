# Step 1: Build stage
FROM python:3.9-slim as builder
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Step 2: Production stage
FROM python:3.9-slim
WORKDIR /app

# Copy dependencies and source code
COPY --from=builder /root/.local /root/.local
COPY . .

# Update PATH for locally installed packages
ENV PATH=/root/.local/bin:$PATH

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose the port
EXPOSE 5000

# ADD HEALTHCHECK
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:5000/ || exit 1

# Start the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
