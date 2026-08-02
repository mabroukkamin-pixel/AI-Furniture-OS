class BrainReportGenerator:


    def generate(self, state):

        product = state.product or {}

        decision = state.decision or {}

        dna = state.design_dna or {}

        action = getattr(
            state,
            "action_plan",
            {}
        )


        html = f"""
<!DOCTYPE html>

<html>

<head>

<title>
AI Furniture OS Report
</title>


<style>

body {{
font-family: Arial;
background:#f5f5f5;
padding:40px;
}}

.card {{
background:white;
padding:25px;
margin:20px;
border-radius:15px;
box-shadow:0 0 10px #ccc;
}}

.title {{
font-size:30px;
font-weight:bold;
}}

.score {{
font-size:40px;
color:#b8860b;
}}

</style>

</head>


<body>


<div class="card">

<div class="title">
AI FURNITURE OS V2
</div>

<h2>
Product
</h2>

<p>
{product.get("name","")}
</p>


</div>



<div class="card">

<h2>
Decision
</h2>

<p>
Style:
{decision.get("style","")}
</p>


<div class="score">

{decision.get("score",0)}%

</div>


</div>




<div class="card">

<h2>
Design DNA
</h2>

<pre>

{dna}

</pre>

</div>



<div class="card">

<h2>
Execution
</h2>


<pre>

{action}

</pre>


</div>


</body>


</html>
"""


        return html
