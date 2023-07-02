# FROM fetalheadsegalgorithm_base:latest
FROM python:3.9.15

RUN useradd -s /bin/bash algorithm

USER algorithm

WORKDIR /opt/algorithm

ENV PATH="/home/algorithm/.local/bin:${PATH}"

COPY --chown=algorithm:algorithm requirements.txt /opt/algorithm/
COPY --chown=algorithm:algorithm model/ /opt/algorithm/model/
COPY --chown=algorithm:algorithm test/ /opt/algorithm/test/
COPY --chown=algorithm:algorithm model_weights/ /opt/algorithm/model_weights/
COPY --chown=algorithm:algorithm utils/ /opt/algorithm/utils/
COPY --chown=algorithm:algorithm process.py /opt/algorithm/
COPY --chown=algorithm:algorithm segmentation.py /opt/algorithm/

RUN python3 -m pip install --user -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ENTRYPOINT python3 -m process $0 $@

LABEL nl.diagnijmegen.rse.algorithm.name=seg_algorithm

