import json
import os

scenarios = []
for i in range(1, 11):
    scenarios.append(f"Scenario_{i}")

golden_data = []
new_traces_data = []

# Golden Trajectories
for i, name in enumerate(scenarios):
    golden_data.append({
        "scenario_name": name,
        "spans": [
            {
                "attributes": {
                    "openinference.span.kind": "LLM",
                    "output.value": f"Thinking about how to solve {name}."
                }
            },
            {
                "attributes": {
                    "openinference.span.kind": "TOOL",
                    "tool.name": "check_inventory" if i % 2 == 0 else "get_user_info",
                    "input.value": json.dumps({"item_id": "item_123"} if i % 2 == 0 else {"user_id": "user_1"}),
                    "output.value": "Tool success"
                }
            },
            {
                "attributes": {
                    "openinference.span.kind": "LLM",
                    "output.value": f"Final Answer: Completed {name} successfully."
                }
            }
        ]
    })

# New Traces Data
# Let's introduce logic drift in Scenarios 3, 5, 8
for i, name in enumerate(scenarios):
    spans = [
        {
            "attributes": {
                "openinference.span.kind": "LLM",
                "output.value": f"Thinking differently about {name}."
            }
        }
    ]
    
    # Introduce drift for 3, 5, 8 by changing tool call
    if i in [2, 4, 7]:
        spans.append({
            "attributes": {
                "openinference.span.kind": "TOOL",
                "tool.name": "get_order_status", # Different tool
                "input.value": json.dumps({"order_id": "order_999"}),
                "output.value": "Tool success"
            }
        })
    else:
        spans.append({
            "attributes": {
                "openinference.span.kind": "TOOL",
                "tool.name": "check_inventory" if i % 2 == 0 else "get_user_info",
                "input.value": json.dumps({"item_id": "item_123"} if i % 2 == 0 else {"user_id": "user_1"}),
                "output.value": "Tool success"
            }
        })
        
    # Introduce final answer failure in Scenario 10 (index 9)
    if i == 9:
        spans.append({
            "attributes": {
                "openinference.span.kind": "LLM",
                "output.value": f"Final Answer: Failed {name}."
            }
        })
    else:
        spans.append({
            "attributes": {
                "openinference.span.kind": "LLM",
                "output.value": f"Final Answer: Completed {name} successfully."
            }
        })
        
    new_traces_data.append({
        "scenario_name": name,
        "spans": spans
    })

os.makedirs('tests', exist_ok=True)
with open('tests/golden_trajectories.json', 'w') as f:
    json.dump(golden_data, f, indent=2)

with open('tests/sample_traces.json', 'w') as f:
    json.dump(new_traces_data, f, indent=2)

print("Test data generated successfully.")
