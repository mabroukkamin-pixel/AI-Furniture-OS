from brain.creative_engine.brief_generator import BriefGenerator


decision = {

    "primary_style": "natural",

    "scene": [
        "luxury_villa",
        "beige_stone_wall"
    ],

    "camera": [
        "45_degree"
    ],

    "lighting": [
        "golden_hour"
    ],

    "avoid": [
        "redesign"
    ],

    "market": "Kuwait"

}


brief = BriefGenerator(
    "بارتيشن قش",
    decision
).generate()


print(brief)