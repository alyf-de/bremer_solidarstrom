import frappe
from frappe.utils.data import add_years, flt, get_datetime
from bremer_solidarstrom.bremer_solidarstrom.overhead_costs import get_overhead_cost, get_management_cost


@frappe.whitelist(methods=["POST"])
def get_global_margin(to_date, quotation_management_cost):
	"""Return the global margin for the year before to_date."""
	to_date = get_datetime(to_date).date()
	from_date = add_years(to_date, -1)

	overhead_cost = get_overhead_cost(from_date, to_date)
	total_management_cost = get_management_cost(from_date, to_date)[0]

	return min(overhead_cost * flt(quotation_management_cost) / total_management_cost, overhead_cost)
