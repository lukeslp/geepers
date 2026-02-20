"""
Task Decomposition Pattern for Multi-Agent Systems

Description: Pattern for breaking down complex tasks into specific, actionable subtasks
that can be executed independently by specialized agents. Uses LLM-based decomposition
with intelligent padding and validation to ensure optimal agent utilization.

Use Cases:
- Breaking complex research questions into focused sub-questions
- Decomposing software projects into implementable features
- Splitting analysis tasks across specialized domains
- Converting high-level goals into actionable work items
- Distributing work across heterogeneous agent swarms

Dependencies:
- typing (for type hints)
- dataclasses (for data structures)
- datetime (for timestamping)
- re (for parsing numbered lists)

Notes:
- Generates 3-15 subtasks based on complexity
- Automatically pads to match available agent count
- Validates subtask quality and specificity
- Supports context injection for domain-specific decomposition
- Can use template-based fallback if LLM decomposition fails
- Tracks decomposition metadata for debugging

Related Snippets:
- hierarchical_agent_coordination.py - Full orchestration system
- parallel_agent_execution.py - Parallel subtask execution
- task_routing_and_delegation.py - Assigning subtasks to agents

Source Attribution:
- Extracted from: /home/coolhand/projects/beltalowda/src/beltalowda/orchestrator.py
- Method: _decompose_task() (lines 318-412), _parse_numbered_list() (lines 414-434)
- Original author: Luke Steuber
- Project: Beltalowda Multi-Agent Orchestration Platform
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import re


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class TaskDecomposition:
    """Result of task decomposition into subtasks"""
    original_task: str
    subtasks: List[str]
    decomposition_metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class DecompositionConfig:
    """Configuration for task decomposition"""
    min_subtasks: int = 3
    max_subtasks: int = 15
    target_agent_count: Optional[int] = None
    temperature: float = 0.5
    enable_padding: bool = True
    enable_validation: bool = True


# ============================================================================
# TASK DECOMPOSER
# ============================================================================

class TaskDecomposer:
    """
    Decomposes complex tasks into actionable subtasks.

    Uses either LLM-based decomposition or template-based fallback to
    break down tasks while ensuring optimal distribution across agents.
    """

    def __init__(self, config: Optional[DecompositionConfig] = None):
        """Initialize decomposer with configuration"""
        self.config = config or DecompositionConfig()

    async def decompose_task(
        self,
        task: str,
        context: Optional[Dict[str, Any]] = None,
        llm_provider: Optional[Any] = None
    ) -> TaskDecomposition:
        """
        Decompose main task into subtasks.

        Args:
            task: The main task description
            context: Optional additional context for decomposition
            llm_provider: Optional LLM provider for intelligent decomposition

        Returns:
            TaskDecomposition with subtasks and metadata
        """
        # Attempt LLM-based decomposition if provider available
        if llm_provider:
            subtasks = await self._llm_decompose(task, context, llm_provider)
        else:
            # Fallback to template-based decomposition
            subtasks = self._template_decompose(task)

        # Validate subtasks
        if self.config.enable_validation:
            subtasks = self._validate_subtasks(subtasks, task)

        # Pad to target agent count if needed
        if self.config.enable_padding and self.config.target_agent_count:
            subtasks = self._pad_to_target_count(subtasks, task)

        return TaskDecomposition(
            original_task=task,
            subtasks=subtasks,
            decomposition_metadata={
                "method": "llm" if llm_provider else "template",
                "original_count": len(subtasks),
                "padded": self.config.enable_padding and len(subtasks) != len(self._validate_subtasks([], task)),
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    async def _llm_decompose(
        self,
        task: str,
        context: Optional[Dict[str, Any]],
        llm_provider: Any
    ) -> List[str]:
        """Decompose task using LLM"""
        system_prompt = """You are a task decomposition specialist. Break down complex tasks into
specific, actionable subtasks that can be executed independently.

Rules:
1. Create between 3-15 subtasks based on complexity
2. Each subtask should be self-contained and specific
3. Subtasks should cover all aspects of the main task
4. Output ONLY a numbered list of subtasks
5. No explanations or additional text

Example format:
1. Research current market trends for the specified industry
2. Analyze competitor strategies and positioning
3. Identify key customer segments and needs
..."""

        # Build prompt with context
        prompt_parts = [f"Break down this task into subtasks:\n\n{task}"]

        if context:
            context_str = "\n".join(f"- {k}: {v}" for k, v in context.items())
            prompt_parts.append(f"\nAdditional context:\n{context_str}")

        prompt = "\n".join(prompt_parts)

        # Call LLM (placeholder - adapt to your LLM provider)
        try:
            # This would be replaced with actual LLM call
            response = await llm_provider.generate(
                system_prompt=system_prompt,
                user_prompt=prompt,
                temperature=self.config.temperature,
                max_tokens=1000
            )

            # Parse numbered list from response
            subtasks = self._parse_numbered_list(response)

            # Ensure minimum subtasks
            if len(subtasks) < self.config.min_subtasks:
                subtasks.extend(self._get_generic_subtasks(task, self.config.min_subtasks - len(subtasks)))

            return subtasks[:self.config.max_subtasks]

        except Exception as e:
            print(f"LLM decomposition failed: {e}, falling back to template")
            return self._template_decompose(task)

    def _template_decompose(self, task: str) -> List[str]:
        """Template-based decomposition fallback"""
        templates = [
            f"Research and gather relevant information about: {task}",
            f"Analyze key aspects and factors related to: {task}",
            f"Identify challenges and opportunities for: {task}",
            f"Evaluate different approaches and strategies for: {task}",
            f"Synthesize findings and formulate recommendations for: {task}"
        ]

        return templates[:self.config.min_subtasks]

    def _parse_numbered_list(self, text: str) -> List[str]:
        """
        Parse numbered list from text.

        Supports multiple formats:
        - "1. Item"
        - "1) Item"
        - "- Item"
        - "• Item"
        """
        lines = text.strip().split('\n')
        items = []

        for line in lines:
            line = line.strip()
            # Match patterns like "1.", "1)", "- ", "• "
            if line and (
                (line[0].isdigit() and ('.' in line or ')' in line)) or
                line.startswith(('- ', '• ', '* '))
            ):
                # Extract content after marker
                if line[0].isdigit():
                    parts = line.split('.', 1) if '.' in line else line.split(')', 1)
                    if len(parts) > 1:
                        items.append(parts[1].strip())
                else:
                    items.append(line[2:].strip())

        return items

    def _validate_subtasks(self, subtasks: List[str], original_task: str) -> List[str]:
        """Validate and filter subtasks"""
        validated = []

        for subtask in subtasks:
            # Remove empty or too short subtasks
            if len(subtask.strip()) < 10:
                continue

            # Remove duplicates
            if subtask in validated:
                continue

            validated.append(subtask)

        return validated

    def _pad_to_target_count(self, subtasks: List[str], task: str) -> List[str]:
        """Pad subtasks to match target agent count"""
        target = self.config.target_agent_count

        if not target or len(subtasks) >= target:
            return subtasks[:target] if target else subtasks

        # Need to add more subtasks
        additional_needed = target - len(subtasks)
        generic_subtasks = self._get_generic_subtasks(task, additional_needed)

        return subtasks + generic_subtasks

    def _get_generic_subtasks(self, task: str, count: int) -> List[str]:
        """Generate generic subtasks for padding"""
        templates = [
            f"Conduct supplementary research on: {task}",
            f"Perform detailed analysis of: {task}",
            f"Investigate related aspects of: {task}",
            f"Gather additional perspectives on: {task}",
            f"Examine supporting evidence for: {task}",
            f"Research secondary sources about: {task}",
            f"Analyze contextual factors of: {task}",
            f"Study comparative examples of: {task}",
            f"Evaluate different approaches to: {task}",
            f"Explore implications and consequences of: {task}",
            f"Review best practices related to: {task}",
            f"Investigate potential challenges with: {task}",
            f"Research implementation strategies for: {task}",
            f"Analyze stakeholder perspectives on: {task}",
            f"Study market/industry context of: {task}"
        ]

        # Cycle through templates if we need more than available
        result = []
        for i in range(count):
            template = templates[i % len(templates)]
            result.append(template)

        return result


# ============================================================================
# INTELLIGENT DECOMPOSER WITH DOMAIN SPECIALIZATION
# ============================================================================

class DomainSpecializedDecomposer(TaskDecomposer):
    """
    Enhanced decomposer with domain-specific strategies.

    Recognizes task domains and applies specialized decomposition patterns
    for research, software development, analysis, etc.
    """

    def __init__(self, config: Optional[DecompositionConfig] = None):
        """Initialize domain-specialized decomposer"""
        super().__init__(config)
        self.domain_patterns = self._initialize_domain_patterns()

    def _initialize_domain_patterns(self) -> Dict[str, List[str]]:
        """Define domain-specific decomposition patterns"""
        return {
            "research": [
                "Define research questions and objectives",
                "Conduct literature review and background research",
                "Identify primary and secondary data sources",
                "Analyze and synthesize research findings",
                "Formulate conclusions and recommendations"
            ],
            "software": [
                "Define requirements and specifications",
                "Design system architecture and components",
                "Implement core functionality",
                "Write tests and documentation",
                "Perform integration and deployment"
            ],
            "analysis": [
                "Define analysis scope and objectives",
                "Gather and prepare relevant data",
                "Apply analytical methods and techniques",
                "Interpret results and identify patterns",
                "Present findings and recommendations"
            ],
            "planning": [
                "Define goals and success criteria",
                "Identify resources and constraints",
                "Develop action plan and timeline",
                "Identify risks and mitigation strategies",
                "Define monitoring and evaluation approach"
            ]
        }

    def _detect_domain(self, task: str) -> Optional[str]:
        """Detect task domain based on keywords"""
        task_lower = task.lower()

        domain_keywords = {
            "research": ["research", "investigate", "study", "analyze", "explore"],
            "software": ["develop", "implement", "code", "build", "software", "app"],
            "analysis": ["analyze", "evaluate", "assess", "examine", "compare"],
            "planning": ["plan", "strategy", "roadmap", "organize", "design"]
        }

        for domain, keywords in domain_keywords.items():
            if any(keyword in task_lower for keyword in keywords):
                return domain

        return None

    def _template_decompose(self, task: str) -> List[str]:
        """Domain-aware template decomposition"""
        domain = self._detect_domain(task)

        if domain and domain in self.domain_patterns:
            # Use domain-specific pattern
            base_pattern = self.domain_patterns[domain]
            # Adapt pattern to specific task
            return [step.replace("the task", task) for step in base_pattern]
        else:
            # Fall back to generic decomposition
            return super()._template_decompose(task)


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    import asyncio

    async def example_basic():
        """Basic task decomposition"""
        print("Example 1: Basic Task Decomposition")
        print("=" * 60)

        config = DecompositionConfig(
            min_subtasks=3,
            max_subtasks=10,
            target_agent_count=5
        )

        decomposer = TaskDecomposer(config)

        task = "Analyze the impact of artificial intelligence on healthcare"
        result = await decomposer.decompose_task(task)

        print(f"Original Task: {result.original_task}")
        print(f"\nSubtasks ({len(result.subtasks)}):")
        for i, subtask in enumerate(result.subtasks, 1):
            print(f"  {i}. {subtask}")

        print(f"\nMetadata: {result.decomposition_metadata}")

    async def example_domain_specialized():
        """Domain-specialized decomposition"""
        print("\n\nExample 2: Domain-Specialized Decomposition")
        print("=" * 60)

        config = DecompositionConfig(
            min_subtasks=5,
            max_subtasks=10
        )

        decomposer = DomainSpecializedDecomposer(config)

        tasks = [
            "Research the effects of climate change on agriculture",
            "Develop a mobile app for task management",
            "Analyze market trends in renewable energy",
            "Plan a marketing campaign for a new product"
        ]

        for task in tasks:
            result = await decomposer.decompose_task(task)
            print(f"\nTask: {task}")
            print(f"Domain: {decomposer._detect_domain(task) or 'generic'}")
            print(f"Subtasks:")
            for i, subtask in enumerate(result.subtasks, 1):
                print(f"  {i}. {subtask}")

    async def example_with_padding():
        """Decomposition with agent count padding"""
        print("\n\nExample 3: Padding to Agent Count")
        print("=" * 60)

        # Decompose for different agent counts
        task = "Create a comprehensive business plan"

        for agent_count in [5, 10, 15]:
            config = DecompositionConfig(
                min_subtasks=3,
                max_subtasks=20,
                target_agent_count=agent_count,
                enable_padding=True
            )

            decomposer = TaskDecomposer(config)
            result = await decomposer.decompose_task(task)

            print(f"\nAgent Count: {agent_count}")
            print(f"Subtasks Generated: {len(result.subtasks)}")
            print(f"Padded: {result.decomposition_metadata.get('padded', False)}")

    # Run examples
    async def main():
        await example_basic()
        await example_domain_specialized()
        await example_with_padding()

    asyncio.run(main())
