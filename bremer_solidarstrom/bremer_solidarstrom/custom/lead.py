from typing import TYPE_CHECKING

from bremer_solidarstrom.bremer_solidarstrom.next_todo import get_next_todo

if TYPE_CHECKING:
	from erpnext.crm.doctype.lead.lead import Lead

TODO_FIELDS = [
	("custom_infos_erhalten", "Informationen anfordern"),
	("custom_grobplanung_durchgeführt", "Grobplanung durchführen"),
	("custom_vororttermin_angefragt", "Vor-Ort-Termin anfragen"),
	("custom_vororttermin_durchgeführt", "Vor-Ort-Termin durchführen"),
	("custom_feinplanung_durchgeführt", "Feinplanung durchführen"),
]


def before_save(doc: "Lead", event: str):
	doc.custom_next_todo = get_next_todo(doc, TODO_FIELDS, doc.custom_next_todo)
