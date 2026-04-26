"""
PasswordBot: RAG core for the password evaluator.
"""

import os


class PasswordBot:
    def __init__(self, docs_file="Docs/secure_passwords.md", llm_client=None):
        self.docs_file = docs_file
        self.llm_client = llm_client
        self.documents = self.load_documents()
        self.index = self.build_index(self.documents)

    # ------------------------------------------------------------------
    # Document loading
    # ------------------------------------------------------------------

    def load_documents(self):
        """
        Loads secure_passwords.md and splits it into sections at ## and ###
        headings. Returns a list of (section_title, text) tuples.
        """
        if not os.path.exists(self.docs_file):
            return []

        with open(self.docs_file, "r", encoding="utf8") as f:
            text = f.read()

        sections = []
        current_title = "General"
        current_lines = []

        for line in text.splitlines():
            if line.startswith("## ") or line.startswith("### "):
                if current_lines:
                    sections.append((current_title, "\n".join(current_lines).strip()))
                current_title = line.lstrip("#").strip()
                current_lines = [line]
            else:
                current_lines.append(line)

        if current_lines:
            sections.append((current_title, "\n".join(current_lines).strip()))

        return sections

    # ------------------------------------------------------------------
    # Index construction (same approach as docubot.py reference)
    # ------------------------------------------------------------------

    def build_index(self, documents):
        """
        Builds an inverted index mapping lowercase words to section titles.
        """
        index = {}
        for title, text in documents:
            words = set(text.lower().split())
            for word in words:
                if word not in index:
                    index[word] = []
                if title not in index[word]:
                    index[word].append(title)
        return index

    # ------------------------------------------------------------------
    # Scoring and retrieval
    # ------------------------------------------------------------------

    def score_document(self, query, text):
        """
        Counts how many query words appear in the section text.
        Simple word-overlap score, same as the reference pattern.
        """
        query_words = query.lower().split()
        text_lower = text.lower()
        return sum(1 for word in query_words if word in text_lower)

    def retrieve(self, query, top_k=4):
        """
        Returns the top_k most relevant (title, text) sections for the query,
        sorted by score descending.
        """
        scored = [
            (title, text, self.score_document(query, text))
            for title, text in self.documents
        ]
        scored.sort(key=lambda x: x[2], reverse=True)
        return [(title, text) for title, text, _ in scored[:top_k]]

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def evaluate_password(self, password, user_params):
        """
        Retrieves relevant criteria from the grounding file, then asks
        the LLM to score and explain the given password.

        Returns a dict: { score, strength, verdict, explanation }
        """
        if self.llm_client is None:
            raise RuntimeError("An LLM client is required for evaluation.")
        query = self._build_query(password, user_params)
        snippets = self.retrieve(query, top_k=4)
        return self.llm_client.evaluate_password(password, snippets, user_params)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_query(self, password, user_params):
        """
        Builds a retrieval query from the password itself and the stated purpose
        so the index returns the most relevant criteria sections.
        """
        parts = [
            user_params.get("purpose", "general"),
            f"length {len(password)} characters",
        ]
        if any(c.isupper() for c in password):
            parts.append("uppercase")
        if any(c.islower() for c in password):
            parts.append("lowercase")
        if any(c.isdigit() for c in password):
            parts.append("digits numbers")
        if any(not c.isalnum() for c in password):
            parts.append("special characters symbols")
        return " ".join(parts)
