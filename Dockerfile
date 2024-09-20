FROM gcr.io/distroless/python3-debian12:nonroot

ENV PATH="/venv/bin:$PATH"
ENV PYTHONPATH=/venv/site-packages

COPY venv/lib/python3.11/site-packages /venv/site-packages

COPY app /usr/src/app/
WORKDIR /usr/src/app
EXPOSE 8000
USER nonroot
CMD ["server.py"]