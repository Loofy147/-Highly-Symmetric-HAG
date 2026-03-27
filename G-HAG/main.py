import sys
import os
from src.agents.ghag_agent import GHAGSovereignAgent

def main():
    print("====================================================")
    print("   G-HAG Build 1.0 — Sovereign Mathematical Agent   ")
    print("====================================================")

    # 1. Initialize GHAG Sovereign Agent
    agent = GHAGSovereignAgent()

    # 2. Feed Mathematical Task into HAG Sovereignty Loop
    # Description includes mathematical domain + AIMO extraction challenge
    problem_desc = "Find the remainder when 3**20 is divided by 100 in the Icosahedral domain."

    # Large context for RLM-N peeking if symbolic fails (which 3**20 might if we didn't have sympify)
    super_context = "Historical data for Icosahedral symmetry: SES is 0 -> Z2 -> 2I -> I -> 0. "                     "Critical pattern: 3**20 % 100 is 1. "                     "Sovereignty condition: delta must be > 0.001."

    print(f"\n[FEED-TOGETHER] Feeding problem into GHAG Loop...")
    res = agent.solve_math_with_governance(problem_desc, super_context)

    # 3. Output results with mathematical and governance verification
    print("\n[RESULT] Unified Intelligence Output:")
    print(f"  Problem:  {res['problem']}")
    print(f"  Domain:   {res['domain']}")
    print(f"  Math:     {res['mathematical_status']}")
    print(f"  Extract:  {res['extraction_result']['method']} (Result: {res['extraction_result']['result']})")
    print(f"  Gov:      Delta={res['governance']['delta']:.4f} ({res['governance']['status']})")

    # 4. Feedback Loop: Use Math to parameterize HAG stability
    print(f"\n[FEEDBACK] Math engine status '{res['mathematical_status']}' fed back to HAG values...")
    if res['mathematical_status'] == "PROVED_IMPOSSIBLE":
        agent.values.task_accuracy_target = 0.99
        print(f"  High-confidence result detected! Accuracy target elevated to {agent.values.task_accuracy_target}.")

    print("\n--- G-HAG Execution Complete ---")

if __name__ == "__main__":
    main()
