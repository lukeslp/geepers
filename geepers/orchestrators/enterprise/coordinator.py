"""
Caminaå Central Coordinator

The central orchestration engine for the Enterprise AI Orchestration Platform.
Uses Mistral-small:22b for intelligent task routing and workflow management
across specialized agent teams.

Key Features:
- Intelligent task analysis and routing
- Multi-agent workflow orchestration
- Load balancing and resource optimization
- Real-time monitoring and health checks
- Scalable architecture with Redis messaging
"""

import asyncio
import json
import logging
import redis
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from .base import (
    SwarmModuleBase, TaskRequest, TaskResult, TaskPriority,
    AgentCapability, WorkflowState, ModuleStatus, AgentType
)

# Import from installed shared library (installed via pip install -e)
from shared.llm_providers import ProviderFactory, Message


@dataclass
class TaskAnalysis:
    """Analysis results from Mistral-small for task optimization."""
    complexity_score: float
    estimated_duration: str
    required_agents: List[str]
    workflow_pattern: str
    risk_factors: List[str]
    optimization_suggestions: List[str]
    
    @classmethod
    def from_json(cls, json_str: str) -> 'TaskAnalysis':
        """Create TaskAnalysis from JSON response."""
        try:
            data = json.loads(json_str)
            return cls(**data)
        except (json.JSONDecodeError, TypeError) as e:
            # Fallback to default analysis
            logging.warning(f"Failed to parse task analysis: {e}")
            return cls(
                complexity_score=5.0,
                estimated_duration="5 minutes",
                required_agents=["belter"],
                workflow_pattern="sequential",
                risk_factors=["unknown_complexity"],
                optimization_suggestions=["monitor_execution"]
            )


@dataclass
class Workflow:
    """Workflow definition with execution strategy."""
    id: str
    task_id: str
    steps: List[Dict[str, Any]]
    execution_strategy: str
    estimated_duration: str
    priority: TaskPriority


class CaminaCoordinator(SwarmModuleBase):
    """
    Central coordinator using Mistral-small:22b for intelligent task routing
    and workflow orchestration across specialized agent teams.
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        # Store the raw config for accessing nested structures
        self.raw_config = config
        self.capabilities = [
            "task_coordination", "workflow_orchestration", "agent_management",
            "load_balancing", "intelligent_routing", "performance_optimization"
        ]
        
        # Core components
        self.redis_client = None
        self.agent_registry: Dict[str, AgentCapability] = {}
        self.active_workflows: Dict[str, WorkflowState] = {}
        self.task_queue = None
        self.mistral_client = None
        
        # Performance metrics
        self.tasks_routed = 0
        self.workflows_completed = 0
        self.average_response_time = 0.0
        
        self.logger = logging.getLogger("camina.coordinator")
        
    async def setup_module(self):
        """Initialize the coordinator and its components."""
        try:
            # Initialize Redis connection
            redis_config = self.raw_config.get('redis', {})
            self.redis_client = redis.Redis(
                host=redis_config.get('host', 'localhost'),
                port=redis_config.get('port', 6379),
                decode_responses=True
            )
            
            # Initialize task queue
            self.task_queue = TaskQueue(self.redis_client)
            
            # Initialize Mistral client
            await self._initialize_mistral_client()
            
            # Start agent discovery
            await self.discover_agents()
            
            # Start health monitoring
            await self.start_health_monitoring()
            
            self.logger.info("Caminaå Coordinator initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to setup coordinator: {e}")
            raise
    
    async def _initialize_mistral_client(self):
        """Initialize Mistral client for task analysis."""
        try:
            # Initialize Mistral client using shared library
            self.mistral_client = ProviderFactory.get_provider('mistral')
            self.model = "mistral-small-latest"
            self.logger.info(f"Mistral client initialized using shared library provider")
        except Exception as e:
            self.logger.error(f"Failed to initialize Mistral client: {e}")
            raise
    
    async def discover_agents(self):
        """Discover and register available agents."""
        try:
            # In a real implementation, this would discover agents from the network
            # For now, we'll register some mock agents
            
            # Register Belter agents
            belter_agent = AgentCapability(
                agent_id="belter-001",
                agent_type=AgentType.BELTER,
                capabilities=["file_analysis", "document_processing", "data_extraction"],
                current_load=0.0,
                max_concurrent=5,
                model_info={"model": "mistral-7b-latest", "provider": "mistral"},
                health_status="healthy",
                last_heartbeat=datetime.now()
            )
            self.agent_registry["belter-001"] = belter_agent
            
            # Register Drummer agents
            drummer_agent = AgentCapability(
                agent_id="drummer-001",
                agent_type=AgentType.DRUMMER,
                capabilities=["web_search", "api_integration", "data_gathering"],
                current_load=0.0,
                max_concurrent=3,
                model_info={"model": "gpt-4-mini", "provider": "openai"},
                health_status="healthy",
                last_heartbeat=datetime.now()
            )
            self.agent_registry["drummer-001"] = drummer_agent
            
            # Register DeepSeek Reasoner agents
            deepseek_agent = AgentCapability(
                agent_id="deepseek-001",
                agent_type=AgentType.DEEPSEEK,
                capabilities=["complex_reasoning", "logical_analysis", "synthesis"],
                current_load=0.0,
                max_concurrent=2,
                model_info={"model": "deepseek-r1:7b", "provider": "deepseek"},
                health_status="healthy",
                last_heartbeat=datetime.now()
            )
            self.agent_registry["deepseek-001"] = deepseek_agent
            
            self.logger.info(f"Discovered {len(self.agent_registry)} agents")
            
        except Exception as e:
            self.logger.error(f"Failed to discover agents: {e}")
            raise
    
    async def start_health_monitoring(self):
        """Start periodic health monitoring of agents."""
        asyncio.create_task(self._health_monitor_loop())
    
    async def _health_monitor_loop(self):
        """Continuous health monitoring loop."""
        while self.status != ModuleStatus.STOPPED:
            try:
                await self._check_agent_health()
                await asyncio.sleep(30)  # Check every 30 seconds
            except Exception as e:
                self.logger.error(f"Health monitoring error: {e}")
                await asyncio.sleep(5)
    
    async def _check_agent_health(self):
        """Check health of all registered agents."""
        current_time = datetime.now()
        
        for agent_id, agent in self.agent_registry.items():
            # Check if agent has responded recently
            time_since_heartbeat = (current_time - agent.last_heartbeat).total_seconds()
            
            if time_since_heartbeat > 120:  # 2 minutes timeout
                agent.health_status = "unhealthy"
                self.logger.warning(f"Agent {agent_id} marked as unhealthy")
    
    async def execute_task(self, task: TaskRequest) -> TaskResult:
        """
        Main entry point for task processing with intelligent routing.
        """
        try:
            start_time = datetime.now()
            self.logger.info(f"Processing task {task.id} of type {task.type}")
            
            # Analyze task requirements using Mistral-small
            analysis = await self.analyze_task_requirements(task)
            
            # Determine optimal workflow
            workflow = await self.design_workflow(task, analysis)
            
            # Execute workflow with monitoring
            result = await self.execute_workflow(workflow)
            
            # Update metrics
            execution_time = (datetime.now() - start_time).total_seconds()
            self.tasks_routed += 1
            self.average_response_time = (
                (self.average_response_time * (self.tasks_routed - 1) + execution_time)
                / self.tasks_routed
            )
            
            self.logger.info(f"Task {task.id} completed in {execution_time:.2f}s")
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to execute task {task.id}: {e}")
            return TaskResult(
                task_id=task.id,
                status="failed",
                error=str(e)
            )
    
    async def analyze_task_requirements(self, task: TaskRequest) -> TaskAnalysis:
        """Use Mistral-small:22b to analyze task and determine optimal approach."""
        
        analysis_prompt = f"""
        Analyze this task request and determine the optimal execution strategy:
        
        Task Type: {task.type}
        Priority: {task.priority.name}
        Required Capabilities: {task.required_capabilities}
        Context: {json.dumps(task.context, indent=2)}
        
        Available Agent Types:
        - Belter: File processing, manipulation, analysis
        - Drummer: Information gathering, web search, API calls
        - DeepSeek: Complex reasoning, analysis, synthesis
        - Custom: Domain-specific specialized capabilities
        
        Provide analysis in JSON format:
        {{
            "complexity_score": 1-10,
            "estimated_duration": "X minutes",
            "required_agents": ["agent_type1", "agent_type2"],
            "workflow_pattern": "sequential|parallel|hybrid",
            "risk_factors": ["factor1", "factor2"],
            "optimization_suggestions": ["suggestion1", "suggestion2"]
        }}
        """
        
        try:
            # Use Message interface from shared library
            messages = [Message(role="user", content=analysis_prompt)]

            # Run synchronous complete() in thread pool to avoid blocking
            response = await asyncio.to_thread(
                self.mistral_client.complete,
                messages=messages,
                model=self.model,
                max_tokens=500,
                temperature=0.1
            )

            return TaskAnalysis.from_json(response.content)
            
        except Exception as e:
            self.logger.warning(f"Failed to analyze task with Mistral: {e}")
            # Return default analysis
            return TaskAnalysis(
                complexity_score=5.0,
                estimated_duration="5 minutes",
                required_agents=["belter"],
                workflow_pattern="sequential",
                risk_factors=["analysis_unavailable"],
                optimization_suggestions=["use_default_routing"]
            )
    
    async def design_workflow(self, task: TaskRequest, analysis: TaskAnalysis) -> Workflow:
        """Design optimal workflow based on task analysis."""
        
        workflow_steps = []
        
        # Sequential workflow for complex analysis
        if analysis.workflow_pattern == "sequential":
            workflow_steps = await self._design_sequential_workflow(task, analysis)
        
        # Parallel workflow for independent tasks
        elif analysis.workflow_pattern == "parallel":
            workflow_steps = await self._design_parallel_workflow(task, analysis)
        
        # Hybrid workflow for complex scenarios
        elif analysis.workflow_pattern == "hybrid":
            workflow_steps = await self._design_hybrid_workflow(task, analysis)
        
        return Workflow(
            id=f"workflow_{task.id}",
            task_id=task.id,
            steps=workflow_steps,
            execution_strategy=analysis.workflow_pattern,
            estimated_duration=analysis.estimated_duration,
            priority=task.priority
        )
    
    async def _design_sequential_workflow(self, task: TaskRequest, analysis: TaskAnalysis) -> List[Dict[str, Any]]:
        """Design sequential workflow steps."""
        steps = []
        
        for i, agent_type in enumerate(analysis.required_agents):
            step = {
                "step_id": f"step_{i+1}",
                "agent_type": agent_type,
                "task_type": task.type,
                "required_capabilities": task.required_capabilities,
                "dependencies": [f"step_{i}"] if i > 0 else []
            }
            steps.append(step)
        
        return steps
    
    async def _design_parallel_workflow(self, task: TaskRequest, analysis: TaskAnalysis) -> List[Dict[str, Any]]:
        """Design parallel workflow steps."""
        steps = []
        
        for i, agent_type in enumerate(analysis.required_agents):
            step = {
                "step_id": f"parallel_step_{i+1}",
                "agent_type": agent_type,
                "task_type": task.type,
                "required_capabilities": task.required_capabilities,
                "dependencies": []  # No dependencies for parallel execution
            }
            steps.append(step)
        
        return steps
    
    async def _design_hybrid_workflow(self, task: TaskRequest, analysis: TaskAnalysis) -> List[Dict[str, Any]]:
        """Design hybrid workflow with both sequential and parallel steps."""
        # Simplified hybrid approach
        steps = await self._design_sequential_workflow(task, analysis)
        return steps
    
    async def execute_workflow(self, workflow: Workflow) -> TaskResult:
        """Execute workflow with monitoring and error handling."""
        
        workflow_state = WorkflowState(
            workflow_id=workflow.id,
            status="running",
            start_time=datetime.now(),
            steps_completed=0,
            total_steps=len(workflow.steps)
        )
        
        self.active_workflows[workflow.id] = workflow_state
        
        try:
            # Execute based on strategy
            if workflow.execution_strategy == "sequential":
                result = await self._execute_sequential(workflow)
            elif workflow.execution_strategy == "parallel":
                result = await self._execute_parallel(workflow)
            elif workflow.execution_strategy == "hybrid":
                result = await self._execute_hybrid(workflow)
            else:
                raise ValueError(f"Unknown execution strategy: {workflow.execution_strategy}")
            
            workflow_state.status = "completed"
            workflow_state.end_time = datetime.now()
            self.workflows_completed += 1
            
            return result
            
        except Exception as e:
            workflow_state.status = "failed"
            workflow_state.error = str(e)
            self.logger.error(f"Workflow {workflow.id} failed: {e}")
            raise
        finally:
            # Cleanup
            self.active_workflows.pop(workflow.id, None)
    
    async def _execute_sequential(self, workflow: Workflow) -> TaskResult:
        """Execute workflow steps sequentially."""
        results = []
        context = {}
        
        for step in workflow.steps:
            # Select optimal agent for this step
            agent = await self._select_agent(step.get("required_capabilities", []), context)
            
            # Execute step
            step_result = await self._execute_step(agent, step, context)
            results.append(step_result)
            
            # Update context for next step
            if hasattr(step_result, 'context_updates'):
                context.update(step_result.context_updates)
            
            # Update workflow progress
            workflow_state = self.active_workflows[workflow.id]
            workflow_state.steps_completed += 1
        
        return TaskResult(
            task_id=workflow.task_id,
            status="completed",
            results=results,
            metadata={"workflow_type": "sequential"}
        )
    
    async def _execute_parallel(self, workflow: Workflow) -> TaskResult:
        """Execute workflow steps in parallel."""
        # Execute all steps concurrently
        step_tasks = []
        
        for step in workflow.steps:
            agent = await self._select_agent(step.get("required_capabilities", []))
            task_coro = self._execute_step(agent, step)
            step_tasks.append(task_coro)
        
        # Wait for all steps to complete
        results = await asyncio.gather(*step_tasks)
        
        return TaskResult(
            task_id=workflow.task_id,
            status="completed",
            results=results,
            metadata={"workflow_type": "parallel"}
        )
    
    async def _execute_hybrid(self, workflow: Workflow) -> TaskResult:
        """Execute hybrid workflow."""
        # Simplified - treat as sequential for now
        return await self._execute_sequential(workflow)
    
    async def _select_agent(self, capabilities: List[str], context: Dict = None) -> AgentCapability:
        """Intelligently select the best agent for given capabilities."""
        
        # Filter agents by required capabilities
        candidate_agents = [
            agent for agent in self.agent_registry.values()
            if all(cap in agent.capabilities for cap in capabilities)
            and agent.health_status == "healthy"
        ]
        
        if not candidate_agents:
            raise Exception(f"No suitable agents found for capabilities: {capabilities}")
        
        # Score agents based on load and performance
        best_agent = min(candidate_agents, key=lambda agent: agent.current_load)
        
        return best_agent
    
    async def _execute_step(self, agent: AgentCapability, step: Dict[str, Any], context: Dict = None) -> TaskResult:
        """Execute a single workflow step using real agent (LLM provider)."""

        try:
            # Get provider based on agent's model info
            provider_name = agent.model_info.get("provider", "mistral")
            model_name = agent.model_info.get("model", "mistral-small-latest")

            # Get the provider from shared library
            provider = ProviderFactory.get_provider(provider_name)

            # Build the agent's execution prompt based on agent type and step
            task_type = step.get("task_type", "unknown")
            task_description = step.get("description", "")
            task_data = step.get("data", {})

            # Construct agent-specific system message
            if agent.agent_type == AgentType.BELTER:
                system_msg = "You are a file processing and document analysis specialist. Analyze data and extract relevant information."
            elif agent.agent_type == AgentType.DRUMMER:
                system_msg = "You are a web search and data gathering specialist. Find and synthesize information from multiple sources."
            elif agent.agent_type == AgentType.DEEPSEEK:
                system_msg = "You are a complex reasoning and logical analysis specialist. Provide deep insights and synthesize information."
            else:
                system_msg = "You are an AI assistant helping with task execution."

            # Build user message with task details
            user_msg = f"""Task Type: {task_type}
Description: {task_description}
Data: {json.dumps(task_data, indent=2)}
Context: {json.dumps(context or {}, indent=2)}

Please execute this task and provide results."""

            # Create messages
            messages = [
                Message(role="system", content=system_msg),
                Message(role="user", content=user_msg)
            ]

            # Execute using provider (run in thread pool for async compatibility)
            response = await asyncio.to_thread(
                provider.complete,
                messages=messages,
                model=model_name,
                max_tokens=1000,
                temperature=0.3
            )

            # Create task result with actual LLM response
            step_result = TaskResult(
                task_id=step["step_id"],
                status="completed",
                results=[response.content],
                metadata={
                    "agent_id": agent.agent_id,
                    "agent_type": agent.agent_type,
                    "step_type": task_type,
                    "model": model_name,
                    "provider": provider_name,
                    "tokens_used": response.usage.get("total_tokens", 0) if hasattr(response, 'usage') else 0
                }
            )

            self.logger.info(f"Step {step['step_id']} executed by {agent.agent_id} using {provider_name}/{model_name}")

            return step_result

        except Exception as e:
            self.logger.error(f"Failed to execute step {step.get('step_id')}: {e}")
            # Return error result instead of raising
            return TaskResult(
                task_id=step.get("step_id", "unknown"),
                status="failed",
                results=[f"Error: {str(e)}"],
                metadata={
                    "agent_id": agent.agent_id,
                    "error": str(e)
                }
            )
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        
        agent_summary = {}
        for agent_type in [AgentType.BELTER, AgentType.DRUMMER, AgentType.DEEPSEEK]:
            agents = [a for a in self.agent_registry.values() if a.agent_type == agent_type]
            healthy_count = len([a for a in agents if a.health_status == "healthy"])
            
            agent_summary[agent_type.value] = {
                "total": len(agents),
                "healthy": healthy_count,
                "average_load": sum(a.current_load for a in agents) / len(agents) if agents else 0
            }
        
        return {
            "coordinator_status": self.status.value,
            "total_agents": len(self.agent_registry),
            "active_workflows": len(self.active_workflows),
            "tasks_routed": self.tasks_routed,
            "workflows_completed": self.workflows_completed,
            "average_response_time": self.average_response_time,
            "agent_summary": agent_summary,
            "system_health": "healthy" if len(self.agent_registry) > 0 else "degraded"
        }


class TaskQueue:
    """Redis-based task queue for distributed processing."""
    
    def __init__(self, redis_client):
        self.redis_client = redis_client
        self.queue_name = "swarm:tasks"
    
    async def enqueue(self, task: TaskRequest):
        """Add task to the queue."""
        task_data = {
            "id": task.id,
            "type": task.type,
            "payload": task.payload,
            "priority": task.priority.value,
            "timestamp": datetime.now().isoformat()
        }
        
        # Use Redis sorted set for priority queue
        self.redis_client.zadd(
            self.queue_name,
            {json.dumps(task_data): task.priority.value}
        )
    
    async def dequeue(self) -> Optional[TaskRequest]:
        """Get next task from the queue."""
        # Get highest priority task
        items = self.redis_client.zrevrange(self.queue_name, 0, 0, withscores=True)
        
        if not items:
            return None
        
        task_json, priority = items[0]
        task_data = json.loads(task_json)
        
        # Remove from queue
        self.redis_client.zrem(self.queue_name, task_json)
        
        return TaskRequest(
            id=task_data["id"],
            type=task_data["type"],
            payload=task_data["payload"],
            priority=TaskPriority(int(priority))
        )


# MockMistralClient removed - now using shared library's MistralProvider
