FROM gcr.io/distroless/python3-debian12:nonroot

RUN pip3 install gevent

ENV PATH="/venv/bin:$PATH"
ENV PYTHONUSERBASE=/venv

COPY venv /venv

COPY app/ /usr/src/
WORKDIR /usr/src/
EXPOSE 8000
USER nonroot
CMD ["python", "server.py"]