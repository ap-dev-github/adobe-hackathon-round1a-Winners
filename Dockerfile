# Stage 1: Install dependencies
FROM python:3.9-alpine AS builder
RUN apk add --no-cache gcc musl-dev
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime image
FROM python:3.9-alpine
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY pdf_outline_extractor.py .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "pdf_outline_extractor.py"]