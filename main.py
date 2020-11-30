import requests
import notion
import json
from notion.client import NotionClient
from os import environ
from tqdm import tqdm
from pathlib import Path
from time import sleep

STATUS_WAIT_TIME = 5
BLOCK_SIZE = 1024

token = environ.get("TOKEN_V2")
client = NotionClient(token_v2=token)


def get_task_status(task_id):
    task_statuses = client.post("getTasks", {"taskIds": [task_id]}).json()["results"]

    return list(
        filter(lambda task_status: task_status["id"] == task_id, task_statuses)
    )[0]


def launch_page_export(block_id):
    data = {
        "task": {
            "eventName": "exportBlock",
            "request": {
                "blockId": block_id,
                "recursive": False,
                "exportOptions": {
                    "exportType": "html",
                    "timeZone": "Asia/Calcutta",
                    "locale": "en",
                },
            },
        }
    }

    response = client.post("enqueueTask", data)
    return response.json()["taskId"]


def _download_file(url, export_file):
    with requests.get(url, stream=True, allow_redirects=True) as response:
        total_size = int(response.headers.get("content-length", 0))
        tqdm_bar = tqdm(total=total_size, unit="iB", unit_scale=True)
        with export_file.open("wb") as export_file_handle:
            for data in response.iter_content(BLOCK_SIZE):
                tqdm_bar.update(len(data))
                export_file_handle.write(data)
        tqdm_bar.close()


def get_block(block_id):
    collection_block = client.get_block(block_id, force_refresh=True)
    return collection_block


def build_page(page_block):
    title = page_block.title
    page_id = page_block.id

    task_id = launch_page_export(page_id)

    try:
        while True:
            task_status = get_task_status(task_id)
            if task_status["status"]["type"] == "complete":
                break
            print(f"...Export still in progress, waiting for {STATUS_WAIT_TIME} seconds")
            sleep(STATUS_WAIT_TIME)
        print("Export task is finished")
    except:
        print(f"Problem downloading {title}")


    export_link = task_status["status"]["exportURL"]
    print(f"Downloading zip for {title}")

    output_dir_path = Path("exports/")
    export_file_name = f"{page_id}.zip"

    _download_file(export_link, output_dir_path / export_file_name)


def build_collection(collection_block):
    collection = collection_block.collection

    for row in collection.get_rows():
        build_page(row)


def build_space(space_id):
    workspace = client.get_space(space_id, force_refresh=True)
    page_ids = workspace.get(force_refresh=True)["pages"]

    for page_id in page_ids:
        page_block = get_block(page_id)
        if page_block is None:
            continue
        if page_block.type == "page":
            build_page(page_block)
        else:
            build_collection(page_block)


def main():
    space_id = environ.get("SPACE_ID")
    build_space(space_id)


if __name__ == "__main__":
    main()
