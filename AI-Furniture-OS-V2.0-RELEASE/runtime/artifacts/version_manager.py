import os


class VersionManager:

    def __init__(self, root="artifacts/products"):
        self.root = root

    def get_product_path(self, product_id):

        path = os.path.join(
            self.root,
            product_id,
            "versions"
        )

        os.makedirs(
            path,
            exist_ok=True
        )

        return path

    def next_version(self, product_id):

        versions_path = self.get_product_path(
            product_id
        )

        versions = []

        for item in os.listdir(versions_path):

            if item.startswith("v"):

                try:
                    versions.append(
                        int(item[1:])
                    )

                except ValueError:
                    pass

        if not versions:
            return "v001"

        return f"v{max(versions)+1:03d}"

    def latest_version(self, product_id):

        versions_path = self.get_product_path(
            product_id
        )

        versions = []

        for item in os.listdir(versions_path):

            if item.startswith("v"):

                try:
                    versions.append(item)

                except ValueError:
                    pass

        if not versions:
            return None

        return sorted(versions)[-1]

    def list_versions(self, product_id):

        versions_path = self.get_product_path(
            product_id
        )

        versions = []

        for item in os.listdir(versions_path):

            if item.startswith("v"):
                versions.append(item)

        return sorted(versions)