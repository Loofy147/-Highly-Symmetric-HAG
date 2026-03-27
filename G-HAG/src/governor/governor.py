import numpy as np
import json
import os
from src.core.values import SystemValues

class HolographicGovernor:
    """
    محرك Governor 2.1 (HAG-OS Build 4.0 (Legacy)) لتتبع نزاهة الاستدلال.
    HolographicGovernor: Tracks reasoning integrity and prevents model drift via EKRLS.
    """
    def __init__(self, config_path="configs/bayesian_weights.json", **kwargs):
        self.values = SystemValues(config_path)
        self.lam = kwargs.get('lambda_forget', 0.99)
        self.sigma = kwargs.get('sigma_kernel', 1.0)

        # Load specific EKRLS params from file if not overridden by kwargs
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    ekrls = config.get("EKRLS", {})
                    if 'sigma_kernel' not in kwargs:
                        self.sigma = ekrls.get("sigma", self.sigma)
            except:
                pass

        # ⚡ Storage Management (Bolt)
        # We pre-allocate space for the dictionary and matrices to avoid O(N^2) reallocations.
        self.capacity = 128
        self.num_items = 0
        self.dictionary_array = None
        self.dictionary_norms = None # Cached squared norms for faster distance computation
        self.Q = None
        self.alpha = None

        # Use explicit threshold if provided, else use system values
        self.threshold = kwargs.get('threshold', self.values.q_threshold)

    @property
    def dictionary(self):
        """Maintains backward compatibility for tests."""
        if self.dictionary_array is None:
            return []
        return self.dictionary_array[:self.num_items]

    def _ensure_capacity(self, dim=None):
        if self.dictionary_array is None:
            if dim is None: return
            self.dictionary_array = np.zeros((self.capacity, dim))
            self.dictionary_norms = np.zeros(self.capacity)
            self.Q = np.zeros((self.capacity, self.capacity))
            self.alpha = np.zeros(self.capacity)
            return

        if self.num_items >= self.capacity:
            old_capacity = self.capacity
            self.capacity *= 2

            # Grow dictionary
            new_dict = np.zeros((self.capacity, self.dictionary_array.shape[1]))
            new_dict[:old_capacity] = self.dictionary_array
            self.dictionary_array = new_dict

            # Grow norms
            new_norms = np.zeros(self.capacity)
            new_norms[:old_capacity] = self.dictionary_norms
            self.dictionary_norms = new_norms

            # Grow Q
            new_Q = np.zeros((self.capacity, self.capacity))
            new_Q[:old_capacity, :old_capacity] = self.Q
            self.Q = new_Q

            # Grow alpha
            new_alpha = np.zeros(self.capacity)
            new_alpha[:old_capacity] = self.alpha
            self.alpha = new_alpha

    def _compute_kernel_vector(self, reasoning_vector):
        if self.num_items == 0: return np.array([])

        # ⚡ Optimization: Squared norm expansion (Bolt)
        # ||A - B||^2 = ||A||^2 + ||B||^2 - 2AB^T
        # This replaces: np.sum((np.array(self.dictionary) - reasoning_vector)**2, axis=1)
        # which is O(N * dim). This is also O(N * dim) but uses optimized GEMV and cached norms.

        vec_norm = np.sum(reasoning_vector**2)
        dict_part = self.dictionary_array[:self.num_items]

        # We use a dot product which is highly optimized in BLAS
        dot_product = dict_part @ reasoning_vector

        diffs = self.dictionary_norms[:self.num_items] + vec_norm - 2 * dot_product
        # Handle potential numerical precision issues where diffs < 0
        diffs = np.maximum(diffs, 0)

        return np.exp(-diffs / (2 * self.sigma**2))

    def step(self, reasoning_vector, feedback_signal):
        self._ensure_capacity(len(reasoning_vector))
        h = self._compute_kernel_vector(reasoning_vector)

        if self.num_items == 0:
            self.Q[0, 0] = 1.0 / (self.lam + 1.0)
            self.alpha[0] = feedback_signal / (self.lam + 1.0)
            self.dictionary_array[0] = reasoning_vector
            self.dictionary_norms[0] = np.sum(reasoning_vector**2)
            self.num_items = 1
            return True

        # Extract current active parts
        Q_m = self.Q[:self.num_items, :self.num_items]
        alpha_m = self.alpha[:self.num_items]

        z = Q_m @ h
        r = self.lam + 1.0 - h.T @ z
        prediction = h.T @ alpha_m
        prediction_error = feedback_signal - prediction

        if abs(prediction_error) > (1.0 - self.threshold):
            self._trigger_metacognitive_reflection(prediction_error)
            return False

        # ⚡ Fix: Correct dimension expansion for EKRLS (Bolt) - Optimized via slice updates
        m = self.num_items

        # Update current block
        # Q_m is updated in-place via the pre-allocated slice
        Q_m += np.outer(z, z) / r

        # New row and column
        self.Q[:m, m] = -z / r
        self.Q[m, :m] = -z / r
        self.Q[m, m] = 1.0 / r

        # Update alpha
        alpha_m -= (z / r) * prediction_error
        self.alpha[m] = prediction_error / r

        # Add to dictionary and norms
        self.dictionary_array[m] = reasoning_vector
        self.dictionary_norms[m] = np.sum(reasoning_vector**2)

        self.num_items += 1
        return True

    def _trigger_metacognitive_reflection(self, error):
        print(f"ALERT: Reasoning Drift Detected (Error: {error:.4f}). Initiating Suffix Smoothing Protocol...")
