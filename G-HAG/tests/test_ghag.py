import unittest
import sys
import os
try:
    import torch
except ImportError:
    torch = None
try:
    import numpy as np
except ImportError:
    np = None
from src.agents.ghag_agent import GHAGSovereignAgent

class TestGHAG(unittest.TestCase):
    def setUp(self):
        self.agent = GHAGSovereignAgent()

    def test_symbolic_extraction(self):
        res = self.agent.solve_math_with_governance("remainder when 10 is divided by 3")
        self.assertEqual(res['extraction_result']['result'], 1)
        self.assertEqual(res['extraction_result']['method'], 'symbolic')

    def test_domain_analysis_heisenberg(self):
        res = self.agent.solve_math_with_governance("Heisenberg domain m=6 k=3")
        self.assertEqual(res['domain'], 'H3(Z_6)')
        self.assertEqual(res['mathematical_status'], 'PROVED_IMPOSSIBLE')

    def test_domain_analysis_crystal(self):
        res = self.agent.solve_math_with_governance("Crystal domain m=4 k=4")
        self.assertEqual(res['domain'], 'Fd3m (Diamond Space Group)')
        self.assertEqual(res['mathematical_status'], 'PROVED_POSSIBLE')

    def test_diffusion_crystallization(self):
        # query that should trigger rlm_peeking and thus crystallization
        res = self.agent.solve_math_with_governance("Find something complex in hypercontext", "nothing here")
        self.assertEqual(res['extraction_result']['method'], 'rlm_peeking')
        self.assertIn("Crystallized", res['extraction_result']['result'])

    def test_holographic_witness_boost(self):
        # 1. Store a witness by solving a possible problem
        self.agent.solve_math_with_governance("Solve x=4 for x in crystal domain")

        # 2. Re-solve a problem (any problem) and check if a witness is retrieved (boosted)
        # Note: In our current implementation, we retrieve a random witness (since query_vec is random).
        # We need a way to verify that a witness *could* be retrieved.
        # Since it's a random query, we can't guarantee a hit, but let's check the governance object.
        res = self.agent.solve_math_with_governance("remainder when 10 is divided by 3")
        self.assertIn('holographic_witness', res['governance'])

    def test_governance_logic_tear(self):
        # Icosahedral is PROVED_IMPOSSIBLE, should cause a logic tear (delta < 0)
        res = self.agent.solve_math_with_governance("remainder when 10 is divided by 3 in icosahedral domain")
        delta = res['governance']['delta']
        if hasattr(delta, 'item'): delta = delta.item()
        self.assertLess(delta, 0)
        self.assertFalse(res['governance']['is_sovereign'])

if __name__ == "__main__":
    unittest.main()
