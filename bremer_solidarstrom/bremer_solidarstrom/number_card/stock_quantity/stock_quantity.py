import frappe
from erpnext.stock.dashboard.item_dashboard import get_data as get_stock_balance


@frappe.whitelist()
def get_data(filters: str):
	frappe.only_for("Stock User", message=True)

	filters = frappe.parse_json(filters)
	fieldname = filters.pop("fieldname")
	data = get_stock_balance(**filters)

	return {
		"value": sum(d[fieldname] for d in data) if data else 0,
		"fieldtype": "Int",
		"route": "/app/stock-balance",
	}
