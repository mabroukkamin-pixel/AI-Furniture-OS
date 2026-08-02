# Project Cleanup & Duplication Tracking

This document tracks redundant, overlapping, or legacy components across the project structure to be cleaned up safely in future versions.

## 1. Loaders
* ✓ `brain/product_engine/product_loader.py` (Active)
* ✓ `brain/brand_engine/brand_loader.py` (Active)
* ✗ `brain/decision_engine/reference_loader.py` (Review for deprecation)

## 2. Reference & Metadata Engines
* ✓ `brain/reference_engine/` (Active)
* ✗ Redundant standalone reference parsers outside the engine.

## 3. Knowledge & Rules
* ✓ `brain/decision_engine/rules.yaml` (Active)
* ✓ `brain/decision_engine/weights.yaml` (Active)
* ✗ Potential overlapping rules in legacy directories.

## 4. Pipeline Outputs
* ✓ `outputs/` (Active storage for manifests, decisions, briefs, and prompts)