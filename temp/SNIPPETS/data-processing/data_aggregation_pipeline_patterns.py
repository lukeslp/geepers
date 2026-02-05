"""
Data Aggregation and Pipeline Transformation Patterns

Description: Comprehensive patterns for building data processing pipelines including aggregation, grouping, filtering, and multi-stage transformations. Implements functional composition and chainable operations.

Use Cases:
- Building ETL (Extract, Transform, Load) pipelines
- Aggregating data from multiple sources
- Implementing map-reduce style processing
- Creating data analysis workflows
- Building streaming data processors
- Implementing data validation pipelines

Dependencies:
- typing (stdlib)
- functools (stdlib)
- collections (stdlib)
- itertools (stdlib)

Notes:
- All operations are composable and chainable
- Supports both eager and lazy evaluation
- Memory-efficient for large datasets using generators
- Type hints throughout for better IDE support
- Error handling with detailed context
- Functional programming patterns for clean composition

Related Snippets:
- data-processing/format_conversion_patterns.py - Format conversion
- data-processing/data_sanitization_patterns.py - Data cleaning
- data-processing/pydantic_validation_patterns.py - Validation

Source Attribution:
- Patterns inspired by functional programming concepts
- Aggregation patterns from /home/coolhand/projects/swarm data processing
- Pipeline concepts from various ETL implementations
"""

from typing import Any, Callable, Dict, Iterable, List, Optional, Set, Tuple, TypeVar, Union
from functools import reduce
from collections import defaultdict, Counter
from itertools import groupby
import operator


T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')


# ===== Aggregation Functions =====

def group_by(
    items: List[Dict[str, Any]],
    key: str,
    value_key: Optional[str] = None
) -> Dict[Any, List[Any]]:
    """
    Group items by a specific key.

    Args:
        items: List of dictionaries
        key: Key to group by
        value_key: If specified, only collect this value (else collect full items)

    Returns:
        Dictionary mapping key values to lists of items

    Example:
        >>> data = [
        ...     {"type": "fruit", "name": "apple"},
        ...     {"type": "fruit", "name": "banana"},
        ...     {"type": "vegetable", "name": "carrot"}
        ... ]
        >>> group_by(data, "type", "name")
        {'fruit': ['apple', 'banana'], 'vegetable': ['carrot']}
    """
    result = defaultdict(list)

    for item in items:
        group_key = item.get(key)
        if group_key is not None:
            value = item.get(value_key) if value_key else item
            result[group_key].append(value)

    return dict(result)


def count_by(items: List[Dict[str, Any]], key: str) -> Dict[Any, int]:
    """
    Count occurrences grouped by key.

    Args:
        items: List of dictionaries
        key: Key to count by

    Returns:
        Dictionary mapping values to counts

    Example:
        >>> data = [
        ...     {"status": "success"},
        ...     {"status": "success"},
        ...     {"status": "error"}
        ... ]
        >>> count_by(data, "status")
        {'success': 2, 'error': 1}
    """
    return dict(Counter(item.get(key) for item in items if key in item))


def aggregate_by(
    items: List[Dict[str, Any]],
    group_key: str,
    value_key: str,
    aggregation: str = 'sum'
) -> Dict[Any, float]:
    """
    Aggregate numeric values by group.

    Args:
        items: List of dictionaries
        group_key: Key to group by
        value_key: Key containing values to aggregate
        aggregation: Type of aggregation ('sum', 'avg', 'min', 'max', 'count')

    Returns:
        Dictionary mapping group keys to aggregated values

    Example:
        >>> data = [
        ...     {"category": "A", "value": 10},
        ...     {"category": "A", "value": 20},
        ...     {"category": "B", "value": 15}
        ... ]
        >>> aggregate_by(data, "category", "value", "sum")
        {'A': 30, 'B': 15}

        >>> aggregate_by(data, "category", "value", "avg")
        {'A': 15.0, 'B': 15.0}
    """
    groups = group_by(items, group_key, value_key)

    result = {}
    for key, values in groups.items():
        if aggregation == 'sum':
            result[key] = sum(values)
        elif aggregation == 'avg':
            result[key] = sum(values) / len(values) if values else 0
        elif aggregation == 'min':
            result[key] = min(values) if values else None
        elif aggregation == 'max':
            result[key] = max(values) if values else None
        elif aggregation == 'count':
            result[key] = len(values)
        else:
            raise ValueError(f"Unknown aggregation: {aggregation}")

    return result


def unique_values(items: List[Dict[str, Any]], key: str) -> List[Any]:
    """
    Get unique values for a specific key.

    Args:
        items: List of dictionaries
        key: Key to extract unique values from

    Returns:
        List of unique values (preserves order)

    Example:
        >>> data = [
        ...     {"tag": "python"},
        ...     {"tag": "ai"},
        ...     {"tag": "python"}
        ... ]
        >>> unique_values(data, "tag")
        ['python', 'ai']
    """
    seen = set()
    result = []

    for item in items:
        value = item.get(key)
        if value is not None and value not in seen:
            seen.add(value)
            result.append(value)

    return result


# ===== Pipeline Transformation =====

class DataPipeline:
    """
    Chainable data transformation pipeline.

    Supports method chaining for building complex transformations.

    Example:
        >>> data = [1, 2, 3, 4, 5]
        >>> result = (DataPipeline(data)
        ...     .map(lambda x: x * 2)
        ...     .filter(lambda x: x > 5)
        ...     .collect())
        >>> result
        [6, 8, 10]
    """

    def __init__(self, data: Iterable[T]):
        """Initialize with data source."""
        self.data = iter(data) if not isinstance(data, (list, tuple)) else iter(data)
        self._operations: List[Callable] = []

    def map(self, func: Callable[[T], Any]) -> 'DataPipeline':
        """
        Transform each item using function.

        Args:
            func: Transformation function

        Returns:
            Self for chaining
        """
        self._operations.append(lambda items: map(func, items))
        return self

    def filter(self, predicate: Callable[[T], bool]) -> 'DataPipeline':
        """
        Filter items based on predicate.

        Args:
            predicate: Function returning True for items to keep

        Returns:
            Self for chaining
        """
        self._operations.append(lambda items: filter(predicate, items))
        return self

    def flatmap(self, func: Callable[[T], Iterable]) -> 'DataPipeline':
        """
        Map and flatten results.

        Args:
            func: Function returning iterable

        Returns:
            Self for chaining
        """
        def _flatmap(items):
            for item in items:
                yield from func(item)

        self._operations.append(_flatmap)
        return self

    def distinct(self) -> 'DataPipeline':
        """
        Remove duplicates (preserves order).

        Returns:
            Self for chaining
        """
        def _distinct(items):
            seen = set()
            for item in items:
                if item not in seen:
                    seen.add(item)
                    yield item

        self._operations.append(_distinct)
        return self

    def sort(self, key: Optional[Callable] = None, reverse: bool = False) -> 'DataPipeline':
        """
        Sort items.

        Args:
            key: Key function for sorting
            reverse: Sort in descending order

        Returns:
            Self for chaining
        """
        self._operations.append(lambda items: sorted(items, key=key, reverse=reverse))
        return self

    def take(self, n: int) -> 'DataPipeline':
        """
        Take first n items.

        Args:
            n: Number of items to take

        Returns:
            Self for chaining
        """
        self._operations.append(lambda items: (x for i, x in enumerate(items) if i < n))
        return self

    def skip(self, n: int) -> 'DataPipeline':
        """
        Skip first n items.

        Args:
            n: Number of items to skip

        Returns:
            Self for chaining
        """
        self._operations.append(lambda items: (x for i, x in enumerate(items) if i >= n))
        return self

    def collect(self) -> List[Any]:
        """
        Execute pipeline and collect results.

        Returns:
            List of results
        """
        result = self.data
        for operation in self._operations:
            result = operation(result)
        return list(result)

    def reduce(self, func: Callable[[Any, T], Any], initial: Any = None) -> Any:
        """
        Reduce items to single value.

        Args:
            func: Reduction function
            initial: Initial value

        Returns:
            Reduced value
        """
        result = self.collect()
        if initial is None:
            return reduce(func, result)
        return reduce(func, result, initial)


# ===== Dictionary Pipeline =====

class DictPipeline:
    """
    Pipeline for transforming lists of dictionaries.

    Example:
        >>> data = [
        ...     {"name": "Alice", "age": 25, "dept": "eng"},
        ...     {"name": "Bob", "age": 30, "dept": "eng"},
        ...     {"name": "Charlie", "age": 35, "dept": "sales"}
        ... ]
        >>> result = (DictPipeline(data)
        ...     .filter_by("dept", "eng")
        ...     .select("name", "age")
        ...     .collect())
        >>> result
        [{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}]
    """

    def __init__(self, data: List[Dict[str, Any]]):
        """Initialize with list of dictionaries."""
        self.data = data

    def filter_by(self, key: str, value: Any) -> 'DictPipeline':
        """
        Filter dictionaries where key equals value.

        Args:
            key: Key to check
            value: Value to match

        Returns:
            Self for chaining
        """
        self.data = [item for item in self.data if item.get(key) == value]
        return self

    def filter_func(self, predicate: Callable[[Dict], bool]) -> 'DictPipeline':
        """
        Filter using custom predicate function.

        Args:
            predicate: Function returning True for items to keep

        Returns:
            Self for chaining
        """
        self.data = [item for item in self.data if predicate(item)]
        return self

    def select(self, *keys: str) -> 'DictPipeline':
        """
        Select only specified keys from dictionaries.

        Args:
            *keys: Keys to keep

        Returns:
            Self for chaining
        """
        self.data = [{k: item[k] for k in keys if k in item} for item in self.data]
        return self

    def exclude(self, *keys: str) -> 'DictPipeline':
        """
        Exclude specified keys from dictionaries.

        Args:
            *keys: Keys to remove

        Returns:
            Self for chaining
        """
        keys_set = set(keys)
        self.data = [{k: v for k, v in item.items() if k not in keys_set} for item in self.data]
        return self

    def rename(self, mapping: Dict[str, str]) -> 'DictPipeline':
        """
        Rename keys in dictionaries.

        Args:
            mapping: Dict mapping old names to new names

        Returns:
            Self for chaining
        """
        def rename_dict(d):
            return {mapping.get(k, k): v for k, v in d.items()}

        self.data = [rename_dict(item) for item in self.data]
        return self

    def add_column(self, key: str, func: Callable[[Dict], Any]) -> 'DictPipeline':
        """
        Add new column computed from existing data.

        Args:
            key: New column name
            func: Function to compute value

        Returns:
            Self for chaining
        """
        for item in self.data:
            item[key] = func(item)
        return self

    def sort_by(self, key: str, reverse: bool = False) -> 'DictPipeline':
        """
        Sort by dictionary key.

        Args:
            key: Key to sort by
            reverse: Sort descending

        Returns:
            Self for chaining
        """
        self.data = sorted(self.data, key=lambda x: x.get(key), reverse=reverse)
        return self

    def group_by(self, key: str) -> Dict[Any, List[Dict]]:
        """
        Group dictionaries by key value.

        Args:
            key: Key to group by

        Returns:
            Dictionary mapping values to lists of items
        """
        return group_by(self.data, key)

    def aggregate(self, group_key: str, value_key: str, aggregation: str = 'sum') -> Dict[Any, float]:
        """
        Aggregate values by group.

        Args:
            group_key: Key to group by
            value_key: Key containing values
            aggregation: Aggregation type

        Returns:
            Aggregated results
        """
        return aggregate_by(self.data, group_key, value_key, aggregation)

    def collect(self) -> List[Dict[str, Any]]:
        """
        Return current data.

        Returns:
            List of dictionaries
        """
        return self.data


# ===== Merge and Join Operations =====

def merge_dicts(*dicts: Dict[str, Any], strategy: str = 'last') -> Dict[str, Any]:
    """
    Merge multiple dictionaries.

    Args:
        *dicts: Dictionaries to merge
        strategy: Merge strategy ('last', 'first', 'combine')

    Returns:
        Merged dictionary

    Example:
        >>> d1 = {"a": 1, "b": 2}
        >>> d2 = {"b": 3, "c": 4}
        >>> merge_dicts(d1, d2)
        {'a': 1, 'b': 3, 'c': 4}
    """
    if strategy == 'last':
        result = {}
        for d in dicts:
            result.update(d)
        return result

    elif strategy == 'first':
        result = {}
        for d in dicts:
            for k, v in d.items():
                if k not in result:
                    result[k] = v
        return result

    elif strategy == 'combine':
        result = defaultdict(list)
        for d in dicts:
            for k, v in d.items():
                result[k].append(v)
        return dict(result)

    else:
        raise ValueError(f"Unknown strategy: {strategy}")


def left_join(
    left: List[Dict],
    right: List[Dict],
    left_key: str,
    right_key: str,
    prefix: str = "right_"
) -> List[Dict]:
    """
    Perform left join on two lists of dictionaries.

    Args:
        left: Left dataset
        right: Right dataset
        left_key: Key in left dataset
        right_key: Key in right dataset
        prefix: Prefix for right columns

    Returns:
        Joined dataset

    Example:
        >>> users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        >>> orders = [{"user_id": 1, "amount": 100}]
        >>> left_join(users, orders, "id", "user_id")
        [{'id': 1, 'name': 'Alice', 'right_user_id': 1, 'right_amount': 100},
         {'id': 2, 'name': 'Bob'}]
    """
    # Index right dataset
    right_index = group_by(right, right_key)

    result = []
    for left_item in left:
        key_value = left_item.get(left_key)
        merged = left_item.copy()

        if key_value in right_index:
            # Join with first matching right item
            right_item = right_index[key_value][0]
            for k, v in right_item.items():
                merged[f"{prefix}{k}"] = v

        result.append(merged)

    return result


# ===== Usage Examples =====

if __name__ == "__main__":
    print("=" * 70)
    print("Data Aggregation and Pipeline Patterns - Usage Examples")
    print("=" * 70)

    # Sample data
    sales_data = [
        {"product": "Laptop", "category": "Electronics", "price": 1000, "quantity": 2},
        {"product": "Phone", "category": "Electronics", "price": 500, "quantity": 5},
        {"product": "Desk", "category": "Furniture", "price": 300, "quantity": 3},
        {"product": "Chair", "category": "Furniture", "price": 100, "quantity": 10},
        {"product": "Monitor", "category": "Electronics", "price": 300, "quantity": 4},
    ]

    # 1. Basic Aggregation
    print("\n1. Group By Category:")
    print("-" * 70)
    grouped = group_by(sales_data, "category", "product")
    for category, products in grouped.items():
        print(f"{category}: {products}")

    # 2. Count By
    print("\n2. Count By Category:")
    print("-" * 70)
    counts = count_by(sales_data, "category")
    print(counts)

    # 3. Aggregate By
    print("\n3. Total Revenue By Category:")
    print("-" * 70)
    # First compute revenue
    for item in sales_data:
        item['revenue'] = item['price'] * item['quantity']

    revenue_by_category = aggregate_by(sales_data, "category", "revenue", "sum")
    for category, revenue in revenue_by_category.items():
        print(f"{category}: ${revenue}")

    # 4. Data Pipeline
    print("\n4. Data Pipeline - Numbers Example:")
    print("-" * 70)
    numbers = list(range(1, 11))
    result = (DataPipeline(numbers)
        .filter(lambda x: x % 2 == 0)
        .map(lambda x: x * x)
        .collect())
    print(f"Even numbers squared: {result}")

    # 5. Dictionary Pipeline
    print("\n5. Dictionary Pipeline - Filter and Select:")
    print("-" * 70)
    electronics = (DictPipeline(sales_data)
        .filter_by("category", "Electronics")
        .select("product", "price")
        .sort_by("price", reverse=True)
        .collect())
    print("Electronics sorted by price:")
    for item in electronics:
        print(f"  {item['product']}: ${item['price']}")

    # 6. Add Computed Column
    print("\n6. Add Computed Column:")
    print("-" * 70)
    with_discount = (DictPipeline(sales_data)
        .add_column("discount_price", lambda x: x['price'] * 0.9)
        .select("product", "price", "discount_price")
        .collect())
    print("Products with 10% discount:")
    for item in with_discount[:3]:
        print(f"  {item['product']}: ${item['price']} → ${item['discount_price']:.2f}")

    # 7. Chain Multiple Operations
    print("\n7. Complex Pipeline - High Value Electronics:")
    print("-" * 70)
    high_value = (DictPipeline(sales_data)
        .filter_by("category", "Electronics")
        .filter_func(lambda x: x['revenue'] > 1000)
        .sort_by("revenue", reverse=True)
        .select("product", "revenue")
        .collect())
    print("High-value electronics:")
    for item in high_value:
        print(f"  {item['product']}: ${item['revenue']}")

    # 8. Merge Dictionaries
    print("\n8. Merge Dictionaries:")
    print("-" * 70)
    d1 = {"a": 1, "b": 2}
    d2 = {"b": 3, "c": 4}
    d3 = {"c": 5, "d": 6}
    merged = merge_dicts(d1, d2, d3, strategy='last')
    print(f"Merged (last wins): {merged}")

    # 9. Left Join
    print("\n9. Left Join Example:")
    print("-" * 70)
    users = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},
        {"id": 3, "name": "Charlie"}
    ]
    orders = [
        {"user_id": 1, "amount": 100},
        {"user_id": 1, "amount": 200},
        {"user_id": 2, "amount": 150}
    ]
    joined = left_join(users, orders, "id", "user_id", prefix="order_")
    print("Users with orders:")
    for item in joined:
        print(f"  {item}")

    # 10. Reduce Example
    print("\n10. Reduce to Sum Total Revenue:")
    print("-" * 70)
    total_revenue = (DataPipeline(sales_data)
        .map(lambda x: x['revenue'])
        .reduce(operator.add))
    print(f"Total revenue: ${total_revenue}")

    print("\n" + "=" * 70)
    print("Examples complete!")
    print("=" * 70)
