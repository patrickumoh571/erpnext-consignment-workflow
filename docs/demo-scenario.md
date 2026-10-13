# Demo Scenario

Create:
- Customer `DEMO OUTLET - 001`
- Item `DEMO-ITEM-001`
- source and outlet warehouses
- a selling price list
- an Item Price

Create a Material Transfer Stock Entry, tick **Issue to Outlet**, select the outlet customer, and submit.

Expected result:
1. app validates the issue;
2. checks for duplicates;
3. resolves selling price;
4. creates one Sales Order;
5. links the Sales Order back to the Stock Entry.
