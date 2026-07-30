from brain.context import BrainContext
from brain.prompt.master_prompt_composer import MasterPromptComposer


print("=" * 60)
print("MASTER PROMPT TEST")
print("=" * 60)


context = BrainContext()


context.product = {

    "name": "Rattan Partition",

    "category": "room_divider",

    "material": {
        "primary": "rattan",
        "secondary": [
            "wood"
        ]
    },

    "style": [
        "natural",
        "bohemian"
    ],

    "usage": [
        "living_room",
        "villa"
    ],

    "colors": {
        "primary": [
            "beige",
            "natural brown"
        ]
    },

    "size": {

        "width": 200,
        "height": 180
    }

}


context.preservation = {

    "rules": [

        "Do not change product shape",

        "Do not change material texture",

        "Do not change colors",

        "Preserve original dimensions",

        "Keep every detail identical"

    ]

}


composer = MasterPromptComposer()


prompt = composer.compose(context)


print(prompt)