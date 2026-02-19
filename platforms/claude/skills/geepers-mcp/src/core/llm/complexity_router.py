"""
Intelligent Model Complexity Router with Cost Optimization

Analyzes queries and routes them to appropriate models based on complexity.
Extracted from Coze impossibleLlama, Chat Hopper, and cheapHopper patterns.

Author: Luke Steuber
"""

from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum


class Complexity(str, Enum):
    """Query complexity levels"""
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"


class BudgetTier(str, Enum):
    """Budget optimization tiers"""
    CHEAP = "cheap"
    BALANCED = "balanced"
    PREMIUM = "premium"


@dataclass
class RoutingDecision:
    """Model routing decision with metadata"""
    provider: str
    model: str
    complexity: Complexity
    budget_tier: BudgetTier
    estimated_cost_multiplier: float  # Relative to cheapest option
    reason: str
    fallback_provider: Optional[str] = None
    fallback_model: Optional[str] = None


class ComplexityRouter:
    """
    Intelligent model selection based on query complexity and budget constraints.
    
    Features:
    - Multi-factor complexity detection (keywords, length, code, structure)
    - Budget-aware model selection
    - Provider fallback strategies
    - Cost tracking and estimation
    - Transparent decision explanations
    """

    # Complexity indicators (from Coze patterns)
    SIMPLE_INDICATORS = [
        'what is', 'define', 'basic', 'simple', 'quick',
        'tell me', 'list', 'name', 'who is', 'when',
        'how many', 'where', 'yes or no'
    ]

    MEDIUM_INDICATORS = [
        'explain', 'compare', 'analyze', 'how does',
        'why', 'describe', 'summarize', 'review',
        'what are the differences', 'pros and cons'
    ]

    COMPLEX_INDICATORS = [
        'optimize', 'architect', 'design', 'comprehensive',
        'research', 'analyze thoroughly', 'detailed analysis',
        'compare and contrast', 'evaluate', 'implement',
        'create system', 'build', 'develop', 'refactor',
        'design pattern', 'architecture', 'performance tuning'
    ]

    # Relative cost multipliers (simple=1.0 baseline)
    COST_MULTIPLIERS = {
        'openai': {'simple': 1.0, 'medium': 40.0, 'complex': 40.0},  # gpt-4o-mini vs gpt-4o
        'anthropic': {'simple': 1.0, 'medium': 12.5, 'complex': 12.5},  # haiku vs sonnet
        'xai': {'simple': 1.0, 'medium': 1.0, 'complex': 1.0},  # Same model
        'groq': {'simple': 1.0, 'medium': 8.0, 'complex': 8.0},  # 8b vs 70b
        'mistral': {'simple': 1.0, 'medium': 5.0, 'complex': 10.0},  # small vs medium vs large
        'cohere': {'simple': 1.0, 'medium': 2.0, 'complex': 5.0},  # command-light vs command vs r-plus
        'gemini': {'simple': 1.0, 'medium': 3.0, 'complex': 3.0},  # flash vs pro
    }

    def __init__(self, default_provider: str = 'openai', default_budget: BudgetTier = BudgetTier.BALANCED):
        """
        Initialize the complexity router.

        Args:
            default_provider: Default provider to use
            default_budget: Default budget tier
        """
        self.default_provider = default_provider
        self.default_budget = default_budget
        self.routing_history: List[RoutingDecision] = []

    def route(
        self,
        query: str,
        provider: Optional[str] = None,
        budget_tier: Optional[BudgetTier] = None,
        require_capability: Optional[str] = None
    ) -> RoutingDecision:
        """
        Route query to optimal model.

        Args:
            query: User query or task
            provider: Specific provider (or None for auto-select)
            budget_tier: Budget constraint
            require_capability: Required capability (vision, image_generation, etc.)

        Returns:
            RoutingDecision with model selection and metadata
        """
        provider = provider or self.default_provider
        budget_tier = budget_tier or self.default_budget

        # Detect complexity
        complexity = self._detect_complexity(query)

        # Adjust for budget
        adjusted_complexity = self._adjust_for_budget(complexity, budget_tier)

        # Get model from factory
        from .factory import COMPLEXITY_TIERS, ProviderFactory

        if provider not in COMPLEXITY_TIERS:
            raise ValueError(f"Provider {provider} not supported in complexity routing")

        model = COMPLEXITY_TIERS[provider][adjusted_complexity]

        # Calculate cost multiplier
        cost_mult = self.COST_MULTIPLIERS.get(provider, {}).get(adjusted_complexity, 1.0)

        # Check capability if required
        if require_capability:
            caps = ProviderFactory.get_provider_capabilities(provider)
            if not caps.get(require_capability):
                # Find fallback provider with capability
                fallback_providers = ProviderFactory.find_providers_with_capability(require_capability)
                if fallback_providers:
                    fallback_provider = fallback_providers[0]
                    fallback_model = COMPLEXITY_TIERS[fallback_provider][adjusted_complexity]
                else:
                    raise ValueError(f"No providers support capability: {require_capability}")
            else:
                fallback_provider = None
                fallback_model = None
        else:
            fallback_provider = None
            fallback_model = None

        # Generate reason
        reason = self._generate_reason(complexity, adjusted_complexity, budget_tier, query)

        decision = RoutingDecision(
            provider=provider,
            model=model,
            complexity=complexity,
            budget_tier=budget_tier,
            estimated_cost_multiplier=cost_mult,
            reason=reason,
            fallback_provider=fallback_provider,
            fallback_model=fallback_model
        )

        # Track decision
        self.routing_history.append(decision)

        return decision

    def _detect_complexity(self, query: str) -> Complexity:
        """
        Detect query complexity using multi-factor analysis.

        Factors:
        1. Keyword indicators
        2. Query length
        3. Code presence
        4. Structural complexity
        5. Question depth
        """
        query_lower = query.lower()
        word_count = len(query.split())

        # Factor 1: Keywords
        simple_score = sum(1 for kw in self.SIMPLE_INDICATORS if kw in query_lower)
        medium_score = sum(1 for kw in self.MEDIUM_INDICATORS if kw in query_lower)
        complex_score = sum(1 for kw in self.COMPLEX_INDICATORS if kw in query_lower)

        # Factor 2: Length
        if word_count < 10:
            length_score = Complexity.SIMPLE
        elif word_count < 30:
            length_score = Complexity.MEDIUM
        else:
            length_score = Complexity.COMPLEX

        # Factor 3: Code presence
        has_code = any(marker in query for marker in ['```', 'def ', 'class ', 'function ', 'import '])
        
        # Factor 4: Structural complexity
        has_nested_questions = query.count('?') > 1
        has_multiple_tasks = any(word in query_lower for word in ['and ', 'then ', 'also ', 'additionally'])

        # Decision logic
        if complex_score > 0 or (has_code and word_count > 20) or has_nested_questions:
            return Complexity.COMPLEX

        if medium_score > simple_score or (word_count > 20 and not has_code):
            return Complexity.MEDIUM

        if simple_score > 0 and word_count < 15:
            return Complexity.SIMPLE

        # Default based on length
        return length_score

    def _adjust_for_budget(self, complexity: Complexity, budget_tier: BudgetTier) -> str:
        """
        Adjust complexity level based on budget constraints.

        Budget tiers:
        - CHEAP: Downgrade medium to simple
        - BALANCED: No change
        - PREMIUM: Upgrade simple to medium
        """
        if budget_tier == BudgetTier.CHEAP:
            if complexity == Complexity.COMPLEX:
                return Complexity.MEDIUM.value
            elif complexity == Complexity.MEDIUM:
                return Complexity.SIMPLE.value
            return complexity.value

        elif budget_tier == BudgetTier.PREMIUM:
            if complexity == Complexity.SIMPLE:
                return Complexity.MEDIUM.value
            return complexity.value

        return complexity.value

    def _generate_reason(
        self,
        detected_complexity: Complexity,
        adjusted_complexity: str,
        budget_tier: BudgetTier,
        query: str
    ) -> str:
        """Generate human-readable reason for routing decision"""
        word_count = len(query.split())
        
        reason_parts = [f"Detected {detected_complexity.value} complexity query"]
        
        if detected_complexity.value != adjusted_complexity:
            reason_parts.append(f"adjusted to {adjusted_complexity} for {budget_tier.value} budget")
        
        reason_parts.append(f"({word_count} words)")
        
        return "; ".join(reason_parts)

    def get_cost_savings(self, compared_to_provider: str = 'openai') -> Dict[str, Any]:
        """
        Calculate estimated cost savings from intelligent routing.

        Args:
            compared_to_provider: Provider to compare against (using their 'complex' tier)

        Returns:
            Dict with savings statistics
        """
        if not self.routing_history:
            return {'error': 'No routing history available'}

        # Calculate what it would have cost with always-complex tier
        baseline_multiplier = self.COST_MULTIPLIERS[compared_to_provider]['complex']
        total_baseline_cost = len(self.routing_history) * baseline_multiplier

        # Calculate actual cost
        total_actual_cost = sum(
            decision.estimated_cost_multiplier
            for decision in self.routing_history
        )

        savings_percent = ((total_baseline_cost - total_actual_cost) / total_baseline_cost) * 100

        return {
            'total_queries': len(self.routing_history),
            'baseline_cost_units': total_baseline_cost,
            'actual_cost_units': total_actual_cost,
            'savings_percent': round(savings_percent, 1),
            'simple_queries': sum(1 for d in self.routing_history if d.complexity == Complexity.SIMPLE),
            'medium_queries': sum(1 for d in self.routing_history if d.complexity == Complexity.MEDIUM),
            'complex_queries': sum(1 for d in self.routing_history if d.complexity == Complexity.COMPLEX),
        }

    def explain_last_decision(self) -> str:
        """Get detailed explanation of last routing decision"""
        if not self.routing_history:
            return "No routing decisions yet"

        decision = self.routing_history[-1]
        
        explanation = f"""
Routing Decision:
  Provider: {decision.provider}
  Model: {decision.model}
  Complexity: {decision.complexity.value}
  Budget Tier: {decision.budget_tier.value}
  Cost Multiplier: {decision.estimated_cost_multiplier}x
  Reason: {decision.reason}
"""
        
        if decision.fallback_provider:
            explanation += f"  Fallback: {decision.fallback_provider} / {decision.fallback_model}\n"
        
        return explanation
