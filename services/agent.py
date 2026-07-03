from functools import lru_cache

from services.retriever import SHLRetriever
from services.agent_brain import AgentBrain
from services.rag_generator import RAGGenerator
from services.comparison_generator import ComparisonGenerator


@lru_cache(maxsize=1)
def get_retriever():
    return SHLRetriever()


class SHLAgent:

    def __init__(self):
        self.retriever = get_retriever()
        self.brain = AgentBrain()
        self.rag = RAGGenerator()
        self.comparison = ComparisonGenerator()

    def reply(self, messages):

        # Detect intent
        decision = self.brain.decide(messages)

        # Clarification
        if decision == "clarify":
            return {
                "reply": (
                    "Could you provide a few more details about the role?\n\n"
                    "• Job title\n"
                    "• Experience level\n"
                    "• Required skills\n"
                    "• Preferred competencies"
                ),
                "recommendations": [],
                "end_of_conversation": False,
            }

        # Off-topic
        if decision == "refuse":
            return {
                "reply": (
                    "I can only assist with SHL assessment recommendations, "
                    "assessment comparisons, and hiring-related queries."
                ),
                "recommendations": [],
                "end_of_conversation": True,
            }

        # Build conversation
        conversation = "\n".join(
            message.content 
            for message in messages
            if message.role == "user"
        )

        # Retrieve assessments
        if decision == "compare":
            top_k = 10
        elif decision == "refine":
            top_k = 15
        else:
            top_k = 8

        results = self.retriever.search(
            conversation,
            top_k=top_k
        )

        # No results
        if not results:
            return {
                "reply": "No suitable SHL assessments were found.",
                "recommendations": [],
                "end_of_conversation": True,
            }

        # Generate response
        if decision == "compare":
            reply = self.comparison.compare(
                conversation,
                results
            )
        else:
            reply = self.rag.generate(
                conversation,
                results
            )

        recommendations = [
            {
                "name": assessment["name"],
                "url": assessment["link"]
            }
            for assessment in results[:10]
        ]

        return {
            "reply": reply,
            "recommendations": recommendations,
            "end_of_conversation": True,
        }