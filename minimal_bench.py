import time
import sys
import os
from src.agents.ghag_agent import GHAGSovereignAgent

print("Imported GHAGSovereignAgent")
t0 = time.perf_counter()
agent = GHAGSovereignAgent()
print(f"Agent initialized in {(time.perf_counter() - t0)*1000:.2f}ms")

problem = "remainder when 10 is divided by 3 in icosahedral domain"
t0 = time.perf_counter()
res = agent.solve_math_with_governance(problem)
print(f"Solved in {(time.perf_counter() - t0)*1000:.2f}ms")
print(res)
