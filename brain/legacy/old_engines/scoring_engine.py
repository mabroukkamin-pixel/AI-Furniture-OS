from pathlib import Path
import yaml


class ScoringEngine:

    def __init__(self, weights_path):
        self.path = Path(weights_path)
        self.weights = self.load()

    def load(self):
        if not self.path.exists():
            return {}

        with open(
            self.path,
            "r",
            encoding="utf-8"
        ) as file:
            return yaml.safe_load(file)

    def score_materials(self, materials):
        scores = {}
        material_rules = (
            self.weights
            .get("weights", {})
            .get("material", {})
        )

        for material in materials:
            if material in material_rules:
                data = material_rules[material]
                score = data.get("score", 0)
                priorities = data.get("priority", [])

                for item in priorities:
                    if item not in scores:
                        scores[item] = 0
                    scores[item] += score

        return scores

    def score_styles(self, styles, base_scores=None):
        if base_scores is None:
            base_scores = {}

        style_rules = (
            self.weights
            .get("weights", {})
            .get("style", {})
        )

        scores = base_scores.copy()

        for style in styles:
            if style in style_rules:
                data = style_rules[style]
                score = data.get("score", 0)
                scores[style] = scores.get(style, 0) + score

        sorted_scores = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return sorted_scores