from langchain_core.tools import tool

# Sample Inventory
inventory = [
    {"id": 1, "item": "Fridge", "price": 12.99},
    {"id": 2, "item": "Bats and balls", "price": 30},
    {"id": 3, "item": "Air conditioner", "price": 17.67}
]
# === TOOL: Check User Inventory ===
@tool
def check_user_inventory(inventory_id: int):
    """
    Check the user's current inventory based on the inventory ID.
    """
    for item in inventory:
        if item["id"] == inventory_id:
            return item
    return None
# === TOOL: Refund Item ===
@tool
def refund_item(inventory_id: int):
    """
    Perform a refund for an item the user owns.
    """
    item = check_user_inventory({"inventory_id": inventory_id})
    if item is None:
        raise ValueError(f"Item with ID: {inventory_id} not found in inventory")

    for i, inv_item in enumerate(inventory):
        if inv_item["id"] == inventory_id:
            inventory.pop(i)
            return {"status": "refunded", "remaining_inventory": inventory}

    raise ValueError("Unexpected error during refund")
# === TOOL: Replacement Tool ===
@tool
def replacement_tool(inventory_id: int):
    """
    Order a replacement for an item the user owns.
    """
    item = check_user_inventory({"inventory_id": inventory_id})
    if item is None:
        raise ValueError(f"Item with ID: {inventory_id} not found in inventory")

    for i, inv_item in enumerate(inventory):
        if inv_item["id"] == inventory_id:
            inventory.pop(i)
            return {
                "status": "replacement_ordered",
                "removed_item": inv_item,
                "remaining_inventory": inventory
            }

    raise ValueError("Unexpected error during replacement")