from abc import ABC, abstractmethod
from typing import List, Dict, Any

class DatabaseInterface(ABC):
    @abstractmethod
    def get_commits(self, author: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        pass
