# Knowledge Validator V1 Specification

## Purpose

Knowledge Validator V1 protects Decision Graph V3 from malformed or inconsistent
knowledge files before graph construction begins.

The validator is a structural and referential integrity boundary. It does not select
a style, score a product, or mutate knowledge content.

## Validated Sources

The validator reads the same four sources used by `KnowledgeGraphBuilder`:

- `brain/knowledge/materials.yaml`
- `brain/knowledge/styles.yaml`
- `brain/knowledge/scenes.yaml`
- `brain/knowledge/decision_rules.yaml`

## Validation Policy

Validation findings have two severities.

### Errors

Errors represent data that cannot be interpreted safely. Any error makes the report
invalid and blocks graph construction.

Examples:

- required file missing
- YAML root has the wrong type
- `materials` root key missing
- material, style, or scene profile is not a mapping
- `decision_rules` is not a list
- duplicate rule name
- rule conditions or decision is not a mapping
- decision style missing
- score missing, non-numeric, or outside 0 through 100
- list-valued relation stored as another type

### Warnings

Warnings represent valid data that can still produce a graph but may indicate an
incomplete knowledge library. Warnings never block graph construction.

Examples:

- material references a style not defined in `styles.yaml`
- material references a scene not defined in `scenes.yaml`
- style references a material not defined in `materials.yaml`
- scene references a style not defined in `styles.yaml`
- decision rule recommends a style not defined in `styles.yaml`
- decision rule material is not defined in `materials.yaml`

This warning policy preserves the current graph behavior, where referenced entities
may be created as lightweight nodes even when no detailed profile exists.

## Report Contract

The validator returns a JSON-compatible dictionary:

```python
{
    "valid": True,
    "errors": [],
    "warnings": [],
    "stats": {
        "files": 4,
        "materials": 0,
        "styles": 0,
        "scenes": 0,
        "decision_rules": 0,
        "error_count": 0,
        "warning_count": 0,
    },
}
```

Each finding is a dictionary:

```python
{
    "code": "unknown_style_reference",
    "file": "materials.yaml",
    "path": "materials.rattan.styles[2]",
    "message": "Style 'japandi' is referenced but has no profile.",
}
```

Finding order must be deterministic so test and output reports remain stable.

## File Contracts

### materials.yaml

Required root:

```yaml
materials: {}
```

Each material name must map to a dictionary. The following relation fields, when
present, must be lists:

- `styles`
- `scenes`
- `lighting`
- `architecture`
- `walls`
- `floors`
- `avoid`

`colors` and `accessories`, when present, must be dictionaries.

### styles.yaml

The document root must be a dictionary. Each style name must map to a dictionary.
The following fields, when present, must be lists:

- `colors`
- `materials`
- `lighting`
- `mood`

### scenes.yaml

The document root must be a dictionary. Each scene name must map to a dictionary.
The following fields, when present, must be lists:

- `architecture`
- `suitable_styles`
- `accessories`
- `lighting`

### decision_rules.yaml

Required root:

```yaml
decision_rules: []
```

Each rule must contain:

- unique non-empty string `name`
- dictionary `conditions`
- diction `decision`
- non-empty string `decision.style`
- numeric `decision.score` between 0 and 100

`decision.reasons`, when present, must be a list.

Condition keys are open for extension. V1 recognizes the current keys:

- `material`
- `handmade`
- `premium`
- `market`

Unknown condition keys produce warnings rather than errors so future rule dimensions
can be introduced without breaking older validators.

## Runtime Integration

`KnowledgeGraphBuilder.build()` validates before creating any node or edge.

Behavior:

1. Load and validate all four sources.
2. If errors exist, raise `KnowledgeValidationError` with the report attached.
3. If only warnings exist, continue building.
4. Preserve the validation report on the builder as `validation_report`.
5. Expose the report through Decision Graph memory output.

The validator must not modify YAML files or silently repair data.

## Exception Contract

```python
class KnowledgeValidationError(ValueError):
    def __init__(self, report):
        self.report = report
```

The exception message includes the number of validation errors. Consumers can inspect
`error.report` for structured details.

## Test Coverage

Tests must cover:

1. Current knowlede files validate successfully.
2. Current unresolved references produce warnings, not errors.
3. Missing required file blocks graph construction.
4. Invalid YAML root type is rejected.
5. Duplicate rule names are rejected.
6. Missing rule decision style is rejected.
7. Invalid score type and range are rejected.
8. Incorrect relation field type is rejected.
9. Unknown references are reported deterministically.
10. `KnowledgeGraphBuilder` stores the report and blocks on errors.

## Non-Goals

V1 does not:

- validate product YAML
- rewrite or normalize knowledge
- calculate decision scores
- guarantee semantic quality of a recommendation
- require every referenced style or scene to have a detailed profile
- replace `StateValidator`

`StateValidator` validates runtime state. `KnowledgeValidator` validates static
knowledge before that state is reasoned over.
