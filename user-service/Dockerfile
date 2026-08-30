#--------FIRST STAGE: BUILDING THE APPLICATION--------
# From base Image
FROM python:3.10-alpine AS builder
# Set the working directory
WORKDIR /app
# Create virtual environments
RUN python -m venv /opt/venv
# Set the PATH environment variable to include the local bin directory
ENV PATH=/opt/venv/bin:$PATH
# Copy the requirements file into the image
COPY requirements.txt .
# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

#--------SECOND STAGE: CREATING THE FINAL IMAGE--------
FROM python:3.10-alpine AS final
# Set the working directoryss
WORKDIR /app
# Copy the installed dependencies from the builder stage
COPY --from=builder /opt/venv /opt/venv
# Set the PATH environment variable to include the local bin directory
COPY app.py database.py models.py ./
# Set the PATH environment variable to include the local bin directory
ENV PATH=/opt/venv/bin:$PATH
# Expose the port that the application will run on
EXPOSE 8000
# Set the command to run the application using uvicorns
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"] 
