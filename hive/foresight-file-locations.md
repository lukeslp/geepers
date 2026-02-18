# Foresight Quick Wins - Exact File Locations

## Files Modified (9 total)

All paths are absolute from project root: `/home/coolhand/projects/foresight/`

---

## 1. requirements.txt
**Location**: `/home/coolhand/projects/foresight/requirements.txt`
**Lines**: 7-10
**Change**: Added 3 new packages

```diff
  flask>=3.0
  yfinance>=0.2.36
  requests>=2.31
  gunicorn>=21.2
  python-dotenv>=1.0.0

+ # LLM Providers (for stock discovery and prediction)
+ anthropic>=0.25.0
+ google-generativeai>=0.3.0
+ openai>=1.10.0

  # Shared library (install in editable mode)
  # pip install -e /home/coolhand/shared[all]
```

---

## 2. app/config.py
**Location**: `/home/coolhand/projects/foresight/app/config.py`
**Lines**: 23-24
**Change**: Reduced default CYCLE_INTERVAL

```diff
      # Prediction cycle
-     CYCLE_INTERVAL = int(os.environ.get('CYCLE_INTERVAL', 600))  # 10 minutes
+     CYCLE_INTERVAL = int(os.environ.get('CYCLE_INTERVAL', 30))  # 30 seconds (dev), set to 600 for production
```

---

## 3. app/worker.py
**Location**: `/home/coolhand/projects/foresight/app/worker.py`
**Multiple sections with changes**

### Section A: __init__ method (Lines 28-43)
**Change**: Added health tracking fields

```diff
      self.config = config
      self.db_path = config['DB_PATH']
      self.running = False
      self.thread: Optional[threading.Thread] = None
      self.current_cycle_id: Optional[int] = None
+     self.last_cycle_time: Optional[float] = None
+     self.total_cycles_completed: int = 0
```

### Section B: _run_worker method (Lines 69-92)
**Change**: Run first cycle immediately

```diff
      def _run_worker(self):
          """Main worker loop"""
          cycle_interval = self.config['CYCLE_INTERVAL']
+         first_cycle = True

          while self.running:
              try:
                  # Run a prediction cycle
                  self._run_prediction_cycle()

-                 # Wait for next cycle
-                 logger.info(f'Waiting {cycle_interval}s until next cycle')
-                 time.sleep(cycle_interval)
+                 # For first cycle, short wait; then use normal interval
+                 if first_cycle:
+                     logger.info('First cycle complete, entering normal schedule')
+                     first_cycle = False
+                     # Brief wait before next cycle
+                     time.sleep(5)
+                 else:
+                     logger.info(f'Waiting {cycle_interval}s until next cycle')
+                     time.sleep(cycle_interval)

              except Exception as e:
                  logger.error(f'Worker error: {e}', exc_info=True)
                  # Wait a bit before retrying
                  time.sleep(60)
```

### Section C: _discover_stocks method (Lines 124-145)
**Change**: Added debug logging

```diff
          try:
              max_stocks = self.config['MAX_STOCKS']
+             logger.debug(f'Calling discover_stocks with max_stocks={max_stocks}')
              symbols = self.prediction_service.discover_stocks(count=max_stocks)
+             logger.debug(f'Discovery returned: {symbols}')

              if not symbols:
                  logger.warning('Discovery returned no stocks')
                  return []

              logger.info(f'Discovered {len(symbols)} stocks: {symbols}')
```

### Section D: _run_prediction_cycle method (Lines 115-125)
**Change**: Track cycle completion time

```diff
              # Phase 3: Complete cycle
              db.complete_cycle(cycle_id)
+             self.total_cycles_completed += 1
+             self.last_cycle_time = time.time()
-             logger.info(f'Completed prediction cycle {cycle_id}')
+             logger.info(f'Completed prediction cycle {cycle_id} (total: {self.total_cycles_completed})')

              except Exception as e:
                  # ...
              finally:
                  self.current_cycle_id = None
+                 self.last_cycle_time = time.time()
```

### Section E: get_status method (Lines 276-297)
**Change**: Added health monitoring

```diff
      def get_status(self) -> dict:
          """Get worker status"""
+         import time
          status = {
              'running': self.running,
              'thread_alive': self.is_alive(),
              'current_cycle_id': self.current_cycle_id,
+             'total_cycles_completed': self.total_cycles_completed,
+             'last_cycle_time': self.last_cycle_time
          }

+         # Check if worker is stale (no cycle in >2x interval)
+         if self.last_cycle_time:
+             time_since_last = time.time() - self.last_cycle_time
+             max_allowed = self.config['CYCLE_INTERVAL'] * 2
+             status['is_healthy'] = time_since_last < max_allowed
+             status['seconds_since_last_cycle'] = int(time_since_last)
+         else:
+             status['is_healthy'] = True if self.is_alive() else False
+             status['seconds_since_last_cycle'] = None

          return status
```

---

## 4. app/routes/api.py
**Location**: `/home/coolhand/projects/foresight/app/routes/api.py`
**Multiple sections with changes**

### Section A: New health/providers endpoint (Lines 119-147)
**Change**: Added new endpoint BEFORE /api/stream

```diff
+ @api_bp.route('/health/providers')
+ def health_providers():
+     """Check health of LLM providers"""
+     from app.services.prediction_service import PredictionService
+
+     service = PredictionService(current_app.config)
+
+     providers_status = {}
+     for role, provider_name in current_app.config['PROVIDERS'].items():
+         if role in service.providers:
+             provider = service.providers[role]
+             providers_status[role] = {
+                 'status': 'configured',
+                 'provider': provider_name,
+                 'type': type(provider).__name__
+             }
+         else:
+             providers_status[role] = {
+                 'status': 'error',
+                 'provider': provider_name,
+                 'error': 'Failed to initialize'
+             }
+
+     all_healthy = all(p.get('status') == 'configured' for p in providers_status.values())
+
+     return jsonify({
+         'healthy': all_healthy,
+         'providers': providers_status
+     })
+

  @api_bp.route('/stream')
```

### Section B: Modified /api/cycle/start endpoint (Lines 247-280)
**Change**: Now triggers actual cycle instead of just reporting

```diff
  @api_bp.route('/cycle/start', methods=['POST'])
  def start_cycle():
      """Manually trigger a new prediction cycle"""
+     import threading

      db = get_db()

      # Check if there's already an active cycle
      current_cycle = db.get_current_cycle()

      if current_cycle:
          return jsonify({
              'error': 'Cycle already running',
              'cycle_id': current_cycle['id']
          }), 409

      # Check if worker is running
      worker = current_app.worker
      if not worker.is_alive():
          return jsonify({
              'error': 'Background worker is not running',
              'message': 'Restart the application to start the worker'
          }), 503

-     # The worker runs cycles automatically based on CYCLE_INTERVAL
-     # This endpoint just reports status
+     # Trigger an immediate cycle in the worker by calling _run_prediction_cycle directly
+     # This runs in a background thread so we don't block the response
+     def trigger_cycle():
+         try:
+             worker._run_prediction_cycle()
+             current_app.logger.info('Manual cycle triggered via /api/cycle/start')
+         except Exception as e:
+             current_app.logger.error(f'Manual cycle error: {e}', exc_info=True)
+
+     cycle_thread = threading.Thread(target=trigger_cycle, daemon=True)
+     cycle_thread.start()

      return jsonify({
-         'status': 'worker_running',
-         'message': 'Background worker is running and will start cycles automatically',
-         'next_cycle_in': f'{current_app.config["CYCLE_INTERVAL"]} seconds'
+         'status': 'cycle_triggered',
+         'message': 'Prediction cycle triggered immediately'
      }), 200
```

---

## 5. app/services/prediction_service.py
**Location**: `/home/coolhand/projects/foresight/app/services/prediction_service.py`
**Multiple sections with changes**

### Section A: discover_stocks method (Lines 52-95)
**Change**: Added error logging and debug traces

```diff
      if 'discovery' not in self.providers:
-         logger.error('Discovery provider not configured')
+         logger.error('Discovery provider not configured. Available providers: %s', list(self.providers.keys()))
          return []

      try:
          provider = self.providers['discovery']
+         logger.debug(f'Using {provider.__class__.__name__} for stock discovery')

          # ... prompt definition ...

+         # Use standard provider interface: complete(messages)
+         from llm_providers import Message
+         logger.debug(f'Calling provider.complete() for stock discovery')
          response = provider.complete(
              messages=[Message(role='user', content=prompt)]
          )
+         logger.debug(f'Provider returned: {response.content[:200]}...')

          # Parse JSON response (response is CompletionResponse object)
          import json
-         symbols = json.loads(response)
+         symbols = json.loads(response.content)
+         logger.debug(f'Parsed symbols: {symbols}')

          if isinstance(symbols, list):
-             return [s.upper() for s in symbols[:count]]
+             result = [s.upper() for s in symbols[:count]]
+             logger.debug(f'Discovery returning: {result}')
+             return result

+         logger.warning(f'Response was not a list: {type(symbols)}')
          return []
```

### Section B: generate_prediction method (Lines 132-150)
**Change**: Updated to use .complete() interface

```diff
          try:
              provider = self.providers['prediction']

              prompt = f"""Analyze this stock and make a short-term prediction (1-7 days):
              # ... prompt text ...
              }}"""

+             from llm_providers import Message
              response = provider.complete(
                  messages=[Message(role='user', content=prompt)]
              )

              # Parse JSON response (response is CompletionResponse object)
              import json
-             prediction = json.loads(response)
+             prediction = json.loads(response.content)

              return {
                  'provider': self.config['PROVIDERS']['prediction'],
-                 'model': provider.model,
+                 'model': getattr(provider, 'model', 'unknown'),
                  'prediction': prediction.get('prediction', 'NEUTRAL'),
                  'confidence': prediction.get('confidence', 0.5),
                  'reasoning': prediction.get('reasoning', 'No reasoning provided')
              }
```

### Section C: synthesize_confidence method (Lines 181-190)
**Change**: Updated to use .complete() interface

```diff
          try:
              provider = self.providers['synthesis']

              prompt = f"""You are analyzing multiple stock predictions.
              # ... prompt text ...
              Return ONLY a number between 0.0 and 1.0, nothing else."""

+             from llm_providers import Message
              response = provider.complete(
                  messages=[Message(role='user', content=prompt)]
              )

              # Parse float response (response is CompletionResponse object)
-             confidence = float(response.strip())
+             confidence = float(response.content.strip())
              return max(0.0, min(1.0, confidence))
```

---

## 6. static/js/app.js
**Location**: `/home/coolhand/projects/foresight/static/js/app.js`
**Lines**: 308-327
**Change**: Enhanced showEmptyState method

```diff
      showEmptyState() {
-         const statusEl = document.querySelector('#status');
+         const gridEl = document.querySelector('#stock-grid');
-         if (statusEl) {
-             statusEl.innerHTML = `
-                 <h2>No Active Predictions</h2>
-                 <p>Waiting for the next prediction cycle to start...</p>
+         if (gridEl) {
+             gridEl.innerHTML = `
+                 <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 400px; gap: 20px;">
+                   <div class="loading-spinner" style="width: 40px; height: 40px; border: 3px solid var(--glass-border); border-top: 3px solid var(--accent); border-radius: 50%; animation: spin 1s linear infinite;"></div>
+                   <h2 style="margin: 0; color: var(--text-primary);">Waiting for Predictions</h2>
+                   <p style="margin: 0; color: var(--text-secondary); text-align: center; max-width: 300px;">
+                     The prediction engine is running its first cycle. This typically takes 30-60 seconds.
+                   </p>
+                   <p style="margin: 0; color: var(--text-secondary); font-size: 0.9em;">
+                     Or click "Start New Cycle" to trigger immediately
+                   </p>
+                 </div>
```

---

## 7. static/css/animations.css
**Location**: `/home/coolhand/projects/foresight/static/css/animations.css`
**Lines**: 155-172
**Change**: Added spin animation for spinner

```diff
  @keyframes rotate {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }

  .rotating {
    animation: rotate 1s linear infinite;
  }

+ /* ===== SPIN ANIMATION (Loading Spinner) ===== */
+ @keyframes spin {
+   from {
+     transform: rotate(0deg);
+   }
+   to {
+     transform: rotate(360deg);
+   }
+ }
+
+ .loading-spinner {
+   animation: spin 1s linear infinite;
+ }

  /* ===== BOUNCE ANIMATION (Alerts) ===== */
```

---

## Summary by File

| File | Type | Changes | Lines |
|------|------|---------|-------|
| requirements.txt | Package | Add 3 LLM packages | 7-10 |
| app/config.py | Config | Reduce cycle interval | 24 |
| app/worker.py | Backend | Health tracking, timing | 40-41, 72-87, 127-128, 115-120, 276-297 |
| app/routes/api.py | Backend | Health endpoint + cycle/start | 119-147, 247-280 |
| app/services/prediction_service.py | Backend | Provider interface fix | 53, 58, 74-78, 82-87, 133-145, 181-190 |
| static/js/app.js | Frontend | Loading state | 308-327 |
| static/css/animations.css | CSS | Spin animation | 155-172 |

---

## Verification Commands

```bash
# Check each file was modified correctly
grep -n "anthropic>=" /home/coolhand/projects/foresight/requirements.txt
grep -n "CYCLE_INTERVAL, 30" /home/coolhand/projects/foresight/app/config.py
grep -n "first_cycle = True" /home/coolhand/projects/foresight/app/worker.py
grep -n "health/providers" /home/coolhand/projects/foresight/app/routes/api.py
grep -n "provider.complete(" /home/coolhand/projects/foresight/app/services/prediction_service.py
grep -n "Waiting for Predictions" /home/coolhand/projects/foresight/static/js/app.js
grep -n "@keyframes spin" /home/coolhand/projects/foresight/static/css/animations.css
```

---

## Git Tracking

All changes are in commit:
```
586d1aa session checkpoint: 2026-02-16 18:11
```

To see all changes:
```bash
git show 586d1aa --stat
git diff 586d1aa^ 586d1aa
```
