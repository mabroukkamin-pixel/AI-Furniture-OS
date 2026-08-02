import json
import os


class MemoryDeduplicator:

    def __init__(self, memory_file):
        self.memory_file = memory_file


    def load_memory(self):

        if not os.path.exists(self.memory_file):
            return []

        with open(
            self.memory_file,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)


    def exists(self, memory_id):

        memories = self.load_memory()

        for memory in memories:

            if memory.get("memory_id") == memory_id:
                return True

        return False