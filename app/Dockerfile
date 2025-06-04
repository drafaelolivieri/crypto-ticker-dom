FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/app.py .
COPY src/instrumentation.py .
COPY src/test_app.py .
COPY src/templates ./templates/

ENV PORT=8080
ENV ENVIRONMENT=staging
ENV MB_LOGIN=b131d9c70e9a73e299a53203b50289f4dc2b2a1e41780c810ebcabd83da5d011
ENV MB_PASSWORD=daf39bec7a6ef9fc61304bea46db3be769b872600535052c59e2a3e1648ff09b

EXPOSE 8080

CMD ["python", "app.py"] 