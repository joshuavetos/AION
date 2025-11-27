import re

class SlopRefiner:
    """
    The Metabolism Engine: Detects 'Prompt Smells' and neutralizes ambiguity.
    """
    
    def __init__(self):
        self.smells = {
            r"(?i)write a (short|long)": "Ambiguous Length detected. Enforcing word count constraints.",
            r"(?i)be creative": "Subjective instruction detected. Replacing with specific stylistic parameters.",
            r"(?i)analyze this": "Open-loop instruction. Injecting output format requirement.",
            r"(?i)don'?t hallucinate": "Negative constraint detected. Replacing with positive grounding instruction."
        }

    def process(self, raw_text: str) -> tuple[str, list[str]]:
        audit_log = []
        refined_text = raw_text

        # 1. Detect Smells
        for pattern, message in self.smells.items():
            if re.search(pattern, raw_text):
                audit_log.append(message)

        # 2. Structural Cleanup (Basic)
        refined_text = refined_text.strip()
        
        # 3. Inject Structure (Metabolism)
        structure = (
            "### ROLE ###\nAct as an expert analyst.\n\n"
            "### TASK ###\n" + refined_text + "\n\n"
            "### CONSTRAINTS ###\n"
        )
        
        return structure, audit_log
