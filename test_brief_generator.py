from brain.creative_engine.brief_generator import BriefGenerator


decision = {

    "primary_style":
        "gulf_luxury",

    "background":
        [
            "luxury_villa",
            "beige_stone_wall"
        ],

    "camera":
        [
            "45_degree",
            "lifestyle_shot"
        ],

    "lighting":
        [
            "golden_hour"
        ],

    "avoid":
        [
            "product_modification"
        ]
}



generator = BriefGenerator(
    "Partition001",
    decision
)


brief = generator.generate()


print("="*50)
print(brief)
print("="*50)