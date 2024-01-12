from bremer_solidarstrom.bremer_solidarstrom.overhead_costs import get_overhead_cost, get_management_cost
from bremer_solidarstrom.bremer_solidarstrom.next_todo import get_next_todo
from erpnext.projects.doctype.project.project import Project
from frappe.utils.data import add_years, flt, get_datetime


TODO_FIELDS = [
	(
		"custom_voranmeldung_beim_netzbetreiber_erfolgt",
		"Voranmeldung beim Netzbetreiber einreichen",
	),
	("custom_selbstbautermin_vereinbart", "Selbstbautermin vereinbaren"),
	("custom_material_bestellt", "Material bestellen"),
	("custom_gerüst_bestellt", "Gerüst bestellen"),
	(
		"custom_versicherungen_für_baueinsatz_abgeschlossen",
		"Versicherungen für Baueinsatz abschließen",
	),
	("custom_modulmontage_durchgeführt", "Modulmontage durchführen"),
	("custom_dcinstallation_durchgeführt", "DC-Installation durchführen"),
	("custom_acinstallation_durchgeführt", "AC-Installation durchführen"),
	("custom_erdung_fertig", "Erdung fertigsellen"),
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
		self.custom_next_todo = get_next_todo(self, TODO_FIELDS, self.custom_next_todo, ["Completed", "Cancelled"])

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
	end_date = get_datetime(project_start_date).date()
	start_date = add_years(end_date, -1)

	total_mgmt_cost, project_mgmt_cost = get_management_cost(
		start_date, end_date, project_name
	)
	total_common_cost = get_overhead_cost(start_date, end_date)

	return min(
		total_common_cost * project_mgmt_cost / total_mgmt_cost, total_common_cost
	)
