## Root cause

The `apply_discount` function is producing the wrong values. It returns the price plus the discount percentage: 10% produces `110.0`, and 100% produces `200.0`.

## Failing test or file

- `tests/test_pricing.py::test_discount_basic` — expected `90.0`, received `110.0`.
- `tests/test_pricing.py::test_discount_boundaries` — expected `0.0`, received `200.0`.
- Both failures come from `apply_discount` in
  - `src/pricing.py`.
  ## Suggested solution
  Update `apply_discount` to subtract the percentage from the price: return round(price \* (1 - percent / 100), 2) this is what the response is return round(price * (1 - percent / 100), 2)
