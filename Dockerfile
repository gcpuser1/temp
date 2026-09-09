FROM python:3.12-slim
WORKDIR /app
COPY agent_runtime ./agent_runtime
USER 65532:65532
ENV PORT=8080
EXPOSE 8080
CMD ["python", "-m", "agent_runtime.api"]
