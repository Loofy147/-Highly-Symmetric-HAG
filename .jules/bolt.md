## 2024-03-28 - [Optimization of Mathematical Hot Loops in Python]
**Learning:** In Python, nested dictionary or list lookups like `arc_s[cur][pa[sigma[cur]][c]]` inside a high-frequency loop (millions of calls) are extremely expensive due to interpreter overhead. Pre-calculating a 3D transition table `trans[color][permutation][node]` to consolidate these lookups into a single `trans[c][sigma[cur]][cur]` access yields measurable performance gains.
**Action:** Always identify "hot" nested indexing patterns in core engines and attempt to hoist or pre-calculate the transition mapping into a single-level or flattened lookup table.

## 2024-03-28 - [Closed-form vs Search-based Mathematical Discovery]
**Learning:** For symmetric graph decompositions (Hamiltonian cycles), while Simulated Annealing (SA) is a robust general solver, it scales poorly with domain size. Identifying the "Canonical Spike" pattern allowed for an O(m) deterministic construction that replaces SA search entirely for the odd m domain.
**Action:** Before optimizing a search algorithm, investigate if the problem domain supports a deterministic closed-form construction, especially when symmetry (like the Spike pattern) is present.
