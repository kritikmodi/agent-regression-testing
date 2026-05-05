from enum import Enum
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field

class StepType(str, Enum):
    THOUGHT = "THOUGHT"
    TOOL_CALL = "TOOL_CALL"
    OBSERVATION = "OBSERVATION"
    FINAL_ANSWER = "FINAL_ANSWER"

class AgentStep(BaseModel):
    step_type: StepType
    content: str
    tool_name: Optional[str] = None
    tool_args: Optional[Dict[str, Any]] = None

class AgentTrajectory(BaseModel):
    scenario_name: str
    steps: List[AgentStep] = Field(default_factory=list)

class EvaluationResult(BaseModel):
    scenario_name: str
    passed: bool
    score: float
    reasoning: str
    drift_detected: bool
