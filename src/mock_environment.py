import json
from typing import Dict, Any

class MockEnvironment:
    """
    Simulates tool executions and API calls without hitting real production endpoints.
    """
    def __init__(self):
        self.mock_db = {
            "inventory": {"item_123": 50, "item_456": 0},
            "users": {"user_1": {"name": "Alice", "role": "admin"}},
            "orders": {"order_999": {"status": "shipped"}}
        }

    def execute_tool(self, tool_name: str, tool_args: Dict[str, Any]) -> str:
        if tool_name == "check_inventory":
            item_id = tool_args.get("item_id")
            if item_id in self.mock_db["inventory"]:
                return json.dumps({"item_id": item_id, "stock": self.mock_db["inventory"][item_id]})
            return json.dumps({"error": "Item not found"})
        
        elif tool_name == "get_user_info":
            user_id = tool_args.get("user_id")
            if user_id in self.mock_db["users"]:
                return json.dumps(self.mock_db["users"][user_id])
            return json.dumps({"error": "User not found"})
            
        elif tool_name == "get_order_status":
            order_id = tool_args.get("order_id")
            if order_id in self.mock_db["orders"]:
                return json.dumps(self.mock_db["orders"][order_id])
            return json.dumps({"error": "Order not found"})
            
        return json.dumps({"error": f"Unknown tool: {tool_name}"})
