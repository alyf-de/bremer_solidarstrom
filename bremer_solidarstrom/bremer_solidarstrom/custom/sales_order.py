import frappe


def before_save(doc, event):
	"""Custom before save hook for sales orders.

	:param doc: The sales order document.
	:param event: The event that triggered this method.
	"""
	auto_create_project(doc)


def auto_create_project(sales_order) -> None:
	"""Automatically create a project for the given sales order."""
	if sales_order.project or not sales_order.custom_create_project:
		return

	sales_order.project = create_project(sales_order.customer_name, sales_order.customer)
	sales_order.custom_create_project = 0


def create_project(project_name: str, customer: str) -> str:
	"""Create a project with the given name, linked to the customer."""
	project = frappe.new_doc("Project")
	project.project_name = project_name
	project.customer = customer
	project.insert()

	return project.name
