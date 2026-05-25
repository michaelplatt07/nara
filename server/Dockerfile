FROM node:25-bookworm-slim
WORKDIR /usr/local/app

# Install the application dependencies
RUN apt update

# Copy in the source code
COPY server.ts server.ts
COPY middleware.ts middleware.ts
COPY db.ts db.ts
COPY src/ src/
COPY package.json package.json
COPY package-lock.json package-lock.json
EXPOSE 3000

RUN npm install

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

CMD ["npm", "run", "dev"]

