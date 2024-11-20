FROM otel/opentelemetry-collector:0.111.0

COPY otel-collector-config.yml /etc/otel-collector-config.yml

CMD ["--config=/etc/otel-collector-config.yml"]