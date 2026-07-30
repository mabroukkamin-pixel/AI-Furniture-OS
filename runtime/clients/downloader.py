import os
import requests


class ImageDownloader:

    def download(self, url, output_path):

        os.makedirs(
            os.path.dirname(output_path),
            exist_ok=True
        )

        response = requests.get(url)
        response.raise_for_status()

        with open(output_path, "wb") as f:
            f.write(response.content)

        return output_path