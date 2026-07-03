import re

from services.gemini_service import ask_gemini


class AgentBrain:

    def decide(self, messages):

        latest = messages[-1].content.lower().strip()

        # Remove punctuation for consistent matching
        latest = re.sub(r"[^\w\s]", "", latest)

        # ----------------------------
        # Comparison
        # ----------------------------
        comparison_keywords = [
            "compare",
            "difference",
            "vs",
            "versus"
        ]

        if any(word in latest for word in comparison_keywords):
            return "compare"

        # ----------------------------
        # Off-topic / Prompt Injection
        # ----------------------------
        refuse_keywords = [
            "ignore previous",
            "forget previous",
            "system prompt",
            "write a poem",
            "write code",
            "weather",
            "ipl",
            "cricket",
            "football",
            "movie",
            "recipe",
            "joke",
            "news"
        ]

        if any(word in latest for word in refuse_keywords):
            return "refuse"

        # ----------------------------
        # Generic hiring request
        # ----------------------------
        generic_patterns = [
            "hire someone",
            "hiring someone",
            "need to hire",
            "help me hire",
            "recommend an assessment"
        ]

        if any(pattern in latest for pattern in generic_patterns):
            return "clarify"

        # ----------------------------
        # Follow-up refinement
        # ----------------------------
        if len(messages) > 1:

            refine_keywords = [
                "also",
                "add",
                "include",
                "remove",
                "instead",
                "change",
                "make it",
                "leadership",
                "communication",
                "docker",
                "kubernetes",
                "spring",
                "spring boot",
                "react",
                "aws",
                "azure",
                "gcp",
                "senior",
                "junior",
                "entry level"
            ]

            if any(word in latest for word in refine_keywords):
                return "refine"

        # ----------------------------
        # Specific hiring request
        # ----------------------------
        hiring_keywords = [
            "developer",
            "engineer",
            "analyst",
            "manager",
            "consultant",
            "intern",
            "architect",
            "administrator",
            "python",
            "java",
            "react",
            "angular",
            "node",
            "backend",
            "frontend",
            "full stack",
            "fullstack",
            "qa",
            "testing",
            "automation",
            "devops",
            "cloud",
            "aws",
            "azure",
            "gcp",
            "sql",
            "data",
            "machine learning",
            "artificial intelligence",
            "ai",
            "cybersecurity"
        ]

        if any(keyword in latest for keyword in hiring_keywords):
            return "recommend"

        # ----------------------------
        # LLM fallback
        # ----------------------------
        conversation = "\n".join(
            f"{message.role}: {message.content}"
            for message in messages
        )

        prompt = f"""
You are an intent classifier.

Return ONLY one word.

Choices:
clarify
recommend
refine
compare
refuse

Conversation:

{conversation}
"""

        response = ask_gemini(prompt).strip().lower()

        if response not in {
            "clarify",
            "recommend",
            "refine",
            "compare",
            "refuse"
        }:
            return "clarify"

        return response