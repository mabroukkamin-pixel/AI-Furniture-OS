from brain.rules.rule_loader import RuleLoader

def main():
    loader = RuleLoader("knowledge/rules/material")
    rules = loader.load()

    print()
    print("=" * 50)
    print("Loaded Rules:", len(rules))
    print()

    for rule in rules:
        print(rule.get("id"))
        print(rule.get("name"))
        print(rule.get("priority"))
        print()

    print("=" * 50)

if __name__ == "__main__":
    main()