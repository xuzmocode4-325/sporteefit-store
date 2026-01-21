##############################################
# Stage 1: Node Build (only used in production)
##############################################
FROM node:20-alpine AS build
WORKDIR /frontend

ARG DEV=false
ENV NODE_ENV=development

# Copy only lockfile & package manifest first for better caching
COPY frontend/package*.json ./

# Install minimal build tools and git for native modules or git-based deps
RUN apk add --no-cache git python3 make g++ \
    && npm ci --no-audit --no-fund

# Copy frontend source
COPY frontend .

# Set API URL for production build (use relative path so it goes through proxy)
ENV VITE_API_URL=/api

RUN if [ "$DEV" != "true" ]; then \
        echo "Building production frontend..."; \
        npm run build; \
    else \
        echo "Skipping build (DEV mode)"; \
    fi

##############################################
# Stage 2: Nginx Proxy (used in both modes)
##############################################
FROM nginx:alpine
ARG DEV=false
ENV DEV=${DEV}
ENV BACKEND_HOST=zonke-backend
ENV BACKEND_PORT=8000

# Copy template and startup script
COPY ./proxy/nginx.conf.template /etc/nginx/templates/default.conf.template

# Copy built frontend if it exists
COPY --from=build /frontend/dist* /usr/share/nginx/html 

# Show placeholder HTML in dev mode
RUN if [ "$DEV" = "true" ]; then \
        echo "Running in DEV mode (proxy only)" && \
        rm -rf /usr/share/nginx/html/* && \
        echo '<h1>Proxy Container (DEV Mode)</h1><p>Frontend runs at http://localhost:5173</p>' > /usr/share/nginx/html/index.html; \
    fi

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
