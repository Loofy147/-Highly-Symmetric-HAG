from dataclasses import dataclass
import json
import os
try:
    import numpy as np
except ImportError:
    np = None

@dataclass
class QScoreWeights:
    grounding: float = 0.18
    certainty: float = 0.22
    structure: float = 0.20
    applicability: float = 0.18
    coherence: float = 0.12
    generativity: float = 0.10

class SystemValues:
    """
    Central repository for HAG system constants and Bayesian values.
    Updated for HAG-Desktop Build 4.0: Sovereign Desktop Integration.
    """
    def __init__(self, config_path="configs/bayesian_weights.json"):
        # Default Build 4.0 Values
        self.version = "4.0.1-SOVEREIGN-DESKTOP"
        self.q_weights = QScoreWeights()
        self.q_threshold = 0.984
        self.snapshot_compression_ratio = 50.0
        self.ram_optimization_target = 0.42
        self.task_accuracy_target = 0.96 # Harmonized to 0.96
        self.aime_accuracy_target = 1.0
        self.error_amplification_limit = 4.4
        self.hallucination_reduction_target = 0.427
        self.weyl_delta_limit = 0.001

        # Build 4.0 Desktop Metrics
        self.desktop_security_target = 0.96 # 96% L1 isolation
        self.rlm_peeking_accuracy = 0.62   # 62% Context peeking
        self.voice_latency_ms_target = 120.0 # < 120ms
        self.e_desktop_stable_threshold = 20.0

        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    build = config.get("HAG_Build", {})
                    self.version = build.get("version", self.version)
                    self.task_accuracy_target = build.get("task_accuracy", self.task_accuracy_target)

                    kf_ng = config.get("KF_NG", {})
                    self.q_threshold = kf_ng.get("q_threshold", self.q_threshold)

                    w = config.get("Q_Score_Weights", {})
                    self.q_weights = QScoreWeights(
                        grounding=w.get("Grounding", self.q_weights.grounding),
                        certainty=w.get("Certainty", self.q_weights.certainty),
                        structure=w.get("Structure", self.q_weights.structure),
                        applicability=w.get("Applicability", self.q_weights.applicability),
                        coherence=w.get("Coherence", self.q_weights.coherence),
                        generativity=w.get("Generativity", self.q_weights.generativity)
                    )
            except Exception as e:
                print(f"Warning: Failed to load config: {e}")

    def get_aggregate_q_score(self, scores: dict) -> float:
        """Calculates the weighted Q-score based on system values."""
        return (
            scores.get('grounding', 0) * self.q_weights.grounding +
            scores.get('certainty', 0) * self.q_weights.certainty +
            scores.get('structure', 0) * self.q_weights.structure +
            scores.get('applicability', 0) * self.q_weights.applicability +
            scores.get('coherence', 0) * self.q_weights.coherence +
            scores.get('generativity', 0) * self.q_weights.generativity
        )

    def calculate_thales_delta(self, schmidt_x: float, schmidt_y: float) -> float:
        """Thales Diagnostic Deficit: delta = 1 - 2*sqrt(xy)."""
        h_thales = np.sqrt(schmidt_x * schmidt_y)
        delta = 1.0 - 2.0 * h_thales
        return delta

    def calculate_calm_harmony(self, authority: float, liberty: float, alpha=0.5, beta=0.5, gamma=0.2) -> float:
        """C-ALM Harmony Functional."""
        harmony = alpha * authority + beta * liberty - gamma * (authority * liberty)
        return harmony

    def verify_sovereignty_master_equation(self, scores: dict, schmidt_params: tuple) -> bool:
        """Sovereign Master Equation Check: Q subject to delta > 0."""
        q_score = self.get_aggregate_q_score(scores)
        delta = self.calculate_thales_delta(*schmidt_params)
        return q_score >= self.q_threshold and delta > self.weyl_delta_limit
