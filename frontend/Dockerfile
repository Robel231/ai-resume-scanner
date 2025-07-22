# frontend/Dockerfile

# Use a specific, stable version of Node on Alpine Linux for a small image size.
FROM node:20-alpine

# Set the working directory inside the container.
WORKDIR /app

# Copy the package.json and the lock file.
# The '*' handles both package-lock.json (npm) and yarn.lock (yarn).
COPY package.json package-lock.json* ./

# Install dependencies. 'npm ci' is preferred for CI/CD as it's faster
# and respects the lock file, ensuring reproducible builds.
RUN npm install

# Copy the rest of the application's code into the container.
# This will be overwritten by the volume mount in docker-compose for development,
# but it's essential for building a standalone production image.
COPY . .

# The Next.js server runs on port 3000 by default.
EXPOSE 3000

# The command to start the app will be provided by docker-compose.yml.
# We can add a default command here as a fallback.
CMD ["npm", "run", "dev"]