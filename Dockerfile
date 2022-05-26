FROM python:3.8-bullseye as builder

RUN pip install --user -i https://pypi.tuna.tsinghua.edu.cn/simple pipenv
ENV PIPENV_VENV_IN_PROJECT=1
ADD Pipfile.lock Pipfile /usr/src/
WORKDIR /usr/src
RUN /root/.local/bin/pipenv sync

FROM python:3.8-bullseye

RUN mkdir -v /usr/src/venv
COPY --from=builder /usr/src/.venv/ /usr/src/venv/
RUN useradd -s /sbin/nologin word

COPY . /usr/src
WORKDIR /usr/src/
USER word
EXPOSE 8000
CMD ["/usr/src/venv/bin/python", "server.py"]