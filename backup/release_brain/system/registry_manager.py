import json
import os


class RegistryManager:


    def __init__(self):

        self.file = (
            "brain/system/module_registry.json"
        )



    def load(self):

        if not os.path.exists(self.file):

            return {
                "modules": []
            }


        try:

            with open(
                self.file,
                "r",
                encoding="utf-8-sig"
            ) as f:

                return json.load(f)


        except Exception:

            return {
                "modules": []
            }



    def summary(self):

        data = self.load()

        modules = data.get(
            "modules",
            []
        )


        return {

            "total_modules":
                len(modules),


            "required_modules":
                len(
                    [
                        m for m in modules
                        if m.get("required")
                    ]
                )

        }



if __name__ == "__main__":

    manager = RegistryManager()

    print(
        manager.summary()
    )
