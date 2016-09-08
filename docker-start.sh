# Start travel microservice in Docker with 8080 port
# docker run -p 8080:8080 -it --rm --name travel-app menangen/falcon-app
docker run -d -p 8080:8080 --name falcon-service --link some-postgres:postgres -d menangen/falcon-app