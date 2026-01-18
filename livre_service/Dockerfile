# Use official Node.js LTS image
FROM node:18-slim

# Create app directory
WORKDIR /app

# Install system dependencies if needed (for pg)
RUN apt-get update && apt-get install -y build-essential

# Copy package files and install deps
COPY package*.json ./
RUN npm install --production

# Copy source code
COPY . .

# Expose app port
EXPOSE 8080

# Start the app
CMD ["npm", "start"]