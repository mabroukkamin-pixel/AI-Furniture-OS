
import json
import os


class RegistryManager:


    def __init__(self):

        self.file="brain/system/registry/modules.json"



    def get_modules(self):

        if not os.path.exists(self.file):

            return []

        with open(
            self.file,
            encoding="utf-8"
        ) as f:

            data=json.load(f)

        return data.get("modules",[])



    def active(self):

        return sorted(
            [
            m for m in self.get_modules()
            if m.get("enabled")
            ],
            key=lambda x:x["priority"]
        )

