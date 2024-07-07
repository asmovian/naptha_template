#!/usr/bin/env python
from template.schemas import InputSchema
from naptha_sdk.utils import get_logger, load_yaml


logger = get_logger(__name__)

def run(inputs: InputSchema, worker_nodes=None, orchestrator_node=None, flow_run=None, cfg=None):
    logger.info(f"Inputs: {inputs}")

    # try to read the 
    with open(inputs.input_file, "r") as fp:
        line = fp.readline()

    return line


if __name__ == "__main__":

    cfg_path = "template/component.yaml"
    cfg = load_yaml(cfg_path)

    inputs = InputSchema(
        question="question",
        input_file="af6058cca663479fba868e0d0b49a6df/ftest.txt",
    )
    run(inputs, cfg=cfg)