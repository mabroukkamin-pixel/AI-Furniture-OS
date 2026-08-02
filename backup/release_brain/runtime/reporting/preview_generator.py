import os


class PreviewGenerator:

    def generate(self, state):

        output_folder = getattr(
            state,
            "output_folder",
            "outputs"
        )

        os.makedirs(
            output_folder,
            exist_ok=True
        )

        html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>AI Furniture OS Preview</title>

<style>

body{{
font-family:Arial;
background:#f5f5f5;
margin:40px;
}}

.card{{
background:white;
padding:30px;
border-radius:12px;
max-width:900px;
margin:auto;
box-shadow:0 0 15px rgba(0,0,0,.1);
}}

pre{{
white-space:pre-wrap;
background:#fafafa;
padding:15px;
border-radius:8px;
}}

img{{
max-width:100%;
border-radius:8px;
}}

</style>

</head>

<body>

<div class="card">

<h1>AI Furniture OS</h1>

<h2>Product</h2>

<p>{getattr(state,"product_id","")}</p>

<h2>Status</h2>

<p>{getattr(state,"status","")}</p>

<h2>Engine</h2>

<p>{getattr(state,"engine_name","")}</p>

<h2>Generated Image</h2>

<img src="{getattr(state,'generation',{}).get('image','') or ''}">

<h2>Prompt</h2>

<pre>{getattr(state,"prompt",{}).get("final","")}</pre>

</div>

</body>
</html>
"""

        path = os.path.join(
            output_folder,
            "preview.html"
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:
            f.write(html)

        return path.replace("\\", "/")