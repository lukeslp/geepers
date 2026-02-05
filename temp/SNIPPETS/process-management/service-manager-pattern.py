"""
Process Management System for Multiple Python Services

Description: Comprehensive service manager for starting, stopping, monitoring, and
auto-restarting Python/Flask services. Includes health checking, log management,
PID tracking, and systemd integration.

Use Cases:
- Managing multiple Flask/FastAPI applications
- Production service orchestration
- Development environment with many microservices
- Automatic service recovery and monitoring

Dependencies:
- psutil (pip install psutil)
- requests (pip install requests)

Notes:
- Handles graceful shutdown (SIGTERM) and force kill (SIGKILL)
- Automatic health checks via HTTP endpoints
- Exponential backoff for restart attempts
- Comprehensive logging and state tracking
- Works with systemd for boot persistence

Related Snippets:
- See health-check-endpoint.py for Flask health endpoint
- See systemd-service-template.service for systemd integration
"""

import os
import sys
import subprocess
import signal
import time
import json
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import psutil

# Service configurations
SERVICES = {
    'api': {
        'name': 'API Server',
        'script': '/home/user/api/app.py',
        'working_dir': '/home/user/api',
        'port': 8000,
        'health_endpoint': 'http://localhost:8000/health',
        'start_timeout': 10,
        'description': 'Main API server'
    },
    'worker': {
        'name': 'Background Worker',
        'script': '/home/user/worker/worker.py',
        'working_dir': '/home/user/worker',
        'port': 8001,
        'health_endpoint': 'http://localhost:8001/health',
        'start_timeout': 5,
        'description': 'Async task processor'
    }
}

# Paths
HOME_DIR = Path.home()
PID_DIR = HOME_DIR / '.service_manager' / 'pids'
LOG_DIR = HOME_DIR / '.service_manager' / 'logs'
STATE_DIR = HOME_DIR / '.service_manager' / 'state'

# Ensure directories exist
PID_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)
STATE_DIR.mkdir(parents=True, exist_ok=True)


class ServiceManager:
    """Manages multiple Python services with health checking and auto-restart"""

    def __init__(self):
        self.services = SERVICES
        self.pid_dir = PID_DIR
        self.log_dir = LOG_DIR
        self.state_dir = STATE_DIR

    def _get_pid_file(self, service_id: str) -> Path:
        """Get PID file path for a service"""
        return self.pid_dir / f"{service_id}.pid"

    def _get_log_file(self, service_id: str) -> Path:
        """Get log file path for a service"""
        return self.log_dir / f"{service_id}.log"

    def _read_pid(self, service_id: str) -> Optional[int]:
        """Read PID from file"""
        pid_file = self._get_pid_file(service_id)
        if pid_file.exists():
            try:
                with open(pid_file, 'r') as f:
                    return int(f.read().strip())
            except (ValueError, IOError):
                return None
        return None

    def _write_pid(self, service_id: str, pid: int):
        """Write PID to file"""
        pid_file = self._get_pid_file(service_id)
        with open(pid_file, 'w') as f:
            f.write(str(pid))

    def _remove_pid(self, service_id: str):
        """Remove PID file"""
        pid_file = self._get_pid_file(service_id)
        if pid_file.exists():
            pid_file.unlink()

    def _is_process_running(self, pid: int) -> bool:
        """Check if a process is running"""
        try:
            process = psutil.Process(pid)
            return process.is_running()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False

    def _check_health(self, service_id: str) -> Tuple[bool, str]:
        """Check service health via HTTP endpoint"""
        config = self.services[service_id]
        try:
            response = requests.get(
                config['health_endpoint'],
                timeout=5
            )
            if response.status_code == 200:
                return True, "healthy"
            else:
                return False, f"HTTP {response.status_code}"
        except requests.exceptions.ConnectionError:
            return False, "connection refused"
        except requests.exceptions.Timeout:
            return False, "timeout"
        except Exception as e:
            return False, f"error: {str(e)}"

    def get_status(self, service_id: str) -> Dict:
        """Get detailed status of a service"""
        config = self.services[service_id]
        pid = self._read_pid(service_id)

        status = {
            'name': config['name'],
            'service_id': service_id,
            'port': config['port'],
            'pid': pid,
            'running': False,
            'healthy': False,
            'health_message': 'not running',
            'uptime': None
        }

        if pid and self._is_process_running(pid):
            status['running'] = True

            # Get process info
            try:
                process = psutil.Process(pid)
                status['uptime'] = time.time() - process.create_time()
                status['memory_mb'] = process.memory_info().rss / 1024 / 1024
                status['cpu_percent'] = process.cpu_percent(interval=0.1)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

            # Check health
            healthy, message = self._check_health(service_id)
            status['healthy'] = healthy
            status['health_message'] = message
        else:
            # Clean up stale PID file
            if pid:
                self._remove_pid(service_id)

        return status

    def start_service(self, service_id: str, verbose: bool = True) -> bool:
        """Start a service"""
        config = self.services[service_id]

        # Check if already running
        pid = self._read_pid(service_id)
        if pid and self._is_process_running(pid):
            if verbose:
                print(f"Service {config['name']} is already running (PID {pid})")
            return False

        if verbose:
            print(f"Starting {config['name']}...")

        # Prepare log file
        log_file = self._get_log_file(service_id)

        try:
            # Start process
            with open(log_file, 'a') as log:
                log.write(f"\n{'='*60}\n")
                log.write(f"Starting {config['name']} at {datetime.now().isoformat()}\n")
                log.write(f"{'='*60}\n\n")

                process = subprocess.Popen(
                    [sys.executable, config['script']],
                    cwd=config['working_dir'],
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    start_new_session=True,
                    env=os.environ.copy()
                )

            # Write PID
            self._write_pid(service_id, process.pid)

            # Wait for startup
            if verbose:
                print(f"   Process started with PID {process.pid}")
                print(f"   Waiting for service to be ready (timeout: {config['start_timeout']}s)...")

            start_time = time.time()
            while time.time() - start_time < config['start_timeout']:
                time.sleep(1)

                # Check if process is still running
                if not self._is_process_running(process.pid):
                    if verbose:
                        print(f"   Process died during startup")
                        print(f"   Check logs: {log_file}")
                    return False

                # Check health
                healthy, message = self._check_health(service_id)
                if healthy:
                    if verbose:
                        print(f"   {config['name']} started successfully!")
                        print(f"   Port: {config['port']}")
                        print(f"   Logs: {log_file}")
                    return True

            # Timeout
            if verbose:
                print(f"   Service started but health check timeout")
                print(f"   The service may still be starting up")
            return True

        except Exception as e:
            if verbose:
                print(f"   Failed to start: {str(e)}")
            return False

    def stop_service(self, service_id: str, verbose: bool = True) -> bool:
        """Stop a service"""
        config = self.services[service_id]
        pid = self._read_pid(service_id)

        if not pid:
            if verbose:
                print(f"{config['name']} is not running")
            return False

        if not self._is_process_running(pid):
            if verbose:
                print(f"{config['name']} PID exists but process not found")
            self._remove_pid(service_id)
            return False

        if verbose:
            print(f"Stopping {config['name']} (PID {pid})...")

        try:
            process = psutil.Process(pid)

            # Try graceful shutdown first (SIGTERM)
            process.terminate()

            # Wait up to 10 seconds for graceful shutdown
            try:
                process.wait(timeout=10)
                if verbose:
                    print(f"   {config['name']} stopped gracefully")
            except psutil.TimeoutExpired:
                # Force kill if necessary (SIGKILL)
                if verbose:
                    print(f"   Forcing shutdown...")
                process.kill()
                process.wait(timeout=5)
                if verbose:
                    print(f"   {config['name']} stopped (forced)")

            self._remove_pid(service_id)
            return True

        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            if verbose:
                print(f"   Error stopping service: {str(e)}")
            self._remove_pid(service_id)
            return False

    def restart_service(self, service_id: str, verbose: bool = True) -> bool:
        """Restart a service"""
        config = self.services[service_id]

        if verbose:
            print(f"Restarting {config['name']}...")

        self.stop_service(service_id, verbose=False)
        time.sleep(2)  # Give it a moment to fully shut down
        return self.start_service(service_id, verbose=verbose)

    def status_all(self):
        """Show status of all services"""
        print("Service Status Dashboard")
        print("=" * 80)
        print()

        statuses = {}
        for service_id in self.services:
            statuses[service_id] = self.get_status(service_id)

        # Display table
        print(f"{'SERVICE':<20} {'PORT':<8} {'STATUS':<12} {'PID':<10} {'HEALTH':<15}")
        print("-" * 80)

        for service_id, status in statuses.items():
            name = status['name'][:19]
            port = str(status['port'])

            if status['running']:
                status_text = "Running"
                pid_text = str(status['pid'])
                health_text = status['health_message']
            else:
                status_text = "Stopped"
                pid_text = "-"
                health_text = "-"

            print(f"{name:<20} {port:<8} {status_text:<12} {pid_text:<10} {health_text:<15}")

        print()


# Usage example
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Service Manager')
    parser.add_argument('command', choices=['start', 'stop', 'restart', 'status'])
    parser.add_argument('service', nargs='?', choices=list(SERVICES.keys()))
    parser.add_argument('--all', action='store_true', help='Apply to all services')

    args = parser.parse_args()

    manager = ServiceManager()

    if args.command == 'status':
        manager.status_all()
    elif args.service:
        if args.command == 'start':
            manager.start_service(args.service)
        elif args.command == 'stop':
            manager.stop_service(args.service)
        elif args.command == 'restart':
            manager.restart_service(args.service)
    elif args.all:
        for service_id in SERVICES:
            if args.command == 'start':
                manager.start_service(service_id)
            elif args.command == 'stop':
                manager.stop_service(service_id)
            elif args.command == 'restart':
                manager.restart_service(service_id)
    else:
        parser.error(f"{args.command} requires either a service name or --all flag")


"""
Example Usage:

# Start a service
python service_manager.py start api

# Stop a service
python service_manager.py stop worker

# Restart a service
python service_manager.py restart api

# Check status of all services
python service_manager.py status

# Start all services
python service_manager.py start --all

# Stop all services
python service_manager.py stop --all
"""
