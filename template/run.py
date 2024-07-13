#!/usr/bin/env python
from template.schemas import InputSchema
from naptha_sdk.utils import get_logger, load_yaml
import chromadb
import asyncio
import ollama
from ollama import Client

logger = get_logger(__name__)

def run(inputs: InputSchema, worker_nodes=None, orchestrator_node=None, flow_run=None, cfg=None):
    logger.info(f"Inputs: {inputs}")
    logger.debug(f"config = {cfg}")

    client = chromadb.PersistentClient(path=inputs.input_dir)
    collection_name = cfg["chroma"]["collection"]

    # Set the prompt
    messages = [
        {"role": "system", "content": cfg["inputs"]["system_message"]}
    ]

    collections = client.list_collections()
    existing_collection_names = [x.name for x in collections]
    if collection_name in existing_collection_names:
        collection = client.get_collection(name=collection_name)
        num = f"{collection_name} has {collection.count()} entries"
        logger.info(num)

        # put vector db results into query:
        results = collection.query(query_texts=inputs.question, n_results=10)
        for doc in results["documents"][0]:
            messages.append({"role": "assistant", "content": doc})

    else:
        logger.warning(f"Error: Collection {collection_name} not found.")

    messages.append({"role": "user", "content": inputs.question})

    logger.debug(messages)

    ollama_client = Client(host=cfg["models"]["ollama"]["api_base"])
    response = ollama_client.chat(
        model=cfg["models"]["ollama"]["model"], 
        messages=messages
    )

    logger.debug(response)

    return response


if __name__ == "__main__":

    cfg_path = "template/component.yaml"
    cfg = load_yaml(cfg_path)

    # Note: this is for local testing only. When running on naptha
    # it may look like this: first you need to upload the vector db with
    # the chunked data:
    # $ naptha write_storage -i chromadb.zip
    # -> storage id for file system = <id>: i.e. something like 1caddaae8ca5495c996db80e33e42da9
    # Now run the query:
    # $ naptha run template -p "question='Where should I store my Roko coins?' input_dir='<id>'"

    inputs = InputSchema(
        question="Where should I store my Roko coin?",
        input_dir="/home/julien/data/naptha/roko-chromadb"
    )
    run(inputs, cfg=cfg)