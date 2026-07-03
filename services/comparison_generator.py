from services.groq_service import ask_groq


class ComparisonGenerator:

    def compare(self, query: str, retrieved_docs: list):

        if not retrieved_docs:
            return "No matching SHL assessments were found."

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
You are an SHL Assessment comparison assistant.

User request:
{query}

Available SHL assessments:
{catalog}

Instructions:

- Compare ONLY the provided assessments.
- Use ONLY the supplied assessment information.
- Do NOT mention assessments that are not listed.
- Return ONLY a plain English comparison.
- Do NOT use markdown.
- Do NOT return JSON.
- Keep the response under 200 words.
"""

        response = ask_groq(prompt).strip()

        if response.startswith("```"):
            response = response.replace("```json", "").replace("```", "").strip()

        return response