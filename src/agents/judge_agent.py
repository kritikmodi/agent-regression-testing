from src.models import AgentTrajectory, EvaluationResult

class JudgeAgent:
    """
    Sub-Agent: Semantic Evaluator
    Uses an LLM-as-a-judge approach to semantically compare new trajectories against golden trajectories.
    """
    
    def evaluate(self, golden: AgentTrajectory, new: AgentTrajectory) -> EvaluationResult:
        """
        Mock implementation of an LLM judge.
        Compares the sequence of tool calls to detect path divergence.
        """
        golden_tools = [step.tool_name for step in golden.steps if step.step_type == "TOOL_CALL"]
        new_tools = [step.tool_name for step in new.steps if step.step_type == "TOOL_CALL"]
        
        drift_detected = False
        reasoning = "Trajectories match semantically."
        score = 1.0
        
        if golden_tools != new_tools:
            drift_detected = True
            # Calculate a simple sequence overlap score for trajectory grading
            matched = sum(1 for g, n in zip(golden_tools, new_tools) if g == n)
            max_len = max(len(golden_tools), len(new_tools))
            trajectory_score = matched / max_len if max_len > 0 else 0.0
            score = trajectory_score * 0.5 # 50% weight for tools if they differ
            reasoning = f"Trajectory drift detected (Score: {trajectory_score:.2f})! Golden called {golden_tools}, but New called {new_tools}."
        
        # Check final answer
        golden_final = [step.content for step in golden.steps if step.step_type == "FINAL_ANSWER"]
        new_final = [step.content for step in new.steps if step.step_type == "FINAL_ANSWER"]
        
        if golden_final and new_final:
            if golden_final[0] != new_final[0]:
                drift_detected = True
                score = score * 0.5 # Reduce score if final answer is wrong
                reasoning += f" Final answers differ: Golden='{golden_final[0]}', New='{new_final[0]}'."
                
        return EvaluationResult(
            scenario_name=golden.scenario_name,
            passed=not drift_detected,
            score=score,
            reasoning=reasoning,
            drift_detected=drift_detected
        )
