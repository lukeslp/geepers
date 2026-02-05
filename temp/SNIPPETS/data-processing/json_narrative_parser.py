"""
JSON Narrative Story Format Parser

Description: Parse and convert JSON-based interactive narrative formats (similar to
StoryBlocks, Twine, Ink) into runtime-ready data structures for game engines or
web-based interactive fiction.

Use Cases:
- Building interactive fiction engines (text adventures, visual novels)
- Converting story data from authoring tools to game format
- Implementing branching narrative systems with conditions and effects
- Creating story-driven game systems with RPG mechanics
- Parsing exported stories from tools like Twine, Articy Draft, or custom editors

Dependencies:
- json (stdlib)
- re (stdlib)
- typing (stdlib)

Notes:
- Supports conditional branching based on game state
- Handles state modifications (stats, inventory, flags)
- Uses regex for skill check extraction from choice text
- Can be extended for custom node types and effect systems
- Designed to be engine-agnostic (works with any game framework)

Related Snippets:
- data-processing/json_validation_patterns.py - JSON structure validation
- data-processing/pydantic_validation_patterns.py - Type-safe data models
- file-operations/config_file_loading.py - Loading game data from files

Source Attribution:
- Extracted from: /home/coolhand/projects/storyblocks-godot/scripts/import/story_importer.gd
- Pattern adapted from Godot GDScript to Python
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field


@dataclass
class StoryMetadata:
    """Story metadata and configuration"""
    title: str = "Untitled Story"
    author: str = "Unknown"
    version: str = "1.0"
    description: str = ""
    genre: str = ""
    estimated_play_time: str = ""
    key_features: List[str] = field(default_factory=list)


@dataclass
class GameState:
    """Game state tracking player progress"""
    stats: Dict[str, int] = field(default_factory=dict)
    inventory: List[str] = field(default_factory=list)
    flags: Dict[str, bool] = field(default_factory=dict)
    variables: Dict[str, Any] = field(default_factory=dict)
    relationships: Dict[str, int] = field(default_factory=dict)
    current_node: str = "start"


class NarrativeParser:
    """
    Parse JSON-based narrative story formats into runtime data structures.

    Supports:
    - Story nodes with text, choices, and branching
    - Conditional choices based on game state
    - State effects (modify stats, add/remove items, set flags)
    - Skill checks with difficulty ratings
    - Character dialogue and narration
    """

    def __init__(self):
        self.story_data: Dict[str, Any] = {}
        self.metadata: StoryMetadata = StoryMetadata()
        self.initial_state: GameState = GameState()
        self.nodes: Dict[str, Dict] = {}
        self.start_node: str = "start"

    def load_from_file(self, file_path: str) -> bool:
        """Load story from JSON file"""
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Story file not found: {file_path}")

        try:
            with path.open('r', encoding='utf-8') as f:
                self.story_data = json.load(f)

            self._parse_story()
            return True
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in story file: {e}")

    def load_from_dict(self, data: Dict) -> bool:
        """Load story from dictionary"""
        self.story_data = data
        self._parse_story()
        return True

    def _parse_story(self):
        """Parse story data into structured format"""
        # Extract metadata
        self.metadata = StoryMetadata(
            title=self.story_data.get("title", "Untitled Story"),
            author=self.story_data.get("author", "Unknown"),
            version=self.story_data.get("version", "1.0"),
            description=self.story_data.get("description", ""),
            genre=self.story_data.get("genre", ""),
            estimated_play_time=self.story_data.get("estimatedPlayTime", ""),
            key_features=self.story_data.get("metadata", {}).get("keyFeatures", [])
        )

        # Extract initial game state
        initial_state_data = self.story_data.get("initialState", {})
        self.initial_state = GameState(
            stats=initial_state_data.get("stats", {}),
            inventory=initial_state_data.get("inventory", []),
            flags=initial_state_data.get("flags", {}),
            variables=initial_state_data.get("variables", {}),
            relationships=initial_state_data.get("relationships", {})
        )

        # Extract start node
        self.start_node = self.story_data.get("startNode", "start")

        # Parse all nodes
        raw_nodes = self.story_data.get("nodes", {})
        for node_id, node_data in raw_nodes.items():
            self.nodes[node_id] = self._convert_node(node_id, node_data)

    def _convert_node(self, node_id: str, node_data: Dict) -> Dict:
        """Convert a story node to runtime format"""
        converted = {
            "id": node_id,
            "type": node_data.get("type", "story"),
            "title": node_data.get("title", ""),
            "text": node_data.get("text", ""),
            "speaker": self._determine_speaker(node_data),
            "choices": [],
            "effects": node_data.get("effects", []),
            "conditions": node_data.get("condition", None),
            "next": node_data.get("next", None)  # For auto-advancing nodes
        }

        # Convert choices
        choices = node_data.get("choices", [])
        for choice in choices:
            converted["choices"].append(self._convert_choice(choice))

        return converted

    def _convert_choice(self, choice: Dict) -> Dict:
        """Convert a story choice to runtime format"""
        return {
            "text": choice.get("text", "Continue"),
            "next": choice.get("next", ""),
            "condition": choice.get("condition", None),
            "effects": choice.get("effects", []),
            "skill_check": self._extract_skill_check(choice)
        }

    def _determine_speaker(self, node: Dict) -> str:
        """Determine the speaker for a node (character or narrator)"""
        title = node.get("title", "")
        text = node.get("text", "")

        # Check if it's narration (second person)
        if text.startswith("You ") or text.startswith("Your "):
            return "NARRATOR"

        # Use title as speaker if it looks like a character name
        if title and len(title) < 30:
            return title.upper()

        return "NARRATOR"

    def _extract_skill_check(self, choice: Dict) -> Optional[Dict]:
        """Extract skill check requirements from choice text or condition"""
        text = choice.get("text", "")
        condition = choice.get("condition", "")

        # Parse skill checks from text like "[Wisdom >= 50]"
        pattern = r'\[([A-Za-z]+)\s*>=?\s*(\d+)\]'
        match = re.search(pattern, text)

        if match:
            return {
                "skill": match.group(1).lower(),
                "difficulty": int(match.group(2))
            }

        # Parse from condition string like "stats.wisdom >= 50"
        if condition:
            pattern = r'stats\.([A-Za-z]+)\s*>=?\s*(\d+)'
            match = re.search(pattern, condition)
            if match:
                return {
                    "skill": match.group(1).lower(),
                    "difficulty": int(match.group(2))
                }

        return None

    def get_node(self, node_id: str) -> Optional[Dict]:
        """Get a specific story node"""
        return self.nodes.get(node_id)

    def get_start_node(self) -> Dict:
        """Get the starting story node"""
        return self.nodes.get(self.start_node, {})

    def get_all_nodes(self) -> Dict[str, Dict]:
        """Get all story nodes"""
        return self.nodes


class GameStateManager:
    """
    Manage game state and apply narrative effects.

    Handles:
    - State modification (stats, inventory, flags)
    - Condition evaluation
    - Skill checks with dice rolling
    """

    def __init__(self, initial_state: GameState):
        self.state = GameState(
            stats=initial_state.stats.copy(),
            inventory=initial_state.inventory.copy(),
            flags=initial_state.flags.copy(),
            variables=initial_state.variables.copy(),
            relationships=initial_state.relationships.copy()
        )

    def apply_effects(self, effects: List[Dict]):
        """Apply narrative effects to game state"""
        for effect in effects:
            effect_type = effect.get("type", "")

            if effect_type == "modifyState":
                self._modify_state(effect)
            elif effect_type == "setFlag":
                self._set_flag(effect)
            elif effect_type in ["addItem", "addInventory"]:
                self._add_item(effect)
            elif effect_type in ["removeItem", "removeInventory"]:
                self._remove_item(effect)

    def _modify_state(self, effect: Dict):
        """Modify a stat value"""
        variable = effect.get("variable", "")
        operation = effect.get("operation", "set")
        value = effect.get("value", 0)

        # Parse variable path like "stats.courage"
        parts = variable.split(".")
        if len(parts) != 2:
            return

        category, key = parts

        if category not in ["stats", "variables", "relationships"]:
            return

        # Get current value
        state_dict = getattr(self.state, category)
        current = state_dict.get(key, 0)

        # Apply operation
        if operation == "set":
            state_dict[key] = value
        elif operation == "add":
            state_dict[key] = current + value
        elif operation == "subtract":
            state_dict[key] = current - value
        elif operation == "multiply":
            state_dict[key] = current * value

    def _set_flag(self, effect: Dict):
        """Set a boolean flag"""
        flag = effect.get("flag", "")
        value = effect.get("value", True)
        self.state.flags[flag] = value

    def _add_item(self, effect: Dict):
        """Add item to inventory"""
        item = effect.get("item", "")
        if item and item not in self.state.inventory:
            self.state.inventory.append(item)

    def _remove_item(self, effect: Dict):
        """Remove item from inventory"""
        item = effect.get("item", "")
        if item in self.state.inventory:
            self.state.inventory.remove(item)

    def check_condition(self, condition: Optional[str]) -> bool:
        """Evaluate a condition string against game state"""
        if not condition:
            return True

        # Check stat conditions: stats.wisdom >= 50
        pattern = r'stats\.([A-Za-z]+)\s*([><=]+)\s*(\d+)'
        match = re.search(pattern, condition)
        if match:
            stat = match.group(1)
            operator = match.group(2)
            value = int(match.group(3))
            current = self.state.stats.get(stat, 0)
            return self._compare_values(current, operator, value)

        # Check flag conditions: flags.found_key
        pattern = r'flags\.([A-Za-z_]+)'
        match = re.search(pattern, condition)
        if match:
            flag = match.group(1)
            return self.state.flags.get(flag, False)

        # Check inventory conditions: inventory.has("sword")
        pattern = r'inventory\.has\(["\']([^"\']+)["\']\)'
        match = re.search(pattern, condition)
        if match:
            item = match.group(1)
            return item in self.state.inventory

        return True

    def _compare_values(self, a, operator: str, b) -> bool:
        """Compare two values with an operator"""
        if operator in [">=", "≥"]:
            return a >= b
        elif operator == ">":
            return a > b
        elif operator in ["<=", "≤"]:
            return a <= b
        elif operator == "<":
            return a < b
        elif operator in ["==", "="]:
            return a == b
        elif operator in ["!=", "≠"]:
            return a != b
        return False

    def perform_skill_check(self, skill: str, difficulty: int, dice_sides: int = 20) -> tuple[bool, int, int]:
        """
        Perform a skill check with dice rolling.

        Returns: (success, roll, total)
        """
        import random

        skill_value = self.state.stats.get(skill, 0)
        roll = random.randint(1, dice_sides)
        total = skill_value + roll
        success = total >= difficulty

        return success, roll, total


# Example usage
if __name__ == "__main__":
    # Example story data (simplified)
    story_data = {
        "title": "The Mysterious Forest",
        "author": "Demo Author",
        "startNode": "start",
        "initialState": {
            "stats": {"courage": 50, "wisdom": 50, "health": 100},
            "inventory": ["map", "compass"],
            "flags": {}
        },
        "nodes": {
            "start": {
                "type": "story",
                "title": "The Edge of the Forest",
                "text": "You stand at the edge of a mysterious forest...",
                "choices": [
                    {
                        "text": "Enter the forest [Courage >= 55]",
                        "next": "forest_path",
                        "condition": "stats.courage >= 55"
                    },
                    {
                        "text": "Study your map first",
                        "next": "study_map",
                        "effects": [
                            {"type": "modifyState", "variable": "stats.wisdom", "operation": "add", "value": 10}
                        ]
                    }
                ]
            },
            "forest_path": {
                "type": "story",
                "title": "Into the Woods",
                "text": "You venture into the dark forest...",
                "choices": []
            },
            "study_map": {
                "type": "story",
                "title": "Careful Preparation",
                "text": "You study your map carefully...",
                "next": "start"
            }
        }
    }

    # Parse the story
    parser = NarrativeParser()
    parser.load_from_dict(story_data)

    print(f"Story: {parser.metadata.title} by {parser.metadata.author}")
    print(f"Start node: {parser.start_node}")
    print(f"Total nodes: {len(parser.nodes)}")
    print(f"Initial stats: {parser.initial_state.stats}")
    print()

    # Create game state manager
    state_mgr = GameStateManager(parser.initial_state)

    # Get start node
    current_node = parser.get_start_node()
    print(f"Node: {current_node['title']}")
    print(f"Text: {current_node['text'][:50]}...")
    print(f"Choices:")

    for i, choice in enumerate(current_node['choices']):
        available = state_mgr.check_condition(choice.get('condition'))
        status = "✓" if available else "✗"
        print(f"  {status} {i+1}. {choice['text']}")

    # Simulate choosing option 2 (study map)
    print("\nChoosing option 2: Study map")
    choice = current_node['choices'][1]
    state_mgr.apply_effects(choice.get('effects', []))
    print(f"New wisdom: {state_mgr.state.stats['wisdom']}")
