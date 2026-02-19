# Geepers Vision Skill (`geepers-vision`)

A professional-grade Computer Vision MCP server designed for Enterprise Safety, Engineering Analysis, and Accessibility.

## Features

### 1. 🦺 Certified Safety Evaluation (`dream_vision_safety_eval`)
*   **Persona**: Certified Safety Expert & Risk Assessor.
*   **Capabilities**:
    *   OSHA Violation Detection.
    *   PPE Compliance Checks (Helmets, Vests, Glasses).
    *   Hazard Identification (Fire, Trip, Structural).

### 2. 📐 Engineering Schematics Analysis (`dream_vision_schematic`)
*   **Persona**: Senior Engineering Lead.
*   **Capabilities**:
    *   High-fidelity blueprint & schematic extraction.
    *   Dimension and tolerance verification.
    *   Component relationship mapping.

### 3. ♿ Accessibility (`dream_vision_alt_text`)
*   **Capabilities**:
    *   WCAG-compliant Alt Text generation.
    *   Context-aware descriptions.

### 4. 📂 File Management (`dream_vision_rename`)
*   **Capabilities**:
    *   Visual content-based file renaming (e.g., `IMG_001.jpg` -> `red_construction_helmet_side_view.jpg`).

## Configuration

Add to your `claude_desktop_config.json`:

```json
"geepers-vision": {
  "command": "python3",
  "args": ["/path/to/geepers/skills/source/vision/src/server.py"],
  "env": {
    "OPENAI_API_KEY": "sk-...",
    "XAI_API_KEY": "xai-..."     // Optional: Uses Grok-2 Vision if present
  }
}
```

## Provider Support
*   **OpenAI**: GPT-4o (Default)
*   **xAI**: Grok-2 Vision (Auto-detected if XAI_API_KEY is preferred)
