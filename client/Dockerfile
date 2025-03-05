# Build stage
FROM node:20-alpine AS base

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source files
COPY ../. .

# Build the application
RUN npm run build

CMD cd /app/src
CMD npm run dev


# Production stage
FROM base AS frontend

WORKDIR /app

# Install serve for production static file serving
RUN npm install -g serve

# Copy built files from builder stage
COPY --from=base /app/client /app/dist /app/agent_ops /app/

# Expose port 5000 to match the app's configuration
EXPOSE 5000

# Start the application
CMD ["serve", "-s", "dist", "-l", "5000"]
