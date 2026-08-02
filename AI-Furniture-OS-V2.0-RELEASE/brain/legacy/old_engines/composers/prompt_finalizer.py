class PromptFinalizer:

    def finalize(self, context):

        positive = context.final_prompt.get(
            "positive",
            ""
        )

        negative = ""

        final = f"""

MASTER COMMERCIAL FURNITURE PROMPT


{positive}


FINAL PROTECTION RULES:

The uploaded product image is the ONLY source of truth.

The AI must preserve:

- exact geometry
- exact dimensions
- exact texture
- exact colors
- exact craftsmanship
- exact details


Create a premium luxury furniture advertisement image.

The product must look physically real.

No redesign.
No modification.
No imagination of missing parts.


FINAL NEGATIVE RULES:

{context.final_prompt.get("negative","")}

"""

        context.final_prompt["final"] = final

        return context