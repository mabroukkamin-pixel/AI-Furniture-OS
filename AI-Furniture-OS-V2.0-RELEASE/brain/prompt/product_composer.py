class ProductComposer:

    def compose(self, brain):

        product = brain.product

        name = product.get("name", "")
        category = product.get("category", "")
        
        material = product.get("material", {})
        if isinstance(material, dict):
            primary_material = material.get("primary", "")
            secondary_material = ", ".join(material.get("secondary", []))
        else:
            primary_material = str(material)
            secondary_material = ""

        styles = "\n".join([f"- {s}" for s in product.get("style", [])]) if isinstance(product.get("style"), list) else product.get("style", "")
        usage = "\n".join([f"- {u}" for u in product.get("usage", [])]) if isinstance(product.get("usage"), list) else product.get("usage", "")

        colors_data = product.get("colors", {})
        if isinstance(colors_data, dict):
            colors = "\n".join(
                f"- {c}"
                for c in colors_data.get("primary", [])
            )
        elif isinstance(colors_data, list):
            colors = "\n".join(
                f"- {c}"
                for c in colors_data
            )
        else:
            colors = str(colors_data)

        size = product.get("size", {})
        width = size.get("width", "")
        height = size.get("height", "")

        return f"""
PRODUCT INFORMATION

Name:
{name}

Category:
{category}

Primary Material:
{primary_material}

Secondary Material:
{secondary_material}

Styles:
{styles}

Usage:
{usage}

Colors:
{colors}

Size:
Width: {width} cm
Height: {height} cm
""".strip()