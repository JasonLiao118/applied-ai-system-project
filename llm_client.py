"""
Gemini client for the password evaluator.

Adapted from the reference DocuBot llm_client.py pattern:
- Reads GEMINI_API_KEY from the environment
- evaluate_password(): RAG-grounded scoring and explanation

Response is parsed into a structured dict:
  { score: int (1-10), strength: str, verdict: str, explanation: str }
"""

import os
import google.generativeai as genai

GEMINI_MODEL_NAME = "gemini-2.5-flash"


class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "Missing GEMINI_API_KEY environment variable. "
                "Set it in your .env file."
            )
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(GEMINI_MODEL_NAME)

    def evaluate_password(self, password, snippets, user_params):
        """
        Evaluates the password against retrieved criteria and returns a dict:
          score      — integer 1-10
          strength   — "Weak" | "Fair" | "Strong" | "Very Strong"
          verdict    — "Pass" | "Fail"
          explanation — multi-sentence analysis grounded in the criteria
        """
        context = self._format_snippets(snippets)
        purpose = user_params.get("purpose", "General")

        prompt = f"""
You are a password security auditor. Evaluate the password below using only the
security criteria provided from the knowledge base.

Security criteria from knowledge base:
{context}

Password to evaluate: {password}
Intended purpose: {purpose}

Respond in this exact format with no extra text before or after:
SCORE: <integer 1-10>
STRENGTH: <Weak | Fair | Strong | Very Strong>
VERDICT: <Pass | Fail>
EXPLANATION: <3-5 sentences. Cover: character class diversity, length vs the
criteria thresholds, whether it meets the {purpose} requirements, any
anti-patterns detected, and one concrete improvement suggestion if needed.
Ground every claim in the retrieved criteria.>
"""
        response = self.model.generate_content(prompt)
        return self._parse_response((response.text or "").strip())

    def _parse_response(self, text):
        result = {"score": 0, "strength": "Unknown", "verdict": "Unknown", "explanation": text}
        lines = text.splitlines()
        explanation_lines = []
        in_explanation = False

        for line in lines:
            if line.startswith("SCORE:"):
                try:
                    result["score"] = int(line.split(":", 1)[1].strip())
                except ValueError:
                    pass
            elif line.startswith("STRENGTH:"):
                result["strength"] = line.split(":", 1)[1].strip()
            elif line.startswith("VERDICT:"):
                result["verdict"] = line.split(":", 1)[1].strip()
            elif line.startswith("EXPLANATION:"):
                in_explanation = True
                tail = line.split(":", 1)[1].strip()
                if tail:
                    explanation_lines.append(tail)
            elif in_explanation:
                explanation_lines.append(line)

        if explanation_lines:
            result["explanation"] = " ".join(explanation_lines).strip()

        return result

    def _format_snippets(self, snippets):
        if not snippets:
            return "No specific criteria available."
        blocks = [f"[{title}]\n{text}" for title, text in snippets]
        return "\n\n".join(blocks)
