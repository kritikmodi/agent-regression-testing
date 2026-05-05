import json
import os
from typing import List, Dict, Any
from src.agents.trace_ingestor import TraceIngestor
from src.agents.judge_agent import JudgeAgent
from src.models import EvaluationResult

class TestRunner:
    """
    Orchestrator Agent
    Manages the lifecycle of a regression test suite.
    """
    def __init__(self):
        self.trace_ingestor = TraceIngestor()
        self.judge_agent = JudgeAgent()

    def run_suite(self, golden_path: str, new_traces_path: str) -> List[EvaluationResult]:
        """
        Runs the test suite by loading golden trajectories and new traces,
        ingesting them, and evaluating them.
        """
        with open(golden_path, 'r') as f:
            golden_data = json.load(f)
            
        with open(new_traces_path, 'r') as f:
            new_traces_data = json.load(f)
            
        results = []
        
        # Assume golden_data is a list of scenario dicts with raw spans
        # Assume new_traces_data is a list of scenario dicts with raw spans
        
        golden_scenarios = {s["scenario_name"]: s["spans"] for s in golden_data}
        new_scenarios = {s["scenario_name"]: s["spans"] for s in new_traces_data}
        
        for scenario_name, golden_spans in golden_scenarios.items():
            if scenario_name not in new_scenarios:
                continue
                
            new_spans = new_scenarios[scenario_name]
            
            # 1. Ingest
            golden_traj = self.trace_ingestor.ingest(scenario_name, golden_spans)
            new_traj = self.trace_ingestor.ingest(scenario_name, new_spans)
            
            # 2. Evaluate
            result = self.judge_agent.evaluate(golden_traj, new_traj)
            results.append(result)
            
        return results
