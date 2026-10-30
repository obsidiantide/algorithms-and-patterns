# Algorithms, Data Structures & Python Patterns 🚀

[![CI](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A curated collection of clean, well-tested implementations of core computer science algorithms, data structures, design patterns, and production backend utilities in modern Python.

## 📦 Directory Structure

```text
algorithms/
  ├── searching/      # Binary search, bounds, interpolation
  ├── sorting/        # QuickSort 3-way, MergeSort, HeapSort
  ├── graphs/         # Dijkstra, Kruskal (MST), BFS, DFS, Topological sort
  └── dynamic/        # Knapsack, LCS, Coin change
structures/
  ├── lru_cache.py    # O(1) Doubly Linked List cache
  ├── ring_buffer.py  # Fixed-capacity FIFO circular buffer
  ├── trie.py         # Prefix tree with autocomplete
  ├── heap.py         # Binary min/max heap
  └── disjoint_set.py # Disjoint Set Union (Union-Find) with rank & path compression
patterns/
  ├── behavioral/     # Strategy, Observer, Command
  ├── creational/     # Factory, Builder, Singleton
  └── structural/     # Decorator, Adapter, Facade
utils/
  ├── retry.py        # Exponential backoff decorator
  └── rate_limiter.py # Token Bucket rate limiter
tests/
  └── ...             # Comprehensive pytest test suite
```

## ⏱️ Complexity Matrix

| Algorithm / Structure | Time Complexity (Avg) | Time Complexity (Worst) | Space Complexity |
| :--- | :--- | :--- | :--- |
| **Binary Search** | $O(\log n)$ | $O(\log n)$ | $O(1)$ |
| **QuickSort (3-Way)** | $O(n \log n)$ | $O(n^2)$ | $O(\log n)$ |
| **MergeSort** | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ |
| **HeapSort** | $O(n \log n)$ | $O(n \log n)$ | $O(1)$ |
| **LRU Cache** | $O(1)$ | $O(1)$ | $O(n)$ |
| **Ring Buffer (Push/Pop)** | $O(1)$ | $O(1)$ | $O(n)$ |
| **Trie Lookup** | $O(k)$ | $O(k)$ | $O(n \cdot k)$ |
| **Binary Heap (Push/Pop)** | $O(\log n)$ | $O(\log n)$ | $O(n)$ |
| **Disjoint Set (Find/Union)** | $O(\alpha(n))$ | $O(\alpha(n))$ | $O(n)$ |
| **Topological Sort** | $O(V + E)$ | $O(V + E)$ | $O(V + E)$ |
| **Dijkstra's Algorithm** | $O((V + E) \log V)$ | $O((V + E) \log V)$ | $O(V)$ |
| **Kruskal's Algorithm (MST)** | $O(E \log E)$ | $O(E \log E)$ | $O(V + E)$ |
| **BFS / DFS Traversal** | $O(V + E)$ | $O(V + E)$ | $O(V)$ |
| **0-1 Knapsack** | $O(n \cdot W)$ | $O(n \cdot W)$ | $O(W)$ |
| **Coin Change (Min / Ways)** | $O(n \cdot A)$ | $O(n \cdot A)$ | $O(A)$ |
| **Longest Common Subsequence** | $O(m \cdot n)$ | $O(m \cdot n)$ | $O(\min(m, n))$ |

## 🧪 Testing

Run tests with `pytest`:
```bash
pytest tests/ -v
```
