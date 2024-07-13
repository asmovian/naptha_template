#!/usr/bin/env python
from template.schemas import InputSchema
from naptha_sdk.utils import get_logger, load_yaml
import chromadb
import json


logger = get_logger(__name__)

def run(inputs: InputSchema, worker_nodes=None, orchestrator_node=None, flow_run=None, cfg=None):
    logger.info(f"Inputs: {inputs}")

    client = chromadb.PersistentClient(path=inputs.input_dir)
    collection_name = "roko-telegram"

    collections = client.list_collections()
    existing_collection_names = [x.name for x in collections]
    if collection_name in existing_collection_names:
        collection = client.get_collection(name=collection_name)
        num = f"{collection_name} has {collection.count()} entries"
        logger.info(num)

        r = collection.query(query_texts=inputs.question, n_results=5)
        ret_str = json.dumps(r["documents"], indent=2)
    else:
        ret_str = f"Error: Collection {collection_name} not found."

    logger.debug(ret_str)

    return ret_str


if __name__ == "__main__":

    cfg_path = "template/component.yaml"
    cfg = load_yaml(cfg_path)

    inputs = InputSchema(
        question="Where should I store my Roko coin?",
        input_dir="/home/julien/data/naptha/roko-chromadb"
    )
    run(inputs, cfg=cfg)