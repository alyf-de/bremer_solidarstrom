import frappe
from frappe.query_builder.functions import Sum

# This item code is used to identify the management cost in the sales order.
ITEM_CODE = "000.000.250"


def get_overhead_cost(from_date, to_date) -> float:
	"""Return the total overhead cost for the given period."""
	gl_entry = frappe.qb.DocType("GL Entry")
	account = frappe.qb.DocType("Account")

	base_query = (
		frappe.qb.from_(gl_entry)
		.left_join(account)
		.on(gl_entry.account == account.name)
		.select(Sum(gl_entry.debit - gl_entry.credit))
		.where(
			(account.root_type == "Expense")
			& gl_entry.posting_date.between(from_date, to_date)
			& gl_entry.project.isnull()
		)
	)

	return base_query.run()[0][0] or 0.0


def get_management_cost(
	from_date, to_date, project_name = None
) -> tuple[float, float]:
	"""Return the total management cost and the project management cost for the given period."""
	sales_order = frappe.qb.DocType("Sales Order")
	sales_order_item = frappe.qb.DocType("Sales Order Item")
	base_query = (
		frappe.qb.from_(sales_order_item)
		.left_join(sales_order)
		.on(
			(sales_order_item.parent == sales_order.name)
			& (sales_order_item.parenttype == "Sales Order")
		)
		.select(Sum(sales_order_item.base_net_amount))
		.where((sales_order_item.item_code == ITEM_CODE) & (sales_order.docstatus == 1))
	)

	total_cost = (
		base_query.where(
			sales_order.project.notnull()
			& sales_order.transaction_date.between(from_date, to_date)
		).run()[0][0]
		or 0.0
	)
	project_cost = (
		base_query.where(sales_order.project == project_name).run()[0][0] or 0.0
	) if project_name else 0.0

	return total_cost, project_cost
