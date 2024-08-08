FROM node:18-alpine as builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
CMD ["npm", "run", "start"] 

# # --- Use Node.js to Serve ---
# FROM node:18-alpine

# WORKDIR /app/dist

# # Copy built files
# COPY --from=builder /app/dist .

# # Expose port 8080
# EXPOSE 8080

# CMD ["npm", "run", "start"]

# # Health Check (optional)
# HEALTHCHECK --interval=5s --timeout=3s --retries=3 \
# CMD curl --fail http://localhost:8080/healthz 