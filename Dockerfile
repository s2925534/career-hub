FROM python:3.12-slim

WORKDIR /srv/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

# CAREER_HUB_BIND_HOST / CAREER_HUB_HTTP_PORT are read at runtime by app.config;
# EXPOSE is documentation only, actual binding is controlled by env vars.
EXPOSE 8088

CMD ["python", "-m", "app.main"]
