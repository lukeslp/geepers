import asyncio
import time
import uuid
import logging
from typing import Dict, List, Optional, Any, Callable
from .hierarchical_agent_coordination import HierarchicalOrchestrator, OrchestratorConfig, BelterAgent, DrummerAgent, CaminaAgent, AgentTask, AgentResponse, TaskStatus
from ..llm.factory import ProviderFactory

logger = logging.getLogger(__name__)

class RealLLMBelterAgent(BelterAgent):
    """Belter agent that actually calls an LLM."""
    
    def __init__(self, agent_id: str, provider_name: str, model: Optional[str] = None, specialization: Optional[str] = None, **config):
        super().__init__(agent_id, specialization=specialization, **config)
        self.provider_name = provider_name
        self.model = model
        self.provider = ProviderFactory.get_provider(provider_name)

    async def execute_task(self, task: AgentTask) -> AgentResponse:
        self.current_task = task
        self.status = TaskStatus.RUNNING
        start_time = time.time()
        
        try:
            # Use specialization in prompt if provided
            system_prompt = f"You are a specialized research agent called a 'Belter'. Your specialization is {self.specialization}."
            user_prompt = f"Research task: {task.prompt}\n\nContext: {task.context}"
            
            # Select model if not specified
            model_to_use = self.model
            if not model_to_use:
                model_to_use, _ = ProviderFactory.select_model_by_complexity(task.prompt, self.provider_name)
            
            # Call LLM (assuming provider has a chat method)
            # Note: In a real implementation, we'd handle streaming here if requested
            response_content = await self.provider.chat(prompt=user_prompt, system_prompt=system_prompt, model=model_to_use)
            
            execution_time = time.time() - start_time
            self.status = TaskStatus.COMPLETED
            
            return self._create_response(
                task=task,
                content=response_content,
                status=TaskStatus.COMPLETED,
                execution_time_seconds=execution_time,
                metadata={"specialization": self.specialization, "model": model_to_use}
            )
        except Exception as e:
            logger.error(f"Belter {self.agent_id} failed: {e}")
            execution_time = time.time() - start_time
            self.status = TaskStatus.FAILED
            return self._create_response(task=task, content="", status=TaskStatus.FAILED, execution_time_seconds=execution_time, error_message=str(e))
        finally:
            self.current_task = None

class RealLLMDrummerAgent(DrummerAgent):
    """Drummer agent that actually calls an LLM to synthesize."""
    
    def __init__(self, agent_id: str, provider_name: str, model: Optional[str] = None, **config):
        super().__init__(agent_id, **config)
        self.provider_name = provider_name
        self.model = model
        self.provider = ProviderFactory.get_provider(provider_name)

    async def execute_task(self, task: AgentTask) -> AgentResponse:
        self.current_task = task
        self.status = TaskStatus.RUNNING
        start_time = time.time()
        
        try:
            belter_responses = task.context.get('belter_responses', [])
            responses_text = "\n\n---\n\n".join([f"Belter {r.agent_id} ({r.metadata.get('specialization')}):\n{r.content}" for r in belter_responses if r.status == TaskStatus.COMPLETED])
            
            system_prompt = "You are a synthesis agent called a 'Drummer'. Your job is to aggregate findings from 5 research 'Belters' into a coherent report."
            user_prompt = f"Original Query: {task.prompt}\n\nBelter Findings:\n{responses_text}\n\nPlease synthesize these findings into a detailed summary."
            
            model_to_use = self.model or ProviderFactory.select_model_by_complexity(user_prompt, self.provider_name)[0]
            
            response_content = await self.provider.chat(prompt=user_prompt, system_prompt=system_prompt, model=model_to_use)
            
            execution_time = time.time() - start_time
            self.status = TaskStatus.COMPLETED
            
            return self._create_response(task=task, content=response_content, status=TaskStatus.COMPLETED, execution_time_seconds=execution_time)
        except Exception as e:
            logger.error(f"Drummer {self.agent_id} failed: {e}")
            return self._create_response(task=task, content="", status=TaskStatus.FAILED, execution_time_seconds=time.time()-start_time, error_message=str(e))
        finally:
            self.current_task = None

class RealLLMCaminaAgent(CaminaAgent):
    """Camina agent that actually calls an LLM for executive synthesis."""
    
    def __init__(self, agent_id: str, provider_name: str, model: Optional[str] = None, **config):
        super().__init__(agent_id, **config)
        self.provider_name = provider_name
        self.model = model
        self.provider = ProviderFactory.get_provider(provider_name)

    async def execute_task(self, task: AgentTask) -> AgentResponse:
        self.current_task = task
        self.status = TaskStatus.RUNNING
        start_time = time.time()
        
        try:
            drummer_responses = task.context.get('drummer_responses', [])
            responses_text = "\n\n===\n\n".join([f"Drummer {r.agent_id} Synthesis:\n{r.content}" for r in drummer_responses if r.status == TaskStatus.COMPLETED])
            
            system_prompt = "You are an executive synthesis agent called 'Camina'. Your job is to provide the final high-level executive report based on Drummer syntheses."
            user_prompt = f"Original Query: {task.prompt}\n\nDrummer Syntheses:\n{responses_text}\n\nPlease create the final executive summary and key findings."
            
            model_to_use = self.model or ProviderFactory.select_model_by_complexity(user_prompt, self.provider_name)[0]
            
            response_content = await self.provider.chat(prompt=user_prompt, system_prompt=system_prompt, model=model_to_use)
            
            execution_time = time.time() - start_time
            self.status = TaskStatus.COMPLETED
            
            return self._create_response(task=task, content=response_content, status=TaskStatus.COMPLETED, execution_time_seconds=execution_time)
        except Exception as e:
            logger.error(f"Camina {self.agent_id} failed: {e}")
            return self._create_response(task=task, content="", status=TaskStatus.FAILED, execution_time_seconds=time.time()-start_time, error_message=str(e))
        finally:
            self.current_task = None

class DreamCascadeOrchestrator(HierarchicalOrchestrator):
    """Orchestrator that uses Real LLM Agents."""
    
    def __init__(self, provider_name: str, model: Optional[str] = None, config: Optional[OrchestratorConfig] = None):
        super().__init__(config)
        self.provider_name = provider_name
        self.model = model

    async def _create_agent_swarm(self, num_subtasks: int) -> Dict[str, Any]:
        agents = {'belters': [], 'drummers': [], 'camina': None}
        specializations = ['research', 'analysis', 'technical', 'strategic', 'general']
        
        for i in range(num_subtasks):
            agent = RealLLMBelterAgent(f"belter_{i+1}", self.provider_name, self.model, specialization=specializations[i % len(specializations)])
            agents['belters'].append(agent)
            
        if self.config.enable_drummer:
            num_drummers = (num_subtasks + 4) // 5
            for i in range(num_drummers):
                agent = RealLLMDrummerAgent(f"drummer_{i+1}", self.provider_name, self.model)
                agents['drummers'].append(agent)
                
        if self.config.enable_camina and len(agents['drummers']) >= 2:
            agents['camina'] = RealLLMCaminaAgent("camina_1", self.provider_name, self.model)
            
        return agents
