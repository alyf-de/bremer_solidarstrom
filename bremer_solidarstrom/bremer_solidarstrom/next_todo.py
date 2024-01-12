from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from frappe.model.document import Document


def get_next_todo(doc: "Document", todo_fields: list[str], current_todo: str, complete_docstatus: list[str]):
	"""Returns the next todo for a given document.

	Args:
		doc (Document): The document to get the next todo for.
		todo_fields (list[str]): A list of tuples containing the todo fields and the todo text.
		current_todo (str): The current todo.
		complete_docstatus (list[str]): A list of docstatus values that are considered complete.
	"""
	if current_todo and current_todo not in [todo for field, todo in todo_fields]:
		return current_todo

	if doc.get("status") in complete_docstatus:
		return None

	next_todo = None
	for field, todo in reversed(todo_fields):
		if not doc.get(field):
			next_todo = todo
		else:
			break

	return next_todo
