"""
Core Base Classes for Enterprise AI Orchestration Platform

This module provides the foundational SwarmModuleBase class that all agents and modules
inherit from, ensuring consistent interfaces and standardized lifecycle management.

Key Features:
- Standardized module lifecycle (initialize, setup, execute, shutdown)
- Health monitoring and status reporting
- Dynamic dependency loading and management
- Configuration validation and environment overrides
- Logging and error handling integration
"""

import asyncio
import json
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml
from pydantic import BaseModel, Field, validator


class ModuleStatus(Enum):
    """Module status enumeration for tracking lifecycle states."""
    INITIALIZING = "initializing"
    LOADING_DEPENDENCIES = "loading_dependencies"
    SETTING_UP = "setting_up"
    READY = "ready"
    RUNNING = "running"
    ERROR = "error"
    SHUTTING_DOWN = "shutting_down"
    STOPPED = "stopped"
    FAILED = "failed"


class TaskPriority(Enum):
    """Task priority levels for workflow scheduling."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class AgentType(Enum):
    """Agent type classification for capability matching."""
    BELTER = "file_processing"
    DRUMMER = "information_gathering"
    DEEPSEEK = "analysis_reasoning"
    CUSTOM = "custom_specialist"


@dataclass
class TaskRequest:
    """Standardized task request structure."""
    id: str
    type: str
    payload: Dict[str, Any]
    priority: TaskPriority
    deadline: Optional[datetime] = None
    context: Dict[str, Any] = field(default_factory=dict)
    required_capabilities: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TaskResult:
    """Standardized task result structure."""
    task_id: str
    status: str
    results: List[Any] = field(default_factory=list)
    execution_time: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    context_updates: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentCapability:
    """Agent capability definition for registry and selection."""
    agent_id: str
    agent_type: AgentType
    capabilities: List[str]
    current_load: float
    max_concurrent: int
    model_info: Dict[str, Any]
    health_status: str
    last_heartbeat: datetime


@dataclass
class WorkflowState:
    """Workflow execution state tracking."""
    workflow_id: str
    status: str
    start_time: datetime
    steps_completed: int
    total_steps: int
    end_time: Optional[datetime] = None
    error: Optional[str] = None


class ModuleConfig(BaseModel):
    """Pydantic model for module configuration validation."""
    module_id: Optional[str] = Field(None, description="Unique module identifier")
    name: str = Field(..., description="Module name")
    version: str = Field("1.0.0", description="Module version")
    description: str = Field("", description="Module description")
    capabilities: List[str] = Field(default_factory=list, description="Module capabilities")
    dependencies: List[str] = Field(default_factory=list, description="Required dependencies")
    max_concurrent: int = Field(5, description="Maximum concurrent tasks")
    timeout: int = Field(300, description="Task timeout in seconds")
    retry_attempts: int = Field(3, description="Number of retry attempts")
    health_check_interval: int = Field(30, description="Health check interval in seconds")
    
    @validator('capabilities')
    def validate_capabilities(cls, v):
        """Validate that capabilities are non-empty strings."""
        if not all(isinstance(cap, str) and cap.strip() for cap in v):
            raise ValueError("All capabilities must be non-empty strings")
        return v


class SwarmModuleBase(ABC):
    """
    Base class for all Swarm modules with standardized lifecycle management.
    
    This class provides the foundation for all agents and modules in the enterprise
    orchestration platform, ensuring consistent interfaces, health monitoring,
    and dependency management.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the module with configuration.
        
        Args:
            config: Module configuration dictionary
        """
        # Validate and store configuration
        self.config = ModuleConfig(**config)
        self.module_id = self.config.module_id or f"{self.__class__.__name__}_{id(self)}"
        
        # Initialize status and metadata
        self.status = ModuleStatus.INITIALIZING
        self.capabilities = self.config.capabilities.copy()
        self.dependencies = self.config.dependencies.copy()
        self.current_load = 0.0
        self.max_concurrent = self.config.max_concurrent
        
        # Performance tracking
        self.start_time = datetime.now()
        self.last_heartbeat = datetime.now()
        self.tasks_completed = 0
        self.tasks_failed = 0
        self.total_execution_time = 0.0
        
        # Setup logging
        self.logger = logging.getLogger(f"swarm.{self.module_id}")
        self.logger.setLevel(logging.INFO)
        
        # Task tracking
        self.active_tasks: Dict[str, TaskRequest] = {}
        self.task_history: List[TaskResult] = []
        
        # Health monitoring
        self.last_health_check = datetime.now()
        self.health_status = "initializing"
        self.error_count = 0
        
        self.logger.info(f"Module {self.module_id} initialized with {len(self.capabilities)} capabilities")
    
    async def initialize(self) -> bool:
        """
        Initialize the module and its dependencies.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            self.status = ModuleStatus.LOADING_DEPENDENCIES
            self.logger.info(f"Initializing module {self.module_id}")
            
            # Load dependencies
            await self._load_dependencies()
            
            # Setup module-specific components
            self.status = ModuleStatus.SETTING_UP
            await self.setup_module()
            
            # Validate setup
            if await self._validate_setup():
                self.status = ModuleStatus.READY
                self.health_status = "healthy"
                self.logger.info(f"Module {self.module_id} initialized successfully")
                return True
            else:
                self.status = ModuleStatus.FAILED
                self.health_status = "unhealthy"
                self.logger.error(f"Module {self.module_id} setup validation failed")
                return False
                
        except Exception as e:
            self.status = ModuleStatus.FAILED
            self.health_status = "unhealthy"
            self.error_count += 1
            self.logger.error(f"Failed to initialize module {self.module_id}: {e}")
            raise ModuleInitializationError(f"Failed to initialize {self.module_id}: {e}")
    
    async def _load_dependencies(self) -> None:
        """Load required dependencies for the module."""
        self.logger.debug(f"Loading {len(self.dependencies)} dependencies")
        
        for dependency in self.dependencies:
            try:
                await self._load_dependency(dependency)
                self.logger.debug(f"Loaded dependency: {dependency}")
            except Exception as e:
                self.logger.error(f"Failed to load dependency {dependency}: {e}")
                raise
    
    async def _load_dependency(self, dependency: str) -> None:
        """
        Load a specific dependency.
        
        Args:
            dependency: Dependency identifier to load
        """
        # Implementation depends on dependency type
        # This could be module imports, API connections, etc.
        self.logger.debug(f"Loading dependency: {dependency}")
        
        # Simulate dependency loading
        await asyncio.sleep(0.1)
    
    @abstractmethod
    async def setup_module(self) -> None:
        """
        Module-specific setup logic.
        
        Subclasses must implement this method to perform their specific
        initialization tasks such as model loading, API client setup, etc.
        """
        raise NotImplementedError("Subclasses must implement setup_module")
    
    async def _validate_setup(self) -> bool:
        """
        Validate that the module setup was successful.
        
        Returns:
            bool: True if setup is valid, False otherwise
        """
        # Basic validation - can be overridden by subclasses
        return (
            self.status != ModuleStatus.FAILED and
            len(self.capabilities) > 0 and
            hasattr(self, 'module_id')
        )
    
    @abstractmethod
    async def execute_task(self, task: TaskRequest) -> TaskResult:
        """
        Execute a task.
        
        Args:
            task: Task request to execute
            
        Returns:
            TaskResult: Result of task execution
        """
        raise NotImplementedError("Subclasses must implement execute_task")
    
    async def process_task(self, task: TaskRequest) -> TaskResult:
        """
        Process a task with full lifecycle management.
        
        Args:
            task: Task request to process
            
        Returns:
            TaskResult: Result of task processing
        """
        start_time = time.time()
        self.active_tasks[task.id] = task
        self.current_load = len(self.active_tasks) / self.max_concurrent
        
        try:
            # Update status
            self.status = ModuleStatus.RUNNING
            self.logger.info(f"Processing task {task.id} of type {task.type}")
            
            # Execute the task
            result = await self.execute_task(task)
            
            # Update metrics
            execution_time = time.time() - start_time
            result.execution_time = execution_time
            self.total_execution_time += execution_time
            self.tasks_completed += 1
            
            # Store in history
            self.task_history.append(result)
            
            self.logger.info(f"Task {task.id} completed in {execution_time:.2f}s")
            return result
            
        except Exception as e:
            # Handle task failure
            execution_time = time.time() - start_time
            self.tasks_failed += 1
            self.error_count += 1
            
            error_result = TaskResult(
                task_id=task.id,
                status="failed",
                execution_time=execution_time,
                error=str(e)
            )
            
            self.task_history.append(error_result)
            self.logger.error(f"Task {task.id} failed after {execution_time:.2f}s: {e}")
            
            return error_result
            
        finally:
            # Cleanup
            self.active_tasks.pop(task.id, None)
            self.current_load = len(self.active_tasks) / self.max_concurrent
            self.status = ModuleStatus.READY if not self.active_tasks else ModuleStatus.RUNNING
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform health check and return status.
        
        Returns:
            Dict containing health status and metrics
        """
        self.last_health_check = datetime.now()
        
        # Calculate uptime
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        # Calculate performance metrics
        avg_execution_time = (
            self.total_execution_time / self.tasks_completed
            if self.tasks_completed > 0 else 0.0
        )
        
        success_rate = (
            self.tasks_completed / (self.tasks_completed + self.tasks_failed)
            if (self.tasks_completed + self.tasks_failed) > 0 else 1.0
        )
        
        # Determine health status
        if self.status in [ModuleStatus.READY, ModuleStatus.RUNNING]:
            if self.error_count < 5 and success_rate > 0.9:
                self.health_status = "healthy"
            elif self.error_count < 10 and success_rate > 0.7:
                self.health_status = "degraded"
            else:
                self.health_status = "unhealthy"
        else:
            self.health_status = "unhealthy"
        
        return {
            "module_id": self.module_id,
            "status": self.status.value,
            "health_status": self.health_status,
            "uptime_seconds": uptime,
            "current_load": self.current_load,
            "active_tasks": len(self.active_tasks),
            "tasks_completed": self.tasks_completed,
            "tasks_failed": self.tasks_failed,
            "success_rate": success_rate,
            "avg_execution_time": avg_execution_time,
            "error_count": self.error_count,
            "capabilities": self.capabilities,
            "last_heartbeat": self.last_heartbeat.isoformat()
        }
    
    async def get_metrics(self) -> Dict[str, Any]:
        """
        Get detailed performance metrics.
        
        Returns:
            Dict containing performance metrics
        """
        health = await self.health_check()
        
        # Add additional metrics
        recent_tasks = self.task_history[-10:] if self.task_history else []
        recent_success_rate = (
            len([t for t in recent_tasks if t.status != "failed"]) / len(recent_tasks)
            if recent_tasks else 1.0
        )
        
        return {
            **health,
            "recent_success_rate": recent_success_rate,
            "recent_tasks": len(recent_tasks),
            "memory_usage": self._get_memory_usage(),
            "cpu_usage": self._get_cpu_usage()
        }
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage percentage."""
        # Placeholder - would implement actual memory monitoring
        return 0.0
    
    def _get_cpu_usage(self) -> float:
        """Get current CPU usage percentage."""
        # Placeholder - would implement actual CPU monitoring
        return 0.0
    
    async def shutdown(self) -> None:
        """Graceful shutdown of the module."""
        self.logger.info(f"Shutting down module {self.module_id}")
        self.status = ModuleStatus.SHUTTING_DOWN
        
        # Wait for active tasks to complete (with timeout)
        timeout = 30  # seconds
        start_time = time.time()
        
        while self.active_tasks and (time.time() - start_time) < timeout:
            self.logger.info(f"Waiting for {len(self.active_tasks)} active tasks to complete")
            await asyncio.sleep(1)
        
        if self.active_tasks:
            self.logger.warning(f"Forcefully stopping {len(self.active_tasks)} active tasks")
        
        # Cleanup resources
        await self._cleanup_resources()
        
        self.status = ModuleStatus.STOPPED
        self.logger.info(f"Module {self.module_id} shutdown complete")
    
    async def _cleanup_resources(self) -> None:
        """Cleanup module-specific resources."""
        # Override in subclasses for specific cleanup
        pass
    
    def __repr__(self) -> str:
        """String representation of the module."""
        return (
            f"{self.__class__.__name__}("
            f"id={self.module_id}, "
            f"status={self.status.value}, "
            f"capabilities={len(self.capabilities)}, "
            f"load={self.current_load:.2f})"
        )


class ModuleInitializationError(Exception):
    """Exception raised when module initialization fails."""
    pass


class NoSuitableAgentError(Exception):
    """Exception raised when no suitable agent is found for a task."""
    pass


class NoSuitableModuleError(Exception):
    """Exception raised when no suitable module is found for a task."""
    pass


class UnsupportedTaskError(Exception):
    """Exception raised when a task type is not supported by an agent."""
    pass
