# 🎬 Movie Mate

> *App for movie recommendations, user insights, and cutting-edge microservices tech.*

---
[![build](https://img.shields.io/github/actions/workflow/status/mankis-movie-mate/mm-infrastructure/deploy.yml?branch=main&logo=github)](https://github.com/mankis-movie-mate/mm-infrastructure/actions)
[![license](https://img.shields.io/github/license/mankis-movie-mate/.github?color=blue)](LICENSE)
[![made-with-k8s](https://img.shields.io/badge/Kubernetes-ready-blue?logo=kubernetes)](docs/k8s)
[![openapi-hub](https://img.shields.io/badge/OpenAPI-Hub-green?logo=swagger)](https://github.com/mankis-movie-mate/mm-openapi-hub)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-pink.svg)](#-contributing)


> **Movie Mate** is a full-stack, polyglot platform that delivers personalised movie recommendations with **Dapr sidecars**, **Kafka**, and **end-to-end observability**.  
> Deployed on **Kubernetes** (k3s or full k8s). _Security first_ via **JWT** at the edge.
---

## 🔎 Table of Contents
1. 🏗️ [System Overview](#️-system-overview)
2. 📚 [Tech Stack](#-tech-stack)
3. 🧠 [Microservices](#-microservices)
4. 🛠️ [Platform & Utilities](#-platform--utilities)
5. 🔒 [JWT Auth Flow](#-jwt-auth-flow)
6. 🌐 [Observability](#-observability-first)
7. 🗺️ [Roadmap](#-roadmap)


---

## 🏗️ System Overview
![Movie Mate Architecture](../docs/movie-mate-architecture.png)

---

## 📚 Tech Stack
| Layer | Tech                                                 |
|---|------------------------------------------------------|
| **Frontend** | React, TypeScript, Next.js, Tailwind                 |
| **API Gateway** | Traefik + Consul (service discovery)                 |
| **Microservices** | Java • Node.js • Kotlin • Python                     |
| **Communication** | Dapr Sidecars • Kafka Pub/Sub • REST                 |
| **Databases** | PostgreSQL • MongoDB • Redis • Neo4j                 |
| **Observability** | Prometheus • Loki • Zipkin • OpenTelemetry • Grafana |
| **CI/CD** | GitHub Actions • Docker                              |
| **Platform** | **Kubernetes** (k3s)                                 |
| **Security** | JWT (validated by User Service via API Gateway)      |
| **Docs** | OpenAPI (aggregated in **mm-openapi-hub**)           |

---

## 🧠 Microservices
| Service                                                                                       | Purpose                                                    | Tech                                                                                                                                      |
| --------------------------------------------------------------------------------------------- | ---------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| [`mm-user-service`](https://github.com/mankis-movie-mate/mm-user-service)                     | Users & authentication                                     | ![Java](https://img.shields.io/badge/Java-17-blue?logo=java) ![Status](https://img.shields.io/badge/build-passing-brightgreen?style=flat) |
| [`mm-movie-service`](https://github.com/mankis-movie-mate/mm-movie-service)                   | Movies, genres, metadata                                   | ![Node.js](https://img.shields.io/badge/Node.js-18.x-green?logo=node.js)                                                                  |
| [`mm-recommendation-service`](https://github.com/mankis-movie-mate/mm-recommendation-service) | Recommendation engine (consumes activity & catalog events) | ![Kotlin](https://img.shields.io/badge/Kotlin-1.9-blueviolet?logo=kotlin)                                                                 |
| [`mm-activity-service`](https://github.com/mankis-movie-mate/mm-activity-service)             | Tracks user actions across services                        | ![Python](https://img.shields.io/badge/Python-3.11-yellow?logo=python)                                                                    |
| [`mm-api-gateway`](https://github.com/mankis-movie-mate/mm-api-gateway)                       | Single entrypoint; routing & rate limits                   | ![Gateway](https://img.shields.io/badge/Gateway-Traefik-orange?logo=traefikproxy)                                                         |
| [`mm-discovery-server`](https://github.com/mankis-movie-mate/mm-discovery-server)             | Service registration & discovery (Consul)                  | ![Consul](https://img.shields.io/badge/Discovery-Consul-red?logo=consul)                                                                  |


---

## 🛠️ Platform & Utilities
| Repo                                                                          | Description                                   | Tech                                                                                                                                                                        |
|-------------------------------------------------------------------------------|-----------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [`mm-app-view`](https://github.com/mankis-movie-mate/mm-infrastructure)       | Frontend                                      | ![React](https://img.shields.io/badge/React-✔️-blue?logo=react) ![Next.js](https://img.shields.io/badge/Next.js-informational?logo=nextjs)                                  |
| [`mm-infrastructure`](https://github.com/mankis-movie-mate/mm-infrastructure) | IaC, manifests, CI/CD pipeline for deployment | ![CI/CD](https://img.shields.io/badge/GitHub%20Actions-✔️-blue?logo=githubactions) ![Kubernetes](https://img.shields.io/badge/Kubernetes-k3s-informational?logo=kubernetes) |
| [`mm-openapi-hub`](https://github.com/mankis-movie-mate/mm-openapi-hub)       | Centralised Swagger UI for all services       | ![Swagger UI](https://img.shields.io/badge/OpenAPI-Swagger-green?logo=swagger)                                                                                              |



## 🔒 JWT Auth Flow

> **One way in**: the API Gateway is your bouncer; **User Service** is the ID checker.

```mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant G as Traefik (API Gateway)
    participant U as mm-user-service
    participant S as Target Service

    C->>G: HTTP request + Authorization: Bearer <JWT>
    G->>U: Introspect/validate JWT
    U-->>G: 200 OK (claims) / 401 Unauthorized
    alt token valid
        G->>S: Forward original request (with verified identity)
        S-->>G: Response
        G-->>C: Response
    else invalid
        G-->>C: 401 Unauthorized
    end
```

## 🌐 Observability First

Everything is observable out of the box. Metrics, traces, and logs in real time using:

- 📈 **Prometheus**: Metrics collection
- 🧠 **Grafana**: Unified dashboards
- 🔍 **Loki**: Log aggregation
- 🛰️ **Zipkin**: Distributed tracing
- 📡 **OpenTelemetry Collector**: Unified observability pipeline


## 🗺️ Roadmap

Planned and upcoming features for **Movie Mate** — both for dev experience and user functionality:

### 🎯 Core Features
- 🖼️ **Frontend App**: React + Next.js SPA for browsing movies and managing account
- 🔐 **RBAC & Multi-tenancy**: Role-based access control 
- 🚩 **Feature Flags**: Fine-grained control with [Unleash](https://www.getunleash.io/) for toggling features live
- ✅ **End-to-End Testing**: CI-based tests using [KinD](https://kind.sigs.k8s.io/) + GitHub Actions for full cluster testing

### 🚀 DevOps / Platform
- 🌀 **Canary Releases**: Progressive delivery with [Argo Rollouts](https://argoproj.github.io/argo-rollouts/)
- 🔍 **Zero-Downtime Observability**: Auto instrument new services with OTEL SDKs