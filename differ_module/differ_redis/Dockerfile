FROM redis:8.0-M04-alpine3.21

EXPOSE 6379
HEALTHCHECK --interval=5s --timeout=3s --retries=3 \
    CMD redis-cli PING | grep -q "PONG" || exit 1
