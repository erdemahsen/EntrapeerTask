FROM ubuntu:22.04

# Update package list and install dependencies
RUN apt-get update && \
    apt-get install -y \
        sudo \
        build-essential \
        software-properties-common \
        byobu curl git htop man unzip vim wget \
        python3 python3-pip \
        net-tools dnsutils inetutils-ping iproute2 \
        rabbitmq-server && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV HOME /root
WORKDIR /root

# Copy application code and install dependencies
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN python3 -m spacy download en_core_web_md

# Start RabbitMQ as a service
CMD service rabbitmq-server start && sleep infinity
