import numpy as np

class GovernorKernelEKRLS:
    def __init__(self, lambda_reg=0.1, sigma=1.0):
        self.Q = None # Inverse tracking matrix
        self.a = None # Inference weight vector
        self.dictionary = [] # Reference logic states store
        self.lambda_reg = lambda_reg
        self.sigma = sigma

    def _compute_kernel_vector(self, current_reasoning_step):
        """
        Compute the kernel vector (RBF kernel) for the current step against the dictionary.
        """
        if not self.dictionary:
            return np.array([])

        # Simple RBF Kernel: k(x, y) = exp(-||x-y||^2 / (2*sigma^2))
        # Assuming current_reasoning_step and dictionary items are numpy arrays
        diffs = np.array([np.linalg.norm(current_reasoning_step - d)**2 for d in self.dictionary])
        return np.exp(-diffs / (2 * self.sigma**2))

    def update_integrity(self, current_reasoning_step, feedback):
        """
        Update reasoning integrity and detect drift (EKRLS).
        """
        h = self._compute_kernel_vector(current_reasoning_step)

        if self.Q is None:
            self.Q = np.array([[1.0 / (self.lambda_reg + 1.0)]])
            self.a = np.array([feedback / (self.lambda_reg + 1.0)])
            self.dictionary.append(current_reasoning_step)
            return 1.0 # Initial integrity

        z = self.Q @ h
        r = self.lambda_reg + 1.0 - h.T @ z

        # Update state matrix Q and error e
        prediction = h.T @ self.a
        e = feedback - prediction

        # Expand Q matrix
        z_col = z[:, np.newaxis]
        top_left = self.Q * r + np.outer(z, z)
        new_Q = (1.0/r) * np.block([
            [top_left, -z_col],
            [-z[np.newaxis, :], 1.0]
        ])

        self.Q = new_Q
        self.dictionary.append(current_reasoning_step)

        # Update inference weights
        self.a = np.append(self.a - (z/r)*e, e/r)

        # Integrity score (1 - normalized error)
        integrity = 1.0 - abs(e) / (abs(feedback) + 1e-9)
        return max(0.0, integrity)
