# Stage 1: Build Tailwind CSS with Node.js
FROM node:14 AS tailwind-build

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install npm dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the Tailwind CSS
RUN npx tailwindcss -i ./app/static/src/input.css -o ./app/static/dist/css/output.css

# Stage 2: Build the Flask application with Python
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code from the first stage
COPY --from=tailwind-build /app /app

# Expose the port the app runs on
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# Populate the database
RUN python populate_db.py

# Command to run the Flask app
CMD ["python", "run.py"]
