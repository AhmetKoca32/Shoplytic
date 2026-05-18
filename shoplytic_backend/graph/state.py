from typing import TypedDict, Optional, List, Annotated


class ShopLyticState(TypedDict):
    # Input
    user_input: str
    thread_id: str

    # Agent Outputs
    context_analysis: Optional[dict]
    mind_map: Optional[dict]
    product_recommendations: Optional[dict]
    legal_analysis: Optional[dict]

    # Conversation
    messages: Annotated[list, "add_messages"]

    # Meta
    current_step: str
    error: Optional[str]
