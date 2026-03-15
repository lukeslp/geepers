---
description: Generate documentation - API docs, project docs, inline documentation
---

# Docs Mode

Generate or improve project documentation.

## Execute

Launch **@geepers_docs** to:

1. Scan the project for undocumented code, APIs, and modules
2. Generate appropriate documentation
3. Ensure consistency with existing docs

## Modes

```
/docs                  # Full documentation sweep
/docs api              # API endpoint documentation
/docs readme           # Generate/update README (routes to @geepers_readme)
/docs inline           # Add docstrings and comments to undocumented code
```

## What It Generates

- **API docs**: Endpoint documentation with request/response examples
- **Module docs**: Module-level docstrings explaining purpose and usage
- **Function docs**: Docstrings for public functions missing them
- **README**: Full project README (delegates to @geepers_readme)

## Humanize Gate

All generated documentation is checked against humanization rules:
- No "AI-powered", "AI-enhanced", "AI-driven"
- No "leverages", "utilizes", "facilitates"
- Natural language, not robot voice
- Credit Luke Steuber, not "Claude" or "AI"

## Cross-References

- README specifically: `/readme`
- Context documentation: `/context` (CLAUDE.md maintenance)
- Release notes: `/release` (changelog generation)

**Focus area** (optional): $ARGUMENTS
