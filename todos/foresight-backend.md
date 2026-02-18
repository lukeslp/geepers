# Foresight Backend Implementation

**Project**: /home/coolhand/projects/foresight
**Port**: 5062
**Started**: 2026-02-16
**Status**: MOSTLY COMPLETE

## Completed Components

### Backend Core
- [x] Application factory pattern (app/__init__.py)
- [x] Environment-based configuration (app/config.py)
- [x] Comprehensive database module with WAL mode (db.py)
- [x] Error handlers with JSON responses (app/errors.py)
- [x] Blueprint structure (main_bp, api_bp)
- [x] Shared library integration (sys.path for llm_providers)
- [x] Logging with rotation

### Database Schema (db.py)
- [x] cycles table (prediction cycles)
- [x] stocks table (discovered tickers per cycle)
- [x] prices table (historical price snapshots)
- [x] predictions table (LLM predictions with provider tracking)
- [x] accuracy_stats table (rolling metrics)
- [x] events table (SSE bridge for real-time updates)
- [x] Comprehensive indexes for performance
- [x] WAL mode enabled for concurrent reads
- [x] Foreign key constraints

### Services Layer
- [x] PredictionService (app/services/prediction_service.py)
  - discover_stocks() via configured LLM provider
  - generate_prediction() with JSON parsing
  - synthesize_confidence() for multi-prediction scoring
- [x] StockService (app/services/stock_service.py)
  - fetch_stock_info() via yfinance
  - fetch_historical_data()
  - validate_symbol()
  - get_market_status()

### API Endpoints (app/routes/api.py)
- [x] GET /api/current (current cycle data with stocks)
- [x] GET /api/stats (accuracy statistics by provider)
- [x] GET /api/history (paginated historical cycles)
- [x] GET /api/stock/<symbol> (detailed stock prediction history)
- [x] GET /api/stream (SSE endpoint with heartbeat)
- [x] POST /api/cycle/start (manually trigger new cycle)
- [x] POST /api/cycle/<id>/stop (stop running cycle)

### UI Routes (app/routes/main.py)
- [x] GET /health (health check with database status)
- [x] GET / (dashboard index)

## Remaining Work

### Critical
- [ ] Background worker for continuous prediction cycles (worker.py)
  - Run cycles on CYCLE_INTERVAL (600s = 10min)
  - Discover stocks via PredictionService
  - Fetch prices via StockService
  - Generate predictions
  - Emit events for SSE streaming
  - Evaluate completed predictions

### Enhancements
- [ ] Wire SSE streaming to actual prediction events (currently heartbeat only)
- [ ] Queue/channel system for event bus between worker and SSE
- [ ] Result validation worker (check predictions vs actual outcomes)
- [ ] Rate limiting on API endpoints
- [ ] Authentication for cycle start/stop endpoints

### Deployment
- [ ] Add to service_manager.py with port 5062
- [ ] Configure Caddy routing at /foresight
- [ ] Test health endpoint via sm health foresight
- [ ] Verify frontend integration

## Architecture Summary

```
Application Factory Pattern:
  run.py → create_app() → Flask app with blueprints

Blueprints:
  main_bp (/) → Dashboard UI, health check
  api_bp (/api) → REST + SSE endpoints

Services:
  PredictionService → LLM predictions (Grok/Claude/Gemini)
  StockService → yfinance integration

Database:
  SQLite with WAL mode (concurrent reads)
  ForesightDB class with comprehensive CRUD operations
  Event-based SSE bridge pattern

Configuration:
  Environment-based (Development/Production)
  Shared library integration for LLM providers
```

## Notes
- Using shared library: /home/coolhand/shared
- Providers: xAI (Grok discovery), Anthropic (Claude prediction), Gemini (synthesis)
- Pattern reference: /servers/clinical (Flask factory), /servers/swarm (multi-provider)
- Entry point: run.py (app.py deprecated but kept for backward compat)
