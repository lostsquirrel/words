FROM python:3.11 as builder

RUN useradd --uid 1002 --shel /bin/bash --home-dir /home/nonroot --create-home nonroot
USER nonroot
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --user pipenv
ENV PIPENV_VENV_IN_PROJECT=1
ENV PATH="$PATH:/home/nonroot/.local/bin"
ADD Pipfile.lock Pipfile /home/nonroot/
WORKDIR /home/nonroot
RUN ls -la .local/bin
RUN pipenv install --dev


FROM gcr.io/distroless/python3-debian12:nonroot

ENV PATH="/venv/bin:$PATH"
ENV PYTHONPATH=/venv/site-packages

COPY --from=builder /home/nonroot/.venv/lib/python3.11/site-packages /venv/site-packages

COPY . /usr/src/app/
WORKDIR /usr/src/app
EXPOSE 8000
USER nonroot
CMD ["server.py"]