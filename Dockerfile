# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install uv, the package installer used in this project
RUN pip install uv

# Copy dependency definition files
COPY pyproject.toml ./

# Create a virtual environment
RUN uv venv

# Activate the virtual environment for all subsequent commands by adding it to the PATH
ENV PATH="/app/.venv/bin:$PATH"

# Install dependencies into the virtual environment
RUN uv pip sync --no-cache pyproject.toml

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Define the command to run the application with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"]
