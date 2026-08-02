from dataclasses import dataclass, field


@dataclass
class Product:

    # ---------- Identity ----------

    id: str

    name: str

    category: str

    family: list = field(default_factory=list)

    # ---------- Material ----------

    material: dict = field(default_factory=dict)

    # ---------- Style ----------

    style: list = field(default_factory=list)

    # ---------- Usage ----------

    usage: list = field(default_factory=list)

    # ---------- Size ----------

    size: dict = field(default_factory=dict)

    # ---------- Colors ----------

    colors: dict = field(default_factory=dict)

    # ---------- Flags ----------

    handmade: bool = False

    premium: bool = False

    transparent: bool = False

    movable: bool = False