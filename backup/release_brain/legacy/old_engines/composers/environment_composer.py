class EnvironmentComposer:

    def compose(self, context):

        environment = context.environment or {}

        primary = environment.get(
            "primary",
            ""
        )

        atmosphere = environment.get(
            "atmosphere",
            []
        )

        architecture = environment.get(
            "architecture",
            {}
        )

        options = environment.get(
            "options",
            []
        )


        # ==========================
        # Atmosphere
        # ==========================

        if isinstance(atmosphere, list):
            atmosphere = ", ".join(atmosphere)


        # ==========================
        # Architecture
        # ==========================

        if isinstance(architecture, dict):

            architecture_text = []

            for key, value in architecture.items():

                if isinstance(value, list):

                    architecture_text.append(
                        f"{key}: "
                        +
                        ", ".join(value)
                    )

                else:

                    architecture_text.append(
                        f"{key}: {value}"
                    )


            architecture = "\n".join(
                architecture_text
            )


        elif isinstance(architecture, list):

            architecture = ", ".join(
                architecture
            )


        # ==========================
        # Scenes
        # ==========================

        if isinstance(options, list):

            options = ", ".join(
                options
            )


        return f"""
ENVIRONMENT

Primary:
{primary}

Atmosphere:
{atmosphere}

Architecture:
{architecture}

Preferred Scenes:
{options}
""".strip()