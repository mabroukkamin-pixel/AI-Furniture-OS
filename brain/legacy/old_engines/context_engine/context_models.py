from dataclasses import dataclass

@dataclass
class Context:

    market: str

    season: str

    campaign: str

    platform: str

    language: str

    time: str

    luxury_level: str

    usage: str