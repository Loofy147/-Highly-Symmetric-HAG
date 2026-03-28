import time
import sys
import os
import numpy as np
import torch
from src.agents.ghag_agent import GHAGSovereignAgent
from src.indexing.ribbon import RibbonIndexer

class GHAGBenchmarker:
    def __init__(self):
        self.agent = GHAGSovereignAgent()

    def run_benchmark(self):
        print(f"HAG-OS Build 4.0: Initiating Wide-scale Benchmarking Suite...")

        # 1. Multi-agent Sync Scalability
        self.benchmark_dce_sync()

        # 2. Suffix Smoothing Stability
        self.benchmark_suffix_smoothing()

        # 3. Ribbon Indexer Efficiency
        self.benchmark_ribbon_indexer()

        # 4. Standard Domain Tasks
        self.benchmark_domains()

    def benchmark_dce_sync(self):
        print("\n--- [DCE Sync Scalability] ---")
        for num_peers in [1, 5, 10]:
            # Register peers
            for i in range(num_peers):
                peer_id = f"Peer-{i}"
                peer_identity = torch.sign(torch.randn(8192))
                self.agent.dce_node.register_peer(peer_id, peer_identity)
                self.agent.dce_node.shared_bulk.store(peer_identity, torch.randn(8192))

            t0 = time.perf_counter()
            collective = self.agent.dce_node.sync_collective_state()
            dt = (time.perf_counter() - t0) * 1000
            print(f"  Peers: {num_peers:2} | Sync Latency: {dt:6.2f}ms | Norm: {torch.norm(collective):.4f}")

    def benchmark_suffix_smoothing(self):
        print("\n--- [Suffix Smoothing Stability] ---")
        rlm = self.agent.extraction_engine.rlm
        raw_prob = 0.95
        past_prob = 0.92
        for depth in range(5):
            smoothed = rlm.apply_suffix_smoothing(raw_prob, past_prob, depth=depth)
            print(f"  Depth: {depth} | Smoothed Prob: {smoothed:.4f}")

    def benchmark_ribbon_indexer(self):
        print("\n--- [Ribbon Indexer Efficiency] ---")
        indexer = RibbonIndexer(num_keys=1000)
        keys = [f"key_{i}" for i in range(500)]
        meta = [f"meta_{i}" for i in range(500)]

        t0 = time.perf_counter()
        indexer.add_batch(keys, meta)
        t_add = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        for k in keys[:100]: indexer.query(k)
        t_query = (time.perf_counter() - t0) * 1000 / 100

        usage = indexer.get_memory_usage()
        print(f"  Add (500 keys): {t_add:6.2f}ms | Query Latency: {t_query:6.4f}ms | Savings: {usage['memory_savings']}")

    def benchmark_domains(self):
        print("\n--- [Standard Domain Tasks] ---")
        tasks = [
            ("remainder when 10 is divided by 3", "Symbolic Extraction"),
            ("Heisenberg domain m=6 k=3", "Heisenberg (Impossible)"),
            ("Crystal domain m=4 k=4", "Crystal (Possible)")
        ]

        print(f"{'Task':<40} | {'Time (ms)':<10} | {'Status'}")
        print("-" * 65)
        for desc, label in tasks:
            t0 = time.perf_counter()
            res = self.agent.solve_math_with_governance(desc)
            dt = (time.perf_counter() - t0) * 1000
            print(f"{label:<40} | {dt:<10.2f} | {res['mathematical_status']}")

if __name__ == "__main__":
    bench = GHAGBenchmarker()
    bench.run_benchmark()
