# ---------- Builder ----------
FROM python:3.11-slim AS builder
WORKDIR /opt/app
ENV PYTHONUNBUFFERED=1
COPY pyproject.toml requirements.txt ./
RUN pip install --upgrade pip && pip install --user -r requirements.txt

# ---------- Runtime ----------
FROM python:3.11-slim
WORKDIR /opt/app
ENV PYTHONUNBUFFERED=1
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY . .
RUN chmod +x scripts/*.sh

HEALTHCHECK CMD ["/opt/app/scripts/healthcheck.sh"]
CMD ["python", "examples/news_summarization.py"]

