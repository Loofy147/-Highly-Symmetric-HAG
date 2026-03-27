import sys
import os
import torch
from src.agents.ghag_agent import GHAGSovereignAgent

def main():
    print("====================================================")
    print("   G-HAG Build 4.0 — Sovereign Mathematical Agent   ")
    print("   Integrated RSI | VHSE | RIBB | Active Inference  ")
    print("====================================================")

    # 1. Initialize GHAG Sovereign Agent
    agent = GHAGSovereignAgent()

    # 2. Test 1: Heisenberg Commutator (Symbolic Expansion)
    problem_desc1 = "Evaluate the commutator [P, Q] in the Heisenberg domain."
    print(f"\n[TASK 1] Heisenberg Commutator Extraction...")
    res1 = agent.solve_math_with_governance(problem_desc1, "")
    print(f"  Result: {res1['extraction_result']['result']}")
    print(f"  Domain: {res1['domain']} (Status: {res1['mathematical_status']})")

    # 3. Test 2: Semantic Holographic Retrieval (Proof Anchoring)
    # Solve a possible problem to anchor the witness
    problem_desc2 = "Solve x**2 = 16 for x in the crystal domain."
    print(f"\n[TASK 2a] Crystal solving & Proof Anchoring...")
    agent.solve_math_with_governance(problem_desc2, "")

    # Solve again to retrieve the witness
    print(f"\n[TASK 2b] Semantic Retrieval (Holographic Match)...")
    res2 = agent.solve_math_with_governance(problem_desc2, "")
    print(f"  Holographic Witness Found: {res2['governance']['holographic_witness']}")
    print(f"  Governance Status: {res2['governance']['status']}")

    # 4. Test 3: Active Inference Depth Elevation (Surprise)
    # Icosahedral is PROVED_IMPOSSIBLE, triggering "surprise" and depth elevation
    problem_desc3 = "Find the parity of (123) in S_3 in the Icosahedral domain."
    print(f"\n[TASK 3] Icosahedral Surprise (Depth Elevation)...")
    res3 = agent.solve_math_with_governance(problem_desc3, "Large context...")
    print(f"  Math Status: {res3['mathematical_status']}")
    print(f"  Current RLM Depth: {agent.extraction_engine.rlm.depth_limit}")

    print("\n--- G-HAG Build 4.0 Execution Complete ---")

if __name__ == "__main__":
    main()
