# CI/CD Pipeline with Jenkins, Docker, Prometheus and Grafana

## Project Overview

This project demonstrates a complete **DevOps CI/CD pipeline** for deploying an application using **Jenkins, Docker, Docker Hub, Prometheus, and Grafana**.

In this workflow, the **developer pushes code to GitHub**, then **Jenkins automatically pulls the latest code**, builds a **Docker image**, and pushes that image to **Docker Hub**. After that, the deployment server pulls the latest image, creates a **container**, and exposes the application to users.

For monitoring, **Prometheus** collects application and system metrics, and **Grafana** is used to visualize those metrics through dashboards.

---

## Workflow

1. Developer writes code and pushes it to GitHub.
2. Jenkins detects the changes in the repository.
3. Jenkins pulls the latest source code.
4. Jenkins builds a Docker image for the application.
5. Jenkins pushes the Docker image to Docker Hub.
6. The deployment server pulls the latest image from Docker Hub.
7. A Docker container is created and started.
8. The application is exposed to end users.
9. Prometheus collects monitoring metrics from the application and containers.
10. Grafana displays the collected metrics in dashboard form.

---

## Architecture

```text
Developer
   ↓
GitHub Repository
   ↓
Jenkins Pipeline
   ↓
Build Docker Image
   ↓
Push Image to Docker Hub
   ↓
Pull Image on Deployment Server
   ↓
Run Docker Container
   ↓
Expose Application to Users

Monitoring:
Prometheus --> Collect Metrics
Grafana --> Visualize Metrics
