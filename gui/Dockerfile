FROM alpine:latest
RUN mkdir -p /app
WORKDIR /app
COPY . .
RUN apk add nodejs npm
RUN npm install
EXPOSE 3000
CMD ["npm", "run", "dev", "--", "--host=0.0.0.0"]