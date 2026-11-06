# Roadmap

Backlog grouped by domain. Mark items `- [x]` when done.

## A. Core features (new algorithms and structures)
- [x] Knuth-Morris-Pratt substring search (`algorithms/strings/kmp.py`)
- [ ] Segment tree with range-sum and point update
- [ ] A* pathfinding on a grid
- [ ] Sliding-window rate limiter in `utils/`

## B. Test coverage
- [ ] Property-based comparison tests for sorting against `sorted()`
- [ ] Concurrency tests for `RateLimiter` and `CircuitBreaker`

## C. Architecture and refactoring
- [ ] Add `__init__.py` packages and a shared `Graph` type alias for graph algorithms
- [ ] Share edge-list validation between Bellman-Ford and Floyd-Warshall

## D. Performance and polish
- [ ] Add type-checking (mypy) config and fix reported issues
- [ ] Benchmark script comparing sorting implementations
- [ ] CI workflow running pytest on Python 3.10-3.13
