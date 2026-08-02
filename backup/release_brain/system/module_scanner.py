import os
import json


class ModuleScanner:

    def __init__(self):

        self.root = os.getcwd()

        self.registry_file = (
            "brain/system/module_registry.json"
        )


    def load_registry(self):

        if not os.path.exists(self.registry_file):

            return {
                "modules": []
            }


        try:

            with open(
                self.registry_file,
                "r",
                encoding="utf-8-sig"
            ) as f:

                return json.load(f)


        except Exception as e:

            print(
                "REGISTRY LOAD ERROR:",
                e
            )

            return {
                "modules": []
            }



    def scan(self):

        registry = self.load_registry()

        results = []


        for module in registry.get(
            "modules",
            []
        ):

            path = module.get(
                "path"
            )

            exists = os.path.exists(
                path
            )


            results.append({

                "name":
                    module.get(
                        "name"
                    ),

                "path":
                    path,

                "status":
                    "ACTIVE"
                    if exists
                    else
                    "MISSING",

                "priority":
                    module.get(
                        "priority",
                        0
                    )

            })


        return results



    def report(self):

        data = self.scan()


        print("")
        print("============================")
        print(" SMART MODULE SCANNER ")
        print("============================")


        for item in data:

            print(
                f"{item['name']} : {item['status']}"
            )


        return data



if __name__ == "__main__":

    scanner = ModuleScanner()

    scanner.report()
