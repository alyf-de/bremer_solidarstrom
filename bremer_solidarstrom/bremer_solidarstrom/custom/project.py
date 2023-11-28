import frappe
from bremer_solidarstrom.bremer_solidarstrom.next_todo import get_next_todo
from erpnext.projects.doctype.project.project import Project
from frappe.query_builder.functions import Sum
from frappe.utils.data import add_years, flt, get_datetime


TODO_FIELDS = [
	(
		"custom_voranmeldung_beim_netzbetreiber_erfolgt",
		"Voranmeldung beim Netzbetreiber einreichen",
	),
	("custom_selbstbautermin_vereinbart", "Selbstbautermin vereinbaren"),
	("custom_material_bestellt", "Material bestellen"),
	(
		"custom_versicherungen_für_baueinsatz_abgeschlossen",
		"Versicherungen für Baueinsatz abschließen",
	),
	("custom_dachmontage_durchgeführt", "Dachmontage durchführen"),
	("custom_dcinstallation_durchgeführt", "DC-Installation durchführen"),
	("custom_acinstallation_durchgeführt", "AC-Installation durchführen"),
	("custom_dokumentation_übergeben", "Dokumentation übergeben"),
	(
		"custom_fertigmeldung_beim_netzbetreiber_eingereicht",
		"Fertigmeldung beim Netzbetreiber einreichen",
	),
	("custom_faktisch_in_betrieb_genommen", "Faktisch in Betrieb nehmen"),
	("custom_offiziell_in_betrieb_genommen", "Offiziell in Betrieb nehmen"),
]


class CustomProject(Project):
	def before_save(self):
		if hasattr(super(), "before_save"):
			super().before_save()
		self.custom_next_todo = get_next_todo(self, TODO_FIELDS, self.custom_next_todo)

	def update_costing(self):
		self.custom_overhead_share = get_project_overhead(self.name, self.creation)
		super().update_costing()

	def calculate_gross_margin(self):
		expense_amount = (
			flt(self.total_costing_amount)
			+ flt(self.total_purchase_cost)
			+ flt(self.get("total_consumed_material_cost", 0))
		)

		# gross margin
		self.gross_margin = flt(self.total_sales_amount) - expense_amount
		if self.total_sales_amount:
			self.per_gross_margin = (
				self.gross_margin / flt(self.total_sales_amount)
			) * 100
		else:
			self.per_gross_margin = 0

		# operating margin
		self.custom_operating_margin = self.gross_margin - self.custom_overhead_share
		if self.total_sales_amount:
			self.custom_per_operating_margin = (
				self.custom_operating_margin / flt(self.total_sales_amount)
			) * 100
		else:
			self.custom_per_operating_margin = 0


def get_project_overhead(project_name, project_start_date):
	"""Calculate the common cost attributable to the project.""" ""
	item_code = "000.000.250"
	end_date = get_datetime(project_start_date).date()
	start_date = add_years(end_date, -1)

	total_mgmt_cost, project_mgmt_cost = get_management_cost(
		project_name, item_code, start_date, end_date
	)
	total_common_cost = get_common_cost(start_date, end_date)

	return min(
		total_common_cost * project_mgmt_cost / total_mgmt_cost, total_common_cost
	)


def get_common_cost(from_date, to_date) -> float:
	"""Return the total common cost for the given period."""
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
	project_name, item_code, from_date, to_date
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
		.where((sales_order_item.item_code == item_code) & (sales_order.docstatus == 1))
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
	)

	return total_cost, project_cost
