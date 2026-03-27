import re
import sympy
from typing import Dict, Any, List, Optional
from .rlm import RecursiveLanguageModel

class GlobalExtractionEngine:
    """
    G-HAG Build 1.0: Unified Global Extraction Engine.
    Merges AIMO symbolic patterns with RLM-N hypercontext peeking.
    """
    def __init__(self, rlm_depth=1):
        self.rlm = RecursiveLanguageModel(root_model_name="G-HAG-Extraction", depth_limit=rlm_depth)
        self.symbolic_patterns = [
            (r"remainder when (.*?) is divided by (\d+)", "REMAINDER"),
            (r"solve (.*?) for (x|y|n)", "EQUATION"),
        ]

    def extract_and_solve(self, query: str, context: str) -> Dict[str, Any]:
        """
        Two-stage extraction:
        1. Direct symbolic extraction from query/context.
        2. If fails, use symbolic hints to 'peek' into context via RLM-N.
        """
        # Stage 1: Symbolic
        symbolic_res = self._try_symbolic(query)
        if symbolic_res is not None:
            return {"method": "symbolic", "result": symbolic_res, "status": "success"}

        # Stage 2: RLM-N with Symbolic Hints
        hints = self._generate_hints(query)
        self.rlm.environment['hints'] = hints
        rlm_result = self.rlm.process(query, context)

        return {
            "method": "rlm_peeking",
            "hints_used": hints,
            "result": rlm_result,
            "status": "success" if "MATCH" in rlm_result else "partial"
        }

    def _try_symbolic(self, text: str) -> Optional[Any]:
        for pattern, p_type in self.symbolic_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    if p_type == "REMAINDER":
                        expr_str, mod_str = match.groups()
                        expr_cleaned = self._clean_latex(expr_str)
                        # Remove non-math words if any before sympify
                        expr_cleaned = re.sub(r'[a-zA-Z]+', '', expr_cleaned).strip()
                        if not expr_cleaned: continue
                        val = sympy.sympify(expr_cleaned)
                        return int(val % int(mod_str))
                    elif p_type == "EQUATION":
                        eq, var = match.groups()
                        parts = self._clean_latex(eq).split('=')
                        if len(parts) == 2:
                            sol = sympy.solve(sympy.Eq(sympy.sympify(parts[0]), sympy.sympify(parts[1])), sympy.Symbol(var))
                            if sol: return str(sol[0])
                except:
                    continue
        return None

    def _generate_hints(self, query: str) -> List[str]:
        hints = []
        q_lower = query.lower()
        if "remainder" in q_lower: hints.append("modulo")
        if "solve" in q_lower: hints.append("equation")
        if "find" in q_lower: hints.append("target_value")
        return hints

    def _clean_latex(self, s: str) -> str:
        s = s.replace("^", "**").replace("{", "(").replace("}", ")")
        s = s.replace("\\cdot", "*").replace("\\ ", "")
        return s
