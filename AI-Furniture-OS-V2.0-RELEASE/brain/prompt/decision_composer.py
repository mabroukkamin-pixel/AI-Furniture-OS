class DecisionComposer:


    def compose(self, context):

        print("🔥 DECISION COMPOSER ACTIVE")
        print(context.decision)
        print(context.graph_decision)

        decision = getattr(
            context,
            "decision",
            {}
        )


        if not decision:
            return ""


        lines = []


        lines.append(
            "AI DECISION:"
        )


        if decision.get("style"):

            lines.append(
                f"Style: {decision.get('style')}"
            )


        if decision.get("score"):

            lines.append(
                f"Confidence Score: {decision.get('score')}"
            )


        reasons = decision.get(
            "reasons",
            []
        )


        if reasons:

            lines.append(
                "Reasoning:"
            )

            for r in reasons:

                lines.append(
                    f"- {r}"
                )


        graph = getattr(
            context,
            "graph_decision",
            {}
        )


        nodes = graph.get(
            "nodes",
            []
        )


        for node in nodes:

            if node.get("node") in [
                "lighting",
                "mood",
                "colors"
            ]:

                lines.append(
                    f"{node['node']}: {node['value']}"
                )


        return "\n".join(lines)