import json
import os

from runtime.reporting.metadata_builder import MetadataBuilder
from runtime.reporting.package_builder import PackageBuilder
from runtime.manifest_manager import ManifestManager


class ArtifactBuilder:

    def __init__(self):

        self.metadata_builder = MetadataBuilder()

        self.package_builder = PackageBuilder()

        self.manifest_manager = ManifestManager()

    def build(self, state):

        folder = state.output_folder

        if not folder:
            return

        os.makedirs(
            folder,
            exist_ok=True
        )

        metadata = self.metadata_builder.build(
            state
        )

        metadata_path = os.path.join(
            folder,
            "metadata.json"
        )

        with open(
            metadata_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                metadata,
                f,
                indent=4,
                ensure_ascii=False
            )

        package = self.package_builder.build(
            state
        )

        self.manifest_manager.save(
            state
        )

        state.artifacts.update({

            "metadata": metadata_path,

            "package": package,

            "manifest":
                os.path.join(
                    folder,
                    "manifest.json"
                )

        })

        return state.artifacts