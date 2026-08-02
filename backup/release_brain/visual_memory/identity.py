import hashlib
import os


class MemoryIdentity:

    def generate_id(self, image_path):

        if not os.path.exists(image_path):
            return None

        with open(image_path, "rb") as file:
            image_hash = hashlib.sha256(
                file.read()
            ).hexdigest()

        return f"memory_{image_hash[:16]}"