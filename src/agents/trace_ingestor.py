import json
from typing import List, Dict, Any
from src.models import AgentTrajectory, AgentStep, StepType

class TraceIngestor:
    """
    Sub-Agent: Trace Ingestor
    Listens to OTel spans and converts raw JSON traces into structured "Agent Trajectories".
    """
    
    def ingest(self, scenario_name: str, raw_spans: List[Dict[str, Any]]) -> AgentTrajectory:
        """
        Parses raw OpenTelemetry (OpenInference) spans into an AgentTrajectory.
        Expects spans to have attributes mapping to chain/tool/llm types.
        """
        trajectory = AgentTrajectory(scenario_name=scenario_name)
        
        # Sort spans by timestamp if available, else assume ordered
        # Mock implementation: parse custom attributes we inject
        for span in raw_spans:
            attributes = span.get("attributes", {})
            span_kind = attributes.get("openinference.span.kind")
            
            if span_kind == "LLM":
                # Extract thought and/or final answer
                output = attributes.get("output.value", "")
                if "Final Answer:" in output:
                    trajectory.steps.append(
                        AgentStep(step_type=StepType.FINAL_ANSWER, content=output)
                    )
                else:
                    trajectory.steps.append(
                        AgentStep(step_type=StepType.THOUGHT, content=output)
                    )
            elif span_kind == "TOOL":
                tool_name = attributes.get("tool.name", "unknown_tool")
                tool_args_str = attributes.get("input.value", "{}")
                try:
                    tool_args = json.loads(tool_args_str)
                except:
                    tool_args = {}
                
                # Tool Call Step
                trajectory.steps.append(
                    AgentStep(
                        step_type=StepType.TOOL_CALL,
                        content=f"Calling tool {tool_name}",
                        tool_name=tool_name,
                        tool_args=tool_args
                    )
                )
                
                # Tool Observation Step
                tool_output = attributes.get("output.value", "")
                trajectory.steps.append(
                    AgentStep(
                        step_type=StepType.OBSERVATION,
                        content=tool_output
                    )
                )
                
        return trajectory
