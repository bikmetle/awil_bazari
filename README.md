## Trying it out

A [`run_backend.sh`](./run_backend.sh) utility is provided for quickly building the image and starting a container, using bind mounts for the project and virtual environment directories.

To build and run the web application in the container using `docker run`:

```console
$ ./run_backend.sh
```

To build and run the web application using `docker compose`:

```console
docker compose up --watch 
```

## Useful commands

To check that the environment is up-to-date after image builds:

```console
$ ./run_backend.sh uv sync --frozen
```

To enter a `bash` shell in the container:

```console
$ ./run_backend.sh /bin/bash
```

To build the image without running anything:

```console
$ docker build .
```

To build the multistage image:

```console
$ docker build . --file multistage.Dockerfile
```

# docker stuff
## install docker
```console
sudo apt update && sudo apt install apt-transport-https curl -y && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null && sudo apt update && sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
```

### Verify Installation
```console
sudo systemctl is-active docker && sudo docker run hello-world
```

### Enabling Non-root Users to Run Docker
```console
sudo usermod -aG docker ${USER}
```

### See all Docker containers
```console
docker ps -a
```

### Delete all containers:

#### Stop all running containers
```console
docker stop $(docker ps -q)
```

#### Remove all containers
```console
docker rm $(docker ps -a -q)
```

### Delete all images:
```console
docker rmi $(docker images -q)
```
#### Remove unused data:
```console
docker system prune -a
```
