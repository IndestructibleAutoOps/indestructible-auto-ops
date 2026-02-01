FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    python-docx \
    pyyaml \
    jsonschema \
    markdownify

COPY convert.py /app/convert.py

ENTRYPOINT ["python", "/app/convert.py"]
