#!/usr/bin/env python
from template.schemas import InputSchema
from naptha_sdk.utils import get_logger, load_yaml
import chromadb


logger = get_logger(__name__)

def run(inputs: InputSchema, worker_nodes=None, orchestrator_node=None, flow_run=None, cfg=None):
    logger.info(f"Inputs: {inputs}")

    client = chromadb.PersistentClient(path=inputs.input_dir)
    collection_name = "roko-telegram"
    collection = client.get_collection(name=collection_name)
    num = f"{collection_name} has {collection.count()} entries"
    logger.info(num)

    # try to read the 
    # with open(f"{inputs.input_dir}/ftest.txt", "r") as fp:
        #line = fp.readline()

    return num


if __name__ == "__main__":

    cfg_path = "template/component.yaml"
    cfg = load_yaml(cfg_path)

    inputs = InputSchema(
        question="question",
        input_file="4bf5d447ecc749a5b3d42c50b27c8ce0",
    )
    run(inputs, cfg=cfg)