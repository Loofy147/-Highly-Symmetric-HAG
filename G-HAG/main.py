import sys
import os
import torch
from src.agents.ghag_agent import GHAGSovereignAgent

def main():
    print("====================================================")
    print("   G-HAG Build 4.0 — Sovereign Mathematical Agent   ")
    print("   Domain Expansion: Heisenberg | Magic | S3        ")
    print("====================================================")

    # 1. Initialize GHAG Sovereign Agent
    agent = GHAGSovereignAgent()

    # 2. Feed Mathematical Task into HAG Sovereignty Loop
    # Test 1: Heisenberg domain (should be PROVED_IMPOSSIBLE)
    problem_desc = "Find the remainder when 3**20 is divided by 100 in the Heisenberg domain."
    super_context = "Historical data for Heisenberg symmetry: Central extension 0 -> Z_m -> H -> Z_m^2 -> 0."

    print(f"\n[TASK 1] Heisenberg domain challenge...")
    res1 = agent.solve_math_with_governance(problem_desc, super_context)

    print("\n[RESULT 1] Unified Intelligence Output:")
    print(f"  Problem:  {res1['problem']}")
    print(f"  Domain:   {res1['domain']}")
    print(f"  Math:     {res1['mathematical_status']}")
    print(f"  Extract:  {res1['extraction_result']['method']} (Result: {res1['extraction_result']['result']})")
    print(f"  Gov:      Delta={res1['governance']['delta']:.4f} ({res1['governance']['status']})")
    print(f"  Witness:  {res1['governance']['holographic_witness']}")

    # Test 2: Crystal domain (should be OPEN/PROVED_POSSIBLE)
    problem_desc2 = "Solve x**2 - 4 = 0 for x in the crystal domain."
    print(f"\n[TASK 2] Crystal domain challenge...")
    res2 = agent.solve_math_with_governance(problem_desc2, "")

    print("\n[RESULT 2] Unified Intelligence Output:")
    print(f"  Math:     {res2['mathematical_status']}")
    print(f"  Extract:  {res2['extraction_result']['method']} (Result: {res2['extraction_result']['result']})")
    print(f"  Gov:      Delta={res2['governance']['delta']:.4f} ({res2['governance']['status']})")

    # Check if a witness was anchored
    if res2['extraction_result']['status'] == "success" and not res2['governance']['discrete_obstruction_detected']:
        print(f"\n[ANCHOR] Witness anchored in VHSE for subsequent retrieval.")

    print("\n--- G-HAG Build 4.0 Execution Complete ---")

if __name__ == "__main__":
    main()
