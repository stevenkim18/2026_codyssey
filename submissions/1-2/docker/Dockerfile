FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install --no-install-recommends --yes \
        bash \
        ca-certificates \
        coreutils \
        file \
        gawk \
        iproute2 \
        procps \
        psmisc \
        util-linux \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --uid 10001 --shell /bin/bash agent-admin \
    && mkdir -p /opt/agent/bin /opt/agent/upload_files /opt/agent/api_keys /var/log/agent-app \
    && chown -R agent-admin:agent-admin /opt/agent /var/log/agent-app

COPY --chown=agent-admin:agent-admin app/agent-app-linux-arm64 /opt/agent/agent-app-linux-arm64
COPY --chown=agent-admin:agent-admin app/secret.key /opt/agent/api_keys/secret.key
COPY --chown=agent-admin:agent-admin monitor.sh /opt/agent/bin/monitor.sh

RUN chmod 0755 /opt/agent/agent-app-linux-arm64 /opt/agent/bin/monitor.sh \
    && chmod 0640 /opt/agent/api_keys/secret.key

ENV AGENT_HOME=/opt/agent \
    AGENT_PORT=15034 \
    AGENT_UPLOAD_DIR=/opt/agent/upload_files \
    AGENT_KEY_PATH=/opt/agent/api_keys \
    AGENT_LOG_DIR=/var/log/agent-app \
    MEMORY_LIMIT=512 \
    CPU_MAX_OCCUPY=10 \
    MULTI_THREAD_ENABLE=false

WORKDIR /opt/agent
USER agent-admin
EXPOSE 15034
ENTRYPOINT ["/opt/agent/agent-app-linux-arm64"]
