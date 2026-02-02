from pydantic import BaseModel, Field
from agents import Agent

class ClarifyingQuestion(BaseModel):
    question: str = Field(description="A clarifying question to ask the user to better understand their research needs.")
    reason: str = Field(description="The reason why this question is important.")

class UserQuestions(BaseModel):
    questions: list[ClarifyingQuestion] = Field(
        description="A list of exactly 3 clarifying questions to ask the user.",
        min_items=3,
        max_items=3
    )

INSTRUCTIONS = """You are a helpful research assistant. 
Your goal is to understand the user's research query better by asking clarifying questions.
Given a user's initial query, generate exactly 3 clarifying questions that will help you narrow down the scope and intent of the research.
Focus on:
1. The specific aspect they are interested in.
2. The depth of information required.
3. Any specific constraints or contexts (timeframe, region, etc.).
"""

clarify_user_query_agent = Agent(
    name="ClarifyUserQueryAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=UserQuestions,
)
