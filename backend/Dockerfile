# FROM python:3.11-buster

# RUN mkdir app
# WORKDIR /app

# ENV PATH="${PATH}:/root/.local/bin"
# ENV PYTHONPATH=.

# COPY requirements.txt .
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

# COPY src/ .
# --platform=windows/amd64
FROM  continuumio/miniconda3

WORKDIR /app
ADD environment.yml /tmp/environment.yml

RUN conda env create -f /tmp/environment.yml

RUN echo "source activate $(head -1 /tmp/environment.yml | cut -d' ' -f2)" > ~/.bashrc
ENV PATH /opt/conda/envs/$(head -1 /tmp/environment.yml | cut -d' ' -f2)/bin:$PATH