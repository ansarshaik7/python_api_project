#!/bin/bash
set -e

# -----------------------------
# Install and start HTTPD
# -----------------------------
SERVICE_NAME="httpd"

if systemctl is-active --quiet "$SERVICE_NAME"; then
    echo "$SERVICE_NAME is already installed and running."
else
    echo "$SERVICE_NAME is not running. Installing/starting..."
    sudo yum install -y "$SERVICE_NAME"
    sudo systemctl start "$SERVICE_NAME"
    sudo systemctl enable "$SERVICE_NAME"
    echo "$SERVICE_NAME has been installed and started."
fi


# -----------------------------
# Install and start Docker
# -----------------------------
SERVICE_NAME="docker"

if systemctl is-active --quiet "$SERVICE_NAME"; then
    echo "$SERVICE_NAME is already installed and running."
else
    echo "$SERVICE_NAME is not running. Installing/starting..."
    sudo yum install -y "$SERVICE_NAME"
    sudo systemctl start "$SERVICE_NAME"
    sudo systemctl enable "$SERVICE_NAME"
    sudo usermod -aG docker "$USER"
    echo "$SERVICE_NAME has been installed and started."
fi

docker --version

# -----------------------------
# Install Git
# -----------------------------
SERVICE_NAME="git"

if command -v "$SERVICE_NAME" &> /dev/null; then
    echo "$SERVICE_NAME is already installed."
else
    echo "$SERVICE_NAME is not installed. Installing..."
    sudo yum install -y "$SERVICE_NAME"
    echo "$SERVICE_NAME has been installed."
fi

git --version

# -----------------------------
# Install kubectl
# -----------------------------
SERVICE_NAME="kubectl"

if command -v "$SERVICE_NAME" &> /dev/null; then
    echo "$SERVICE_NAME is already installed."
else
    echo "$SERVICE_NAME is not installed. Installing..."

    if [ "$(uname -m)" = "x86_64" ]; then
        curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.36.2/2026-07-05/bin/linux/amd64/kubectl
    else
        echo "Unsupported architecture: $(uname -m)"
        exit 1
    fi

    chmod +x ./kubectl

    mkdir -p "$HOME/bin"
    cp ./kubectl "$HOME/bin/kubectl"

    if ! grep -q 'export PATH=$HOME/bin:$PATH' "$HOME/.bashrc"; then
        echo 'export PATH=$HOME/bin:$PATH' >> "$HOME/.bashrc"
    fi

    export PATH="$HOME/bin:$PATH"

    rm -f ./kubectl

    echo "$SERVICE_NAME has been installed."
fi


kubectl version --client

# -----------------------------
# Install Kind
# -----------------------------
SERVICE_NAME="kind"

if command -v "$SERVICE_NAME" &> /dev/null; then
    echo "$SERVICE_NAME is already installed."
else
    echo "$SERVICE_NAME is not installed. Installing..."

    if [ "$(uname -m)" = "x86_64" ]; then
        curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.33.0/kind-linux-amd64
    else
        echo "Unsupported architecture: $(uname -m)"
        exit 1
    fi

    chmod +x ./kind
    sudo mv ./kind /usr/local/bin/kind

    echo "$SERVICE_NAME has been installed."
fi

kind version

# -----------------------------
# Create Kind cluster
# -----------------------------
CLUSTER_NAME="kind2"

if kind get clusters | grep -qx "$CLUSTER_NAME"; then
    echo "Kind cluster $CLUSTER_NAME already exists."
else
    echo "Kind cluster $CLUSTER_NAME does not exist. Creating..."

    kind create cluster --name "$CLUSTER_NAME"

    echo "Kind cluster $CLUSTER_NAME has been created."
fi

kind get clusters

kubectl cluster-info --context kind-"$CLUSTER_NAME"

kubectl get nodes --context kind-"$CLUSTER_NAME"