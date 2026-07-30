class PromptCleaner:

    def clean(self, prompt):

        if not prompt:
            return ""

        lines = prompt.splitlines()

        cleaned = []

        previous = ""

        for line in lines:

            line = line.rstrip()

            if line == previous:
                continue

            previous = line

            cleaned.append(line)

        return "\n".join(cleaned)