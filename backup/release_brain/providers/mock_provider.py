from brain.providers.base_provider import BaseProvider
import json
import os
from datetime import datetime


class MockProvider(BaseProvider):

    def generate(self, request):

        print("=" * 40)
        print("MOCK IMAGE PROVIDER")
        print("=" * 40)

        os.makedirs(
            "outputs/mock",
            exist_ok=True
        )

        filename = (
            "outputs/mock/"
            + datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".json"
        )

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                request,
                f,
                indent=4,
                ensure_ascii=False
            )

        print("Mock request saved:")
        print(filename)

        return {
            "status": "mock_completed",
            "file": filename,
            "prompt": request["prompt"]
        }