# Dashboard Contract

## Purpose

Provide a local visual production dashboard for the canonical AI Furniture OS pipeline.

The dashboard is a presentation and control layer only. It must not duplicate product analysis, prompt composition, production logic, artifact ownership, or manifest generation.

## Official Integration

The dashboard communicates only with the official FastAPI layer:

- GET /
- GET /products
- POST /generate
- GET /outputs/<ProductID>/<Artifact>

The production path remains:

api/main.py → runtime/run_pipeline.py → runtime/pipeline.py

## Allowed Files

The dashboard implementation may change only:

- api/main.py
- ui/index.html
- ui/static/styles.css
- ui/static/app.js
- tests/test_api.py
- tests/test_dashboard.py
- requirements.txt, only if a required dependency is proven missing

## MVP Interface

The first dashboard version must include:

1. System status.
2. Product selector.
3. Product ID display.
4. Start production button.
5. Current run status.
6. Generation status.
7. Prompt audit score.
8. Final prompt preview.
9. Generated image preview when available.
10. Artifact links.
11. Clear failure message for local-only mode.
12. Manifest summary.

## Visual Direction

- Arabic-first interface.
- Right-to-left layout.
- Premium furniture-production aesthetic.
- Dark navy, warm gold, off-white, and restrained green/red status colors.
- Responsive desktop layout.
- No generated branding assets or fake production images.

## Runtime Rules

- The dashboard must never report success unless generation status is success.
- Local-only mode must be shown as unavailable production, not successful production.
- The dashboard must display API errors without hiding the response details.
- Product and artifact paths must come from the API or manifest.
- The dashboard must not read arbitrary filesystem paths.
- The API remains the source of runtime truth.

## Security Boundaries

- Never expose GEMINI_API_KEY or environment variables.
- Only serve products and output artifacts from their approved project directories.
- Reject path traversal.
- Do not expose legacy or internal source files.

## Testing Gate

The dashboard is accepted only when:

- The home page loads.
- The products endpoint returns available products.
- A valid product can be submitted.
- Local-only mode renders as a failure state.
- Successful generation renders an image when present.
- Invalid product IDs are rejected.
- Existing production tests remain green.