class PromptRanker:

    ORDER = [

        "PRODUCT",
        "PRESERVATION",
        "DESIGN DNA",
        "ENVIRONMENT",
        "SCENE",
        "ARCHITECTURE",
        "ACCESSORIES",
        "LIGHTING",
        "CAMERA",
        "COMPOSITION",
        "MARKETING",
        "BRAND",
        "QUALITY",
        "NEGATIVE"

    ]

    def rank(self, prompt):

        sections = {}

        current = None

        for line in prompt.splitlines():

            text = line.strip()

            if text in self.ORDER:

                current = text
                sections[current] = [line]
                continue

            if current:

                sections[current].append(line)

        result = []

        for name in self.ORDER:

            if name in sections:

                result.extend(sections[name])
                result.append("")

        return "\n".join(result)