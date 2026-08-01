from brain.graph.graph_score import GraphScore


print("================================")
print("GRAPH SCORE TEST")
print("================================")


scorer = GraphScore()


result = scorer.rank(

    "rattan",

    [
        "gulf_villa",
        "luxury_resort",
        "modern_natural_home"
    ]

)


print(result)