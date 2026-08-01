import hashlib
import json
import tempfile
from pathlib import Path
from types import SimpleNamespace

from runtime.artifacts.artifact_registry import ArtifactRegistry


class TestArtifactRegistry:

    def setup_method(self):
        self.project_root = Path(__file__).resolve().parents[1]
        self.outputs_root = self.project_root / "outputs"
        self.outputs_root.mkdir(exist_ok=True)

    @staticmethod
    def make_state(artifacts):
        return SimpleNamespace(
            product_id="ArtifactSnapshotTest",
            status="succeeded",
            engine_name="nano_banana",
            artifacts=artifacts,
            trace=[
                {
                    "engine": "DecisionExpertV3",
                    "message": "Selected style: gulf_villa with score: 95",
                }
            ],
        )

    def test_register_copies_files_and_preserves_source_artifacts(self):
        with tempfile.TemporaryDirectory(
            prefix="artifact_registry_test_",
            dir=self.outputs_root,
        ) as temporary_folder:
            working = Path(temporary_folder)
            archive_root = working / "archive"

            graph_memory = working / "graph_memory.json"
            graph_memory.write_text(
                '{"validation":{"valid":true}}',
                encoding="utf-8",
            )

            graph_decision = working / "graph_decision.json"
            graph_decision.write_text(
                '{"selected_style":"gulf_villa"}',
                encoding="utf-8",
            )

            image = working / "generated.png"
            image.write_bytes(b"generated-image")

            source_artifacts = {
                "graph_memory": graph_memory.relative_to(
                    self.project_root
                ).as_posix(),
                "graph_decision": graph_decision.relative_to(
                    self.project_root
                ).as_posix(),
                "generated_images": [
                    image.relative_to(
                        self.project_root
                    ).as_posix()
                ],
            }

            state = self.make_state(dict(source_artifacts))
            result = ArtifactRegistry(
                root=str(archive_root)
            ).register(state)

            assert result["graph_memory"] == source_artifacts["graph_memory"]
            assert result["graph_decision"] == source_artifacts["graph_decision"]
            assert result["generated_images"] == source_artifacts["generated_images"]
            assert result["version"] == "v001"

            manifest_path = Path(result["manifest"])
            manifest = json.loads(
                manifest_path.read_text(encoding="utf-8")
            )

            assert set(manifest["files"]) == {
                "graph_memory",
                "graph_decision",
                "generated_images",
            }

            memory_record = manifest["files"]["graph_memory"]
            assert memory_record["path"] == (
                "files/graph_memory/graph_memory.json"
            )
            assert memory_record["size"] == graph_memory.stat().st_size
            assert memory_record["sha256"] == hashlib.sha256(
                graph_memory.read_bytes()
            ).hexdigest()

            archived_memory = (
                manifest_path.parent / memory_record["path"]
            )
            assert archived_memory.read_bytes() == graph_memory.read_bytes()

            image_records = manifest["files"]["generated_images"]
            assert len(image_records) == 1
            assert (
                manifest_path.parent / image_records[0]["path"]
            ).read_bytes() == image.read_bytes()

    def test_register_ignores_missing_remote_and_external_paths(self):
        with tempfile.TemporaryDirectory(
            prefix="artifact_registry_filter_test_",
            dir=self.outputs_root,
        ) as temporary_folder, tempfile.TemporaryDirectory() as external_folder:
            working = Path(temporary_folder)
            external = Path(external_folder) / "external.txt"
            external.write_text("external", encoding="utf-8")

            state = self.make_state(
                {
                    "missing": "outputs/does-not-exist.json",
                    "remote": "https://example.com/image.png",
                    "external": str(external),
                }
            )

            result = ArtifactRegistry(
                root=str(working / "archive")
            ).register(state)
            manifest = json.loads(
                Path(result["manifest"]).read_text(encoding="utf-8")
            )

            assert manifest["files"] == {}
            assert result["missing"] == "outputs/does-not-exist.json"
            assert result["remote"] == "https://example.com/image.png"
            assert result["external"] == str(external)

    def test_register_increments_versions(self):
        with tempfile.TemporaryDirectory(
            prefix="artifact_registry_version_test_",
            dir=self.outputs_root,
        ) as temporary_folder:
            registry = ArtifactRegistry(
                root=str(Path(temporary_folder) / "archive")
            )

            first = registry.register(self.make_state({}))
            second = registry.register(self.make_state({}))

            assert first["version"] == "v001"
            assert second["version"] == "v002"
