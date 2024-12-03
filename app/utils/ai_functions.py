from typing import Callable, Type, Any, List, Dict
from pydantic import BaseModel


class AIFunctions:
    _registry: List[Dict[str, Any]] = []

    @classmethod
    def register(cls, func_name: str, input_model: Type[BaseModel], output_model: Type[BaseModel], func: Callable):
        if not func_name:
            raise ValueError("func_name must be provided.")
        if not input_model:
            raise ValueError("input_modell must be provided.")
        if not output_model:
            raise ValueError("output_model must be provided.")
        if not func:
            raise ValueError("func be provided.")
        if any(f["name"] == func_name for f in cls._registry):
            raise ValueError(f"Function with name '{func_name}' is already registered.")
        cls._registry.append({
            "name": func_name,
            "input_model": input_model,
            "output_model": output_model,
            "function": func
        })

    @classmethod
    def get_registered_functions(cls) -> List[Dict[str, Any]]:
        return cls._registry
