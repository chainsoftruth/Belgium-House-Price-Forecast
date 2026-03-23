FROM mambaorg/micromamba:2.0

WORKDIR /app

COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml .

RUN micromamba install -y -n base -f environment.yml && \
    micromamba clean --all --yes

COPY --chown=$MAMBA_USER:$MAMBA_USER . .

ARG MAMBA_DOCKERFILE_ACTIVATE=1

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-7777}"]