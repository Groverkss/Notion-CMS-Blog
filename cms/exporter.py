import requests
from tqdm import tqdm
from time import sleep

BLOCK_SIZE = 1024
STATUS_WAIT_TIME = 3
N_TRAILS = 5
FAIL_SLEEP_TIME = 1


class Exporter:
    def __init__(self, client):
        self.client = client

    def download_file(self, url, export_file):
        with requests.get(url, stream=True, allow_redirects=True) as response:
            total_size = int(response.headers.get("content-length", 0))
            tqdm_bar = tqdm(total=total_size, unit="iB", unit_scale=True)
            with export_file.open("wb") as export_file_handle:
                for data in response.iter_content(BLOCK_SIZE):
                    tqdm_bar.update(len(data))
                    export_file_handle.write(data)
            tqdm_bar.close()

    def get_task_status(self, task_id):
        task_statuses = self.client.post("getTasks", {"taskIds": [task_id]}).json()[
            "results"
        ]

        return list(
            filter(lambda task_status: task_status["id"] == task_id, task_statuses)
        )[0]

    def launch_page_export(self, block_id):
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
        response = self.client.post("enqueueTask", data)
        return response.json()["taskId"]

    def clean_pages(self, path):
        """Takes a Path class and removes all non hidden files and dirs from it"""
        for entry in path.iterdir():
            if entry.is_file():
                entry.unlink()
            else:
                self.clean_pages(path / entry.name)
                entry.rmdir()

    def clean_exports(self, path, preserve):
        """Deletes all non hidden files of a folder which are not present in
        preserve"""
        for entry in path.iterdir():
            if entry.is_file() and entry not in preserve:
                entry.unlink()

    def download_page(self, page_id, title, output_dir_path):
        """Downloads a page with id: page_id, title: title and zipfile path:
        output_dir_path"""
        task_id = self.launch_page_export(page_id)
        done = 0
        while done < N_TRAILS:
            try:
                while True:
                    task_status = self.get_task_status(task_id)
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
            return None

        print(f"Downloading zip for {title}")
        self.download_file(export_link, output_dir_path)
        return output_dir_path
