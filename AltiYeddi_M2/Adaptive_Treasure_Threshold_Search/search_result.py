from dataclasses import dataclass, field


@dataclass
class SearchResult:
    algorithm_name: str
    path: list = field(default_factory=list)
    search_order: list = field(default_factory=list)
    nodes_expanded: int = 0
    path_cost: int = 0
    success: bool = False
    message: str = ""
    runtime_seconds: float = 0.0
