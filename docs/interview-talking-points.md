# Interview Talking Points

- A custom app is preferable to isolated Server Scripts when a solution needs source control, repeatable installation, tests, review, and promotion across environments.
- Version-controlled custom fields prevent configuration drift.
- Idempotency prevents duplicate Sales Orders if hooks or recovery actions are retried.
- Valuation rate is intentionally not used as selling price.
- Draft Sales Order is the safer reusable default; auto-submit is configurable.
- Next enhancements: exposure report, issued-vs-sold report, return reconciliation, retry log, background jobs, integration tests.
