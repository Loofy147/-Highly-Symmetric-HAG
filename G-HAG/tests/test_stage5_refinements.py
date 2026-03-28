import unittest
import torch
from src.agents.rlm import RecursiveLanguageModel
from src.indexing.ribbon import RibbonIndexer
from src.agents.distributed_sync import DistributedAgentNode
from src.agents.ghag_agent import GHAGSovereignAgent

class TestStage5Refinements(unittest.TestCase):
    def test_depth_aware_suffix_smoothing(self):
        rlm = RecursiveLanguageModel()
        phi = 0.8
        raw_prob = 0.95
        past_prob = 0.92

        # At depth 0, effective phi = 0.8
        smoothed_d0 = rlm.apply_suffix_smoothing(raw_prob, past_prob, depth=0, phi=phi)
        expected_d0 = 0.8 * raw_prob + 0.2 * past_prob
        self.assertAlmostEqual(smoothed_d0, expected_d0)

        # At depth 1, effective phi = 0.8 * 0.9 = 0.72
        smoothed_d1 = rlm.apply_suffix_smoothing(raw_prob, past_prob, depth=1, phi=phi)
        expected_d1 = 0.72 * raw_prob + 0.28 * past_prob
        self.assertAlmostEqual(smoothed_d1, expected_d1)

        # Verify deeper recursions have less influence (phi decreases)
        self.assertLess(smoothed_d1, smoothed_d0)

    def test_full_gaussian_ribbon(self):
        # Even with row-reduction, it should correctly retrieve stored metadata
        indexer = RibbonIndexer(num_keys=20)
        keys = [f"morphism_{i}" for i in range(10)]
        meta = [f"META_{i}" for i in range(10)]

        indexer.add_batch(keys, meta)

        for k, v in zip(keys, meta):
            self.assertEqual(indexer.query(k), v)

    def test_dce_peer_registry_sync(self):
        node = DistributedAgentNode(agent_id="Node-01")
        peer_id = "Node-02"
        peer_identity = torch.sign(torch.randn(8192))

        node.register_peer(peer_id, peer_identity)

        # Manually store something in shared_bulk for the peer identity
        peer_state = torch.ones(8192)
        node.shared_bulk.store(peer_identity, peer_state)

        # Syncing without arguments should use the registry
        collective_state = node.sync_collective_state()
        self.assertAlmostEqual(torch.norm(collective_state).item(), torch.norm(peer_state).item())

    def test_agent_collective_sync(self):
        agent = GHAGSovereignAgent()
        peer_id = "Agent-02"
        peer_identity = torch.sign(torch.randn(8192))

        agent.dce_node.register_peer(peer_id, peer_identity)

        # Store state for peer
        peer_state = torch.randn(8192)
        agent.dce_node.shared_bulk.store(peer_identity, peer_state)

        # Solving a problem should trigger sync message
        res = agent.solve_math_with_governance("remainder when 10 is divided by 3")
        # Check extraction context if we could (simplified)
        self.assertEqual(res['extraction_result']['status'], 'success')

if __name__ == "__main__":
    unittest.main()
