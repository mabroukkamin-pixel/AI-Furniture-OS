from brain.world.world_state import WorldState


class WorldManager:

    def __init__(self):
        self.world = WorldState()

    def get_world(self):
        return self.world

    def reset(self):
        self.world = WorldState()

    def update(self, section: str, data: dict):

        if not hasattr(self.world, section):
            raise ValueError(f"Unknown World section: {section}")

        current = getattr(self.world, section)

        if isinstance(current, dict):
            current.update(data)
        else:
            setattr(self.world, section, data)

    def add_decision(self, decision: dict):
        self.world.decisions.append(decision)

    def add_trace(self, trace: dict):
        self.world.trace.append(trace)