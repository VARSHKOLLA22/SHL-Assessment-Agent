from services.groq_service import ask_groq


class RAGGenerator:

    def generate(self, query: str, retrieved_docs: list):

        if not retrieved_docs:
            return "No suitable SHL assessments were found."

        catalog = ""

        for assessment in retrieved_docs:
            catalog += f"""
Assessment Name: {assessment.get("name", "")}

Description:
{assessment.get("description", "")}

Job Levels:
{", ".join(assessment.get("job_levels", []))}

Skills:
{", ".join(assessment.get("keys", []))}

URL:
{assessment.get("link", "")}

----------------------------------------
"""

        prompt = f"""
You are an SHL Assessment Recommendation Assistant.

User hiring requirements:
{query}

Available SHL assessments:
{catalog}

Instructions:

- Recommend ONLY from the assessments provided.
- Consider the entire conversation.
- Explain why the recommended assessments match.
- Do NOT invent assessment names.
- Do NOT use markdown.
- Do NOT return JSON.
- Keep the response under 200 words.
"""

        response = ask_groq(prompt).strip()

        if response.startswith("```"):
            response = response.replace("```json", "").replace("```", "").strip()

        return response