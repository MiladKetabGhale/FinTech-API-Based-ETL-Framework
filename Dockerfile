# Use slim Python 3.10 base image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Add metadata (optional but helpful)
LABEL maintainer="milad.ketabi@alumni.anu.edu.au"
LABEL description="Core MLOps pipeline with shared components and common tests"
LABEL version="1.0"

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy core project code
COPY main.py ./
COPY core ./core
COPY interfaces ./interfaces
COPY Error_Handling ./Error_Handling

# Copy reusable test logic
COPY tests/ingestion ./tests/ingestion
#COPY tests/validation ./tests/validation                   once you add general validation or transformation tests, uncomment these lines
#COPY tests/transformation ./tests/transformation

# Create empty mountable folders so Docker doesn't ignore them
RUN mkdir -p /app/plugins \
    && mkdir -p /app/tests/test_plugins

# Ensure Python can find mounted modules
ENV PYTHONPATH="/app"

# Default to running all tests
ENV PLUGIN_NAME=""

# Entrypoint with conditional execution
# add tests/validation and tests/transformation to the list once the folders have some general tests inside them
ENTRYPOINT ["sh", "-c", "pytest tests/ingestion tests/test_plugins/test_${PLUGIN_NAME}"]
