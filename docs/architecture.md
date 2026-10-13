# Architecture

## No Core Edits
The app uses hooks, custom fields, Python services, whitelisted methods, and DocType JavaScript.

## Document Ownership
- **Stock Entry:** physical stock movement
- **Sales Order:** commercial consignment commitment
- **Sales Invoice:** accounting sale / receivable
- **Material Request:** optional upstream request

## Idempotency
Before creating a Sales Order the service checks:
1. the Stock Entry's linked Sales Order field;
2. any non-cancelled Sales Order already referencing the Stock Entry.

## Service Layer
Both the submit event and recovery API call the same `ensure_outlet_sales_order()` service.

## Draft by Default
A generated Sales Order remains Draft unless site configuration explicitly enables auto-submit.
