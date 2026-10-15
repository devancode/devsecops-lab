FROM jenkins/jenkins:lts-jdk21

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 python3-venv python3-pip git curl ca-certificates nodejs npm && \
    rm -rf /var/lib/apt/lists/*

USER jenkins

RUN git config --global --add safe.directory '*'

RUN jenkins-plugin-cli --plugins \
    workflow-aggregator git pipeline-stage-view warnings-ng \
    htmlpublisher junit credentials-binding timestamper ws-cleanup