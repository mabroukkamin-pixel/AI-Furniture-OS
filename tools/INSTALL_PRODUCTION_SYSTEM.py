from pathlib import Path

router = Path("brain/commander/command_router.py")

text = router.read_text(encoding="utf-8")

if "def production(self)" not in text:

    insert = """

    def production(self):

        from brain.production.production_brain import ProductionBrain

        result = ProductionBrain().run()

        return {
            "production_status": "ACTIVE",
            "result": result
        }

"""

    text = text.replace(
        "    def auto(self):",
        insert + "\n    def auto(self):"
    )


if 'command == "PRODUCTION"' not in text:

    text = text.replace(
        'if command == "AUTO":',
        'if command == "PRODUCTION":\n            return self.production()\n\n        if command == "AUTO":'
    )


router.write_text(text, encoding="utf-8")


# create production brain runner

prod = Path("brain/production/production_runner.py")

prod.parent.mkdir(exist_ok=True)

prod.write_text(
'''
from brain.commander.command_router import CommandRouter

if __name__=="__main__":

    result = CommandRouter().route("PRODUCTION")

    print(result)

''',
encoding="utf-8"
)


print("PRODUCTION SYSTEM CONNECTED")

