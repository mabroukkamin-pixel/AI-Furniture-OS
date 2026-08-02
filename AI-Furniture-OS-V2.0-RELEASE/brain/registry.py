EXPERTS = []


def register(factory):
    EXPERTS.append(factory)


def clear():
    EXPERTS.clear()


def get_experts():
    return [
        factory()
        for factory in EXPERTS
    ]