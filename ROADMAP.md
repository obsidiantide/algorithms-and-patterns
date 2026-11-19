# Roadmap

Backlog grouped by domain. Mark items `- [x]` when done.

## A. Core features (new algorithms and structures)
- [x] Knuth-Morris-Pratt substring search (`algorithms/strings/kmp.py`)
- [x] Segment tree with range-sum and point update
- [x] A* pathfinding on a grid
- [x] Sliding-window rate limiter in `utils/sliding_window.py`

## B. Test coverage
- [x] Property-based comparison tests for sorting against `sorted()`
- [x] Concurrency tests for `CircuitBreaker` and `TokenBucketRateLimiter`

## C. Architecture and refactoring
- [ ] Add `__init__.py` packages and a shared `Graph` type alias for graph algorithms
- [x] Share edge-list validation between Bellman-Ford and Floyd-Warshall

## D. Performance and polish
- [x] Add type-checking (mypy) config and fix reported issues
- [ ] Benchmark script comparing sorting implementations
- [x] CI workflow running pytest and mypy on Python 3.10-3.13
