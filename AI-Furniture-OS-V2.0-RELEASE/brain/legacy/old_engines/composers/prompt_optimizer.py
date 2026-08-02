class PromptOptimizer:

    def optimize(self, prompt):

        while "\n\n\n" in prompt:
            prompt = prompt.replace(
                "\n\n\n",
                "\n\n"
            )

        return prompt.strip()