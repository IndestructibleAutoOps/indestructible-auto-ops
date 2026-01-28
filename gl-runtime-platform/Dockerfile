FROM node:20-alpine

# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: docker-build-configuration
# @GL-charter-version: 2.0.0

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy source code
COPY . .

# Build TypeScript
RUN npm run build

# Create storage directories
RUN mkdir -p storage/gl-events-stream \
         storage/gl-artifacts \
         storage/gl-audit-reports \
         storage/logs \
         ops/pipelines

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

# Start application
CMD ["npm", "start"]