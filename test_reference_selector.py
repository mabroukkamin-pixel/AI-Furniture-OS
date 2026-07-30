from brain.decision_engine.reference_selector import ReferenceSelector


selector = ReferenceSelector(
    "reference_library"
)


result = selector.select(

    material="rattan",

    style="natural",

    scene="luxury_villa",

    product="partition_rattan"

)


print(result)