import pandas as pd
import torch
import numpy as np
import os
import glob

class GeneralDataLoader:
    """
    Unified loader for HAG Build 4.0 (Unified) datasets (Physics, Finance, Legal).
    """
    def __init__(self, input_dim=16):
        self.input_dim = input_dim

    def load_domain_data(self, domain="physics"):
        """
        Loads features from a specific domain.
        """
        if domain == "physics":
            return self._load_physics()
        elif domain == "finance":
            return self._load_finance()
        elif domain == "legal":
            return self._load_legal()
        return None, None

    def _load_physics(self):
        # Combined logic from previous implementation
        all_x, all_y = [], []

        # Particles
        p_path = "./data/physics_particles.csv"
        if os.path.exists(p_path):
            df = pd.read_csv(p_path)
            df['mass'] = pd.to_numeric(df['mass'], errors='coerce')
            df = df.dropna(subset=['mass'])
            x, y = self._preprocess(df[['mass']].values, df[['mass']].values)
            all_x.append(x); all_y.append(y)

        # CERN
        c_path = "./data/cern/dielectron.csv"
        if os.path.exists(c_path):
            df = pd.read_csv(c_path)
            cols = ['E1', 'pt1', 'eta1', 'phi1', 'E2', 'pt2', 'eta2', 'phi2']
            x, y = self._preprocess(df[cols].values, df[['M']].values)
            all_x.append(x); all_y.append(y)

        if not all_x: return None, None
        return torch.cat(all_x, dim=0), torch.cat(all_y, dim=0)

    def _load_finance(self):
        # Huge Stock Market Dataset: Use a few ETF files for variety
        etf_files = glob.glob("./data/finance/Data/ETFs/*.us.txt")[:10]
        all_x, all_y = [], []

        for f in etf_files:
            df = pd.read_csv(f)
            # Use Open, High, Low, Volume to predict Close
            cols = ['Open', 'High', 'Low', 'Volume']
            x, y = self._preprocess(df[cols].values, df[['Close']].values)
            all_x.append(x); all_y.append(y)

        if not all_x: return None, None
        return torch.cat(all_x, dim=0), torch.cat(all_y, dim=0)

    def _load_legal(self):
        # Legal Text Classification
        path = "./data/legal/legal_text_classification.csv"
        if not os.path.exists(path): return None, None
        df = pd.read_csv(path, nrows=5000)

        # For simplicity, we convert text length and unique word count to numeric features
        # In Build 2.2 we would use an LLM embedding layer here.
        df['text_len'] = df['case_text'].str.len()
        df['word_count'] = df['case_text'].str.split().str.len()
        df = df.dropna(subset=['text_len', 'word_count'])

        features = df[['text_len', 'word_count']].values
        # Predict outcome (numeric mapping)
        outcomes = pd.get_dummies(df['case_outcome']).values

        return self._preprocess(features, outcomes[:, :1]) # Return first outcome category

    def _preprocess(self, features, targets):
        # Normalize
        features = (features - features.mean(axis=0)) / (features.std(axis=0) + 1e-6)
        targets = (targets - targets.mean(axis=0)) / (targets.std(axis=0) + 1e-6)

        num_samples = features.shape[0]
        padded_x = np.zeros((num_samples, self.input_dim))
        cols = min(features.shape[1], self.input_dim)
        padded_x[:, :cols] = features[:, :cols]

        return torch.tensor(padded_x, dtype=torch.float32), torch.tensor(targets, dtype=torch.float32)
