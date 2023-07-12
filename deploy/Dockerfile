# Pre-stage
# Get frontend repo
FROM alpine/git:latest as repo
WORKDIR /frontend
# RUN git clone https://github.com/Yushkevich-A-A/nn_apartments.git --branch dev --single-branch
COPY ./frontend ./

# The first stage
# Build React static files
FROM node:18-alpine as build

WORKDIR /app/frontend
COPY --from=repo /frontend/nn_apartments/package*.json ./
RUN npm install

COPY --from=repo /frontend/nn_apartments/ ./
# COPY /apartmentsNN/.env ./
RUN npm run build

# The second stage
# Copy React static files and start nginx
FROM nginx:stable-alpine
COPY --from=build /app/frontend/build /build
CMD ["nginx", "-g", "daemon off;"]
