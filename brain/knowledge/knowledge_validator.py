from pathlib import Path

import yaml


class KnowledgeValidationError(ValueError):

    def __init__(self, report):
        self.report = report
        count = report.get("stats", {}).get("error_count", 0)
        super().__init__(
            f"Knowledge validation failed with {count} error(s)."
        )


class KnowledgeValidator:

    REQUIRED_FILES = (
        "materials.yaml",
        "styles.yaml",
        "scenes.yaml",
        "decision_rules.yaml",
    )

    RELATIONS = {
        "materials.yaml": ("styles", "scenes"),
        "styles.yaml": ("materials",),
        "scenes.yaml": ("suitable_styles",),
    }

    ALLOWED_CONDITIONS = {
        "material",
        "handmade",
        "premium",
        "market",
    }

    def __init__(self, knowledge_directory="brain/knowledge"):
        directory = Path(knowledge_directory)
        if not directory.is_absolute():
            project_root = Path(__file__).resolve().parents[2]
            directory = project_root / directory
        self.knowledge_directory = directory.resolve()

    @staticmethod
    def _finding(code, filename, path, message):
        return {
            "code": code,
            "file": filename,
            "path": path,
            "message": message,
        }

    def _add(self, target, code, filename, path, message):
        target.append(
            self._finding(code, filename, path, message)
        )

    def _load_sources(self, errors):
        sources = {}
        for filename in self.REQUIRED_FILES:
            path = self.knowledge_directory / filename
            if not path.is_file():
                self._add(
                    errors,
                    "missing_file",
                    filename,
                    filename,
                    f"Required knowledge file is missing: {filename}",
                )
                continue
            try:
                with path.open("r", encoding="utf-8") as handle:
                    sources[filename] = yaml.safe_load(handle)
            except yaml.YAMLError as error:
                self._add(
                    errors,
                    "invalid_yaml",
                    filename,
                    filename,
                    f"Invalid YAML: {error}",
                )
        return sources

    def _profiles(self, sources, filename, root_key, errors):
        if filename not in sources:
            return {}

        data = sources[filename]

        if not isinstance(data, dict):
            self._add(
                errors,
                "invalid_root_type",
                filename,
                root_key,
                "The YAML root must be a mapping.",
            )
            return {}

        if root_key in data:
            profiles = data[root_key]

            if not isinstance(profiles, dict):
                self._add(
                    errors,
                    "invalid_root_type",
                    filename,
                    root_key,
                    f"{root_key} must be a mapping.",
                )
                return {}

            return profiles

        if filename in {
            "styles.yaml",
            "scenes.yaml",
        }:
            return data

        self._add(
            errors,
            "missing_root_key",
            filename,
            root_key,
            f"Required root key is missing: {root_key}",
        )

        return {}
    def _validate_profiles(self, profiles, filename, root_key, errors):
        fields = self.RELATIONS.get(filename, ())
        for name, profile in profiles.items():
            base_path = f"{root_key}.{name}"
            if not isinstance(name, str) or not name.strip():
                self._add(
                    errors,
                    "invalid_entry_name",
                    filename,
                    base_path,
                    "Entry names must be non-empty strings.",
                )
            if not isinstance(profile, dict):
                self._add(
                    errors,
                    "invalid_entry_type",
                    filename,
                    base_path,
                    "Knowledge entry must be a mapping.",
                )
                continue
            for field in fields:
                if field in profile and not isinstance(profile[field], list):
                    self._add(
                        errors,
                        "invalid_relation_type",
                        filename,
                        f"{base_path}.{field}",
                        f"{field} must be a list.",
                    )

    def _validate_rules(self, sources, errors, warnings):
        filename = "decision_rules.yaml"
        if filename not in sources:
            return []
        data = sources[filename]
        if not isinstance(data, dict):
            self._add(
                errors,
                "invalid_root_type",
                filename,
                "decision_rules",
                "The YAML root must be a mapping.",
            )
            return []
        rules = data.get("decision_rules")
        if not isinstance(rules, list):
            code = (
                "missing_root_key"
                if "decision_rules" not in data
                else "invalid_root_type"
            )
            self._add(
                errors,
                code,
                filename,
                "decision_rules",
                "decision_rules must be a list.",
            )
            return []

        names = set()
        for index, rule in enumerate(rules):
            base_path = f"decision_rules[{index}]"
            if not isinstance(rule, dict):
                self._add(
                    errors,
                    "invalid_rule_type",
                    filename,
                    base_path,
                    "Each decision rule must be a mapping.",
                )
                continue

            name = rule.get("name")
            if not isinstance(name, str) or not name.strip():
                self._add(
                    errors,
                    "invalid_rule_name",
                    filename,
                    f"{base_path}.name",
                    "Rule name must be a non-empty string.",
                )
            elif name in names:
                self._add(
                    errors,
                    "duplicate_rule_name",
                    filename,
                    f"{base_path}.name",
                    f"Duplicate decision rule name: {name}",
                )
            else:
                names.add(name)

            conditions = rule.get("conditions")
            if not isinstance(conditions, dict):
                self._add(
                    errors,
                    "invalid_conditions_type",
                    filename,
                    f"{base_path}.conditions",
                    "conditions must be a mapping.",
                )
                conditions = {}
            for key in conditions:
                if key not in self.ALLOWED_CONDITIONS:
                    self._add(
                        warnings,
                        "unknown_condition_key",
                        filename,
                        f"{base_path}.conditions.{key}",
                        f"Unknown condition key: {key}",
                    )

            decision = rule.get("decision")
            if not isinstance(decision, dict):
                self._add(
                    errors,
                    "invalid_decision_type",
                    filename,
                    f"{base_path}.decision",
                    "decision must be a mapping.",
                )
                continue

            style = decision.get("style")
            if not isinstance(style, str) or not style.strip():
                self._add(
                    errors,
                    "missing_decision_style",
                    filename,
                    f"{base_path}.decision.style",
                    "Decision style must be a non-empty string.",
                )

            score = decision.get("score")
            numeric = (
                isinstance(score, (int, float))
                and not isinstance(score, bool)
            )
            if not numeric:
                self._add(
                    errors,
                    "invalid_score_type",
                    filename,
                    f"{base_path}.decision.score",
                    "Decision score must be numeric.",
                )
            elif score < 0 or score > 100:
                self._add(
                    errors,
                    "score_out_of_range",
                    filename,
                    f"{base_path}.decision.score",
                    "Decision score must be between 0 and 100.",
                )

            reasons = decision.get("reasons")
            if reasons is not None and not isinstance(reasons, list):
                self._add(
                    errors,
                    "invalid_reasons_type",
                    filename,
                    f"{base_path}.decision.reasons",
                    "Decision reasons must be a list.",
                )
        return rules

    def _warn_reference(
        self,
        warnings,
        known,
        value,
        code,
        filename,
        path,
        label,
    ):
        if isinstance(value, str) and value not in known:
            self._add(
                warnings,
                code,
                filename,
                path,
                f"Unknown {label} reference: {value}",
            )

    def _validate_references(
        self,
        materials,
        styles,
        scenes,
        rules,
        warnings,
    ):
        material_names = set(materials)
        style_names = set(styles)
        scene_names = set(scenes)

        for name, profile in materials.items():
            if not isinstance(profile, dict):
                continue
            for index, value in enumerate(profile.get("styles", [])):
                self._warn_reference(
                    warnings, style_names, value,
                    "unknown_style_reference", "materials.yaml",
                    f"materials.{name}.styles[{index}]", "style",
                )
            for index, value in enumerate(profile.get("scenes", [])):
                self._warn_reference(
                    warnings, scene_names, value,
                    "unknown_scene_reference", "materials.yaml",
                    f"materials.{name}.scenes[{index}]", "scene",
                )

        for name, profile in styles.items():
            if not isinstance(profile, dict):
                continue
            for index, value in enumerate(profile.get("materials", [])):
                self._warn_reference(
                    warnings, material_names, value,
                    "unknown_material_reference", "styles.yaml",
                    f"styles.{name}.materials[{index}]", "material",
                )

        for name, profile in scenes.items():
            if not isinstance(profile, dict):
                continue
            for index, value in enumerate(profile.get("suitable_styles", [])):
                self._warn_reference(
                    warnings, style_names, value,
                    "unknown_style_reference", "scenes.yaml",
                    f"scenes.{name}.suitable_styles[{index}]", "style",
                )

        for index, rule in enumerate(rules):
            if not isinstance(rule, dict):
                continue
            conditions = rule.get("conditions", {})
            decision = rule.get("decision", {})
            if isinstance(conditions, dict):
                self._warn_reference(
                    warnings, material_names,
                    conditions.get("material"),
                    "unknown_material_reference", "decision_rules.yaml",
                    f"decision_rules[{index}].conditions.material", "material",
                )
            if isinstance(decision, dict):
                self._warn_reference(
                    warnings, style_names, decision.get("style"),
                    "unknown_style_reference", "decision_rules.yaml",
                    f"decision_rules[{index}].decision.style", "style",
                )

    def validate(self):
        errors = []
        warnings = []
        sources = self._load_sources(errors)

        materials = self._profiles(
            sources, "materials.yaml", "materials", errors
        )
        styles = self._profiles(
            sources, "styles.yaml", "styles", errors
        )
        scenes = self._profiles(
            sources, "scenes.yaml", "scenes", errors
        )

        self._validate_profiles(
            materials, "materials.yaml", "materials", errors
        )
        self._validate_profiles(
            styles, "styles.yaml", "styles", errors
        )
        self._validate_profiles(
            scenes, "scenes.yaml", "scenes", errors
        )
        rules = self._validate_rules(sources, errors, warnings)

        self._validate_references(
            materials, styles, scenes, rules, warnings
        )

        stats = {
            "files": len(sources),
            "materials": len(materials),
            "styles": len(styles),
            "scenes": len(scenes),
            "decision_rules": len(rules),
            "error_count": len(errors),
            "warning_count": len(warnings),
        }
        return {
            "valid": not errors,
            "errors": errors,
            "warnings": warnings,
            "stats": stats,
        }
