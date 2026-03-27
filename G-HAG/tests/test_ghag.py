import unittest
import sys
import os
import numpy as np
from src.agents.ghag_agent import GHAGSovereignAgent

class TestGHAG(unittest.TestCase):
    def setUp(self):
        self.agent = GHAGSovereignAgent()

    def test_symbolic_extraction(self):
        res = self.agent.solve_math_with_governance("remainder when 10 is divided by 3")
        self.assertEqual(res['extraction_result']['result'], 1)
        self.assertEqual(res['extraction_result']['method'], 'symbolic')

    def test_domain_analysis(self):
        res = self.agent.solve_math_with_governance("icosahedral domain")
        self.assertEqual(res['domain'], '2I (Binary Icosahedral Group)')
        self.assertEqual(res['mathematical_status'], 'PROVED_IMPOSSIBLE')

    def test_governance_logic_tear(self):
        # Icosahedral is PROVED_IMPOSSIBLE, should cause a logic tear (delta < 0)
        res = self.agent.solve_math_with_governance("remainder when 10 is divided by 3 in icosahedral domain")
        delta = res['governance']['delta']
        if hasattr(delta, 'item'): delta = delta.item()
        self.assertLess(delta, 0)
        self.assertFalse(res['governance']['is_sovereign'])

if __name__ == "__main__":
    unittest.main()
