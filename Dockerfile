FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STUDENT_NAME=Alisher \
    STUDENT_SURNAME=Panabaev \
    STUDENT_GROUP=It2-2308 \
    STUDENT_ID=37332

COPY app/server.py ./server.py

RUN adduser --system --uid 10001 --group appuser \
    && python -m py_compile /app/server.py

USER appuser

EXPOSE 8080

CMD ["python", "server.py"]
