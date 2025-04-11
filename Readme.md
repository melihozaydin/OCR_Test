------------------------------------------------------
Requirements:
https://docs.docker.com/engine/install/ubuntu/
--- 
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

# Install the Docker packages.

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo docker run hello-world
---

--- sudo apt install docker-compose

------------------------------------------------------
------------------------------------------------------
Add the NVIDIA Container Toolkit repository:
------------------------------------------------------

bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# Update the package list:
bash
sudo apt-get update

# Install the NVIDIA Container Toolkit:
bash
sudo apt-get install -y nvidia-container-toolkit

# Configure Docker to use the NVIDIA runtime:
bash
sudo nvidia-ctk runtime configure --runtime=docker

# Restart the Docker service:
bash
sudo systemctl restart docker

# Verify the installation:
bash
    docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
    This should display your GPU info, confirming the toolkit is working.

# Prerequisites

    NVIDIA GPU with compatible driver installed (check with nvidia-smi).
    Docker installed (e.g., via sudo apt install docker.io).
    Root or sudo access.

------------------------------------------------------
Build the Docker image:

bash
docker build -t olmocr:latest .

    Start the service with docker-compose:

bash
docker-compose up -d

    Get inside the running container:

bash
docker exec -it olmocr bash

    Run the example inside the container:

bash
python -m olmocr.pipeline ./localworkspace --pdfs tests/gnarly_pdfs/horribleocr.pdf

    To stop the service later:

bash
docker-compose down
------------------------------------------------------
Make sure you're in the directory containing your Dockerfile and docker-compose.yml before running these commands. Also ensure Docker and NVIDIA Container Toolkit are installed on your system.


Place your PDF in the local folder /appdata/olmocr/localworkspace on your host machine.

python -m olmocr.pipeline localworkspace --max_page_error_rate 0.5 --pdfs localworkspace/nihat_books/Cropped_2.pdf
********
sudo docker cp bbc336c4a9ce:/app/olmocr/.localworkspace/results ./results/
Successfully copied 1.01MB to /home/melihozaydin/Desktop/OCR_Test/results/
