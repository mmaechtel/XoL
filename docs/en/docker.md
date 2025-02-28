### Installing [Docker](../glossary.md#docker) on Debian: A Step-by-Step Guide

[Docker](../glossary.md#docker) is a widely used platform for containerizing applications that helps developers and administrators efficiently create, deploy, and manage applications. This article explains how to install Docker on a system with Debian. The guide is factual and practice-oriented, making it easy to follow even for beginners.

## Prerequisites

Before you begin, ensure that:

- You have access to a Debian system
- You have root or sudo rights

## Step 1: Update System

First, ensure your Debian system is up to date. Open a terminal and execute these commands:

```bash
sudo apt update
sudo apt upgrade -y
```

This updates the package lists and installs available updates for already installed software.

## Step 2: Install Required Dependencies

Docker requires some basic packages to function correctly. Install these with:

```bash
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release
```

These packages enable secure software downloads and repository key management.

## Step 3: Add Docker Repository

While Debian includes an older version of Docker in its standard repository, it's recommended to use the official Docker repository to get the latest version. Follow these steps:

1. **Add GPG Key:**

   ```bash
   curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
   ```

2. **Set up Repository:**

   ```bash
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```

3. **Update Package Lists:**
   ```bash
   sudo apt update
   ```

## Step 4: Install Docker

Now you can install Docker. Execute the following command to install the main packages:

```bash
sudo apt install -y docker-ce docker-ce-cli containerd.io
```

- `docker-ce`: The Docker Engine itself.
- `docker-ce-cli`: The command-line interface.
- `containerd.io`: The container runtime used by Docker.

## Step 5: Start and Enable Docker Service

After installation, you need to start the Docker service and ensure it runs automatically at system startup:

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

## Step 6: Verify Installation

To ensure Docker was installed correctly, run this command:

```bash
docker --version
```

You should see output like `Docker version 20.10.x, build ...` (or a newer version). Also test if Docker works by starting a simple container:

```bash
sudo docker run hello-world
```

This command downloads a test image and runs it. If everything is working correctly, you'll receive a confirmation message from Docker.

## Step 7: Use Docker Without Root Rights (optional)

By default, Docker requires root rights. If you want to run Docker as a normal user, add your user to the `docker` group:

```bash
sudo usermod -aG docker $USER
```

Log out and back in (or restart the terminal) for the changes to take effect. After that, you can run Docker commands without `sudo`.

## Conclusion

You have now successfully installed Docker on Debian. With this installation, you can create containers, manage images, and run applications in isolated environments. If you need further adjustments or specific configurations, the [official Docker documentation](https://docs.docker.com) provides detailed information. 