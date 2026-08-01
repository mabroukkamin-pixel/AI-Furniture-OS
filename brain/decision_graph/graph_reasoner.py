class GraphReasoner:

    def __init__(self, memory):

        self.memory = memory

    def _build_context(self, brain_state):

        product = brain_state.product or {}
        branding = brain_state.branding or {}

        nested_branding = branding.get(
            "branding",
            {}
        )

        market = (
            branding.get("market")
            or nested_branding.get("market")
        )

        return {
            "material": (
                product
                .get("material", {})
                .get("primary")
            ),
            "handmade": product.get(
                "handmade",
                False
            ),
            "premium": product.get(
                "premium",
                False
            ),
            "market": market
        }

    def _conditions_match(
        self,
        conditions,
        context
    ):

        for key, expected_value in conditions.items():

            if context.get(key) != expected_value:
                return False

        return True

    def _rule_recommendations(self, context):

        recommendations = []

        rule_nodes = self.memory.find_by_type(
            "decision_rule"
        )

        for node in rule_nodes:

            conditions = node.attributes.get(
                "conditions",
                {}
            )

            if not self._conditions_match(
                conditions,
                context
            ):
                continue

            decision = node.attributes.get(
                "decision",
                {}
            )

            style = decision.get("style")

            if not style:
                continue

            recommendations.append(
                {
                    "style": style,
                    "score": decision.get(
                        "score",
                        0
                    ),
                    "reasons": decision.get(
                        "reasons",
                        []
                    ),
                    "rule": node.attributes.get(
                        "name"
                    ),
                    "source": "decision_rule"
                }
            )

        return recommendations

    def _knowledge_recommendations(
        self,
        material
    ):

        if not material:
            return []

        material_id = f"material:{material}"

        relations = (
            "supports_style",
            "compatible_with_style"
        )

        recommendations = []

        for relation in relations:

            neighbors = self.memory.neighbors(
                material_id,
                relation=relation
            )

            for item in neighbors:

                node = item["node"]

                recommendations.append(
                    {
                        "style": node.attributes.get(
                            "name"
                        ),
                        "score": 50,
                        "reasons": [
                            "material knowledge match"
                        ],
                        "rule": None,
                        "source": "knowledge_graph"
                    }
                )

        return recommendations

    def _scene_recommendations(
        self,
        material
    ):

        if not material:
            return []

        material_id = f"material:{material}"

        neighbors = self.memory.neighbors(
            material_id,
            relation="supports_scene"
        )

        return [
            item["node"].attributes.get(
                "name"
            )
            for item in neighbors
            if item["node"].attributes.get(
                "name"
            )
        ]

    def _merge_recommendations(
        self,
        recommendations
    ):

        merged = {}

        for recommendation in recommendations:

            style = recommendation.get(
                "style"
            )

            if not style:
                continue

            current = merged.get(style)

            if (
                current is None
                or recommendation.get("score", 0)
                > current.get("score", 0)
            ):
                merged[style] = recommendation

        return sorted(
            merged.values(),
            key=lambda item: item.get(
                "score",
                0
            ),
            reverse=True
        )

    def recommend(self, context):

        if isinstance(context, str):

            context = {
                "material": context
            }

        material = context.get("material")

        recommendations = (
            self._rule_recommendations(context)
            + self._knowledge_recommendations(
                material
            )
        )

        return self._merge_recommendations(
            recommendations
        )

    def run(self, brain_state):

        context = self._build_context(
            brain_state
        )

        recommendations = self.recommend(
            context
        )

        selected = (
            recommendations[0]
            if recommendations
            else None
        )

        brain_state.graph_decision = {
            "context": context,
            "material": context.get(
                "material"
            ),
            "recommendations": recommendations,
            "selected_style": (
                selected.get("style")
                if selected
                else None
            ),
            "selected_score": (
                selected.get("score", 0)
                if selected
                else 0
            ),
            "scenes": (
                self._scene_recommendations(
                    context.get("material")
                )
            ),
            "source": (
                "DecisionGraph + GraphMemory"
            )
        }

        return brain_state