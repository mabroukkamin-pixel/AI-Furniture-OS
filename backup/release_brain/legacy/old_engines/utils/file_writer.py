from pathlib import Path
import json
from datetime import datetime


class FileWriter:

    OUTPUT = Path("outputs")


    def save_prompt(self, prompt):

        folder = self.OUTPUT / "prompts"
        folder.mkdir(parents=True, exist_ok=True)

        filename = datetime.now().strftime("%Y%m%d_%H%M%S.txt")

        path = folder / filename

        path.write_text(prompt, encoding="utf8")

        return path


    def save_context(self, context):

        folder = self.OUTPUT / "context"
        folder.mkdir(parents=True, exist_ok=True)

        filename = datetime.now().strftime("%Y%m%d_%H%M%S.json")

        path = folder / filename

        data = {}

        for k, v in context.__dict__.items():

            try:
                json.dumps(v)
                data[k] = v

            except:

                data[k] = str(v)

        path.write_text(
            json.dumps(data, indent=4, ensure_ascii=False),
            encoding="utf8"
        )

        return path