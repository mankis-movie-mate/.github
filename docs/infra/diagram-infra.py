from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.network import Traefik, Consul
from diagrams.programming.language import Java, Kotlin, Python, NodeJS
from diagrams.programming.runtime import Dapr
from diagrams.onprem.client import Users
from diagrams.onprem.queue import Kafka
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.logging import Loki
from diagrams.generic.blank import Blank
from diagrams.custom import Custom
import os

def openapi_node():
    icon_path = os.path.join("assets", "openapi.png")
    if os.path.exists(icon_path):
        return Custom("OpenAPI Hub", icon_path)
    else:
        return Blank("OpenAPI Hub")

def otel_node():
    icon_path = os.path.join("assets", "otel.png")
    if os.path.exists(icon_path):
        return Custom("OTEL Collector", icon_path)
    else:
        return Blank("OTEL Collector")

def zipkin_node():
    icon_path = os.path.join("assets", "zipkin.png")
    if os.path.exists(icon_path):
        return Custom("Zipkin", icon_path)
    else:
        return Blank("Zipkin")

def create_microservices():
    svcs = {}
    with Cluster("MovieMate Microservices"):
        with Cluster("mm-user-service"):
            user_lang = Java("Java")
            user_dapr = Dapr("Dapr")
            svcs["user"] = {"lang": user_lang, "dapr": user_dapr}
        with Cluster("mm-movie-service"):
            movie_lang = NodeJS("Node.js")
            movie_dapr = Dapr("Dapr")
            svcs["movie"] = {"lang": movie_lang, "dapr": movie_dapr}
        with Cluster("mm-recommendation-service"):
            rec_lang = Kotlin("Kotlin")
            rec_dapr = Dapr("Dapr")
            svcs["rec"] = {"lang": rec_lang, "dapr": rec_dapr}
        with Cluster("mm-activity-service"):
            activity_lang = Python("Python")
            activity_dapr = Dapr("Dapr")
            svcs["activity"] = {"lang": activity_lang, "dapr": activity_dapr}
        with Cluster("mm-openapi-hub"):
            openapi = openapi_node()
            svcs["openapi"] = {"node": openapi}
    return svcs

def create_messaging():
    with Cluster("Messaging"):
        kafka = Kafka("Kafka/Redpanda")
    return {"kafka": kafka}

def create_observability():
    with Cluster("Observability"):
        prom = Prometheus("Prometheus")
        loki = Loki("Loki")
        graf = Grafana("Grafana")
        otel = otel_node()
        zipkin = zipkin_node()
    return {"prom": prom, "loki": loki, "graf": graf, "otel": otel, "zipkin": zipkin}

def create_api_edge():
    with Cluster("API Edge"):
        gateway = Traefik("mm-api-gateway\n(Traefik)")
        consul = Consul("mm-discovery-server\n(Consul)")
    return {"gateway": gateway, "consul": consul}

def create_edges(user, svcs, obs, api, msg):
    # User to Traefik (API Edge)
    user >> Edge(color="green", style="bold", label="HTTPS/REST") >> api["gateway"]

    # API Edge to *first* microservice (BOLD, labeled as "routes all")
    api["gateway"] >> Edge(color="black", style="bold", label="routes all microservices") >> svcs["user"]["lang"]

    # *One* line from first microservice node to Consul (labeled "register/health (all)")
    svcs["user"]["lang"] >> Edge(color="blue", style="bold", label="register/health (all)") >> api["consul"]

    # Dapr sidecars
    for k in ["user", "movie", "rec", "activity"]:
        svcs[k]["lang"] - Edge(style="dashed", color="gray", label="Dapr sidecar") - svcs[k]["dapr"]

    # Dapr → Kafka (messaging)
    svcs["activity"]["dapr"] >> Edge(label="publish activity-*") >> msg["kafka"]
    svcs["user"]["dapr"] >> Edge(label="publish user-events") >> msg["kafka"]
    svcs["movie"]["dapr"] >> Edge(label="publish catalog-events") >> msg["kafka"]
    svcs["rec"]["dapr"] << Edge(label="consume ratings/activity") << msg["kafka"]

    # Observability
    for k in ["user", "movie", "rec", "activity"]:
        svcs[k]["lang"] >> Edge(label="metrics/traces/logs") >> obs["otel"]
    obs["otel"] >> Edge(label="metrics") >> obs["prom"]
    obs["otel"] >> Edge(label="logs") >> obs["loki"]
    obs["otel"] >> Edge(label="traces") >> obs["zipkin"]
    obs["graf"] << Edge(label="dashboards") << obs["prom"]
    obs["graf"] << Edge(label="explore") << obs["loki"]
    obs["graf"] << Edge(label="traces") << obs["zipkin"]

    # OpenAPI hub connects to first microservice (label: "docs for all")
    openapi = svcs["openapi"]["node"]
    openapi - Edge(style="dotted", color="black", label="OpenAPI docs") - [
        svcs["user"]["lang"], svcs["movie"]["lang"], svcs["rec"]["lang"], svcs["activity"]["lang"]
    ]

def main():
    with Diagram("", show=False, outformat="png", direction="LR"):
        user = Users("User")
        svcs = create_microservices()
        msg = create_messaging()
        obs = create_observability()
        api = create_api_edge()
        create_edges(user, svcs, obs, api, msg)

if __name__ == "__main__":
    main()
