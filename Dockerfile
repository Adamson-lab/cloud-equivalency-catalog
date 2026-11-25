FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
COPY catalog ./catalog
COPY schema ./schema
RUN pip install --no-cache-dir .
ENV CLOUDEQUIV_CATALOG=/app/catalog
ENTRYPOINT ["cloudequiv"]
CMD ["stats"]
