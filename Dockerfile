FROM nvidia/cuda:12.1.0-devel-ubuntu22.04

# Set the working directory in the container
WORKDIR /app

ARG DEBIAN_FRONTEND=noninteractive

# curl is needed to download get-pip.py
# software-properties-common is needed for add-apt-repository
# We get python 3.11 from the deadsnakes PPA to have the latest version
# We install pip from the get-pip.py script to have the latest version
RUN apt-get update \
  && apt-get upgrade -y \
  && apt-get install -y \
  git curl \
  software-properties-common \
  && add-apt-repository ppa:deadsnakes/ppa \
  && rm -rf /var/lib/apt/lists/*

RUN apt-get remove -y python* && apt autoremove -y

RUN apt-get update \
  && apt install -y \
  python3.11 \
  python3.11-distutils \
  python3.11-dev \
  poppler-utils ttf-mscorefonts-installer \
  msttcorefonts \
  fonts-crosextra-caladea \
  fonts-crosextra-carlito \
  gsfonts \
  lcdf-typetools && \
  rm -rf /var/lib/apt/lists/*

RUN rm /usr/bin/python3 \
  && ln -s /usr/bin/python3.11 /usr/bin/python3 \
  && ln -s /usr/bin/python3.11 /usr/bin/python

RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# create the directory /app
RUN mkdir -p /app/olmocr
# Set the working directory to /app
WORKDIR /app
# clone the repository allenai/olmocr.git
RUN git clone https://github.com/allenai/olmocr.git
# Set the working directory to the cloned repository
WORKDIR /app/olmocr

# Install Python packages
RUN pip install -e .[gpu] --find-links https://flashinfer.ai/whl/cu124/torch2.4/flashinfer/

# Run a loop application to keep the container running
CMD ["bash", "-c", "while true; do sleep 30; done;"]
