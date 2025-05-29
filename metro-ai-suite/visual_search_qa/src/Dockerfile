# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

FROM python:3.11-slim

ENV LANG=C.UTF-8

ARG ARCH="gpu"

RUN apt-get update -y && apt-get install -y --no-install-recommends --fix-missing libgl1-mesa-glx libglib2.0-0 build-essential ca-certificates wget curl

RUN useradd -m -s /bin/bash user && \
mkdir -p /home/user && \
chown -R user /home/user/

COPY visual_search_qa /home/user/visual_search_qa
RUN chown -R user /home/user/visual_search_qa

RUN pip install --no-cache-dir --upgrade pip setuptools && \
    pip install --no-cache-dir -r /home/user/visual_search_qa/src/requirements.txt

ENV PYTHONPATH=$PYTHONPATH:/home/user

RUN mkdir -p /home/user/data && chown -R user /home/user/data

USER user

EXPOSE 17580

WORKDIR /home/user/visual_search_qa/src

CMD ["streamlit", "run", "app.py", "--server.port", "17580", "--server.headless", "true"]