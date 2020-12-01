import requests
from tqdm import tqdm

BLOCK_SIZE = 1024


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
