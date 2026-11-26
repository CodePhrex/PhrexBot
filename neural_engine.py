"""Separate cloud benchmark path; no production evidence accepted."""
from dataclasses import dataclass
import requests

@dataclass(frozen=True)
class CloudProbe:
    model: str
    enabled: bool = False

    def run(self, session=None):
        if self.enabled is not True:
            raise PermissionError("Cloud probe not authorized")
        if not isinstance(self.model, str) or not self.model.lower().endswith(":cloud"):
            raise ValueError("Explicit cloud model required")
        client = session or requests
        with client.post("http://127.0.0.1:11434/api/chat",
                         json={"model": self.model, "stream": False,
                               "messages": [{"role": "user", "content": "Reply with the word ready."}],
                               "options": {"num_predict": 16}},
                         timeout=(5, 30), allow_redirects=False) as response:
            return {"available": response.status_code == 200,
                    "status_code": response.status_code}
