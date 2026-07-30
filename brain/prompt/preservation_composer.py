class PreservationComposer:

    def compose(self, context):

        rules = "\n".join(
            f"- {r}"
            for r in context.preservation["rules"]
        )

        return f"""
PRODUCT PRESERVATION

The product must remain IDENTICAL.

{rules}
""".strip()