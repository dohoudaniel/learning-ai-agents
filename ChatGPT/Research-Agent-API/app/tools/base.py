# app/tools/base.py
from abc import ABC, abstractmethod

class Tool(ABC):
    name: str
    description: str

    @abstractmethod
    def execute(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def schema(self):
        raise NotImplementedError