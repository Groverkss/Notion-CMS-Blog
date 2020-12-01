import notion
import json
from notion.client import NotionClient
from os import environ
from pathlib import Path
from time import sleep
from cms.exporter import Exporter

STATUS_WAIT_TIME = 5
N_TRAILS = 5
FAIL_SLEEP_TIME = 1

token = environ.get("TOKEN_V2")
client = NotionClient(token_v2=token)
exporter = Exporter(client)


def get_block(block_id):
    collection_block = client.get_block(block_id, force_refresh=True)
    return collection_block


def build_page(page_block):
    title = page_block.title
    page_id = page_block.id

    task_id = exporter.launch_page_export(page_id)

    done = 0
    while done < N_TRAILS:
        try:
            while True:
                task_status = exporter.get_task_status(task_id)
                if task_status["status"]["type"] == "complete":
                    break
                print(
                    f"...Export still in progress, waiting for {STATUS_WAIT_TIME} seconds"
                )
                sleep(STATUS_WAIT_TIME)
            print("Export task is finished")
            export_link = task_status["status"]["exportURL"]
            done = N_TRAILS + 1
        except:
            print(f"Problem downloading {title} on Trial {done + 1}")
            done += 1
            if done < N_TRAILS:
                print(
                    f"Sleeping for {FAIL_SLEEP_TIME} seconds to prevent rate limiting"
                )
                sleep(FAIL_SLEEP_TIME)

    if done == N_TRAILS:
        print(f"Failed all trails of downloading {title}")
        return

    print(f"Downloading zip for {title}")

    output_dir_path = Path("exports/")
    export_file_name = f"{page_id}.zip"

    exporter.download_file(export_link, output_dir_path / export_file_name)


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
