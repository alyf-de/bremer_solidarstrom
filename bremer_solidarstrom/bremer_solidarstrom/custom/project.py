from typing import TYPE_CHECKING

from bremer_solidarstrom.next_todo import get_next_todo

if TYPE_CHECKING:
	from erpnext.projects.doctype.project.project import Project

TODO_FIELDS = [
	("custom_voranmeldung_beim_netzbetreiber_erfolgt", "Voranmeldung beim Netzbetreiber einreichen"),
	("custom_selbstbautermin_vereinbart", "Selbstbautermin vereinbaren"),
	("custom_material_bestellt", "Material bestellen"),
	("custom_versicherungen_für_baueinsatz_abgeschlossen", "Versicherungen für Baueinsatz abschließen"),
	("custom_dachmontage_durchgeführt", "Dachmontage durchführen"),
	("custom_dcinstallation_durchgeführt", "DC-Installation durchführen"),
	("custom_acinstallation_durchgeführt", "AC-Installation durchführen"),
	("custom_dokumentation_übergeben", "Dokumentation übergeben"),
	("custom_fertigmeldung_beim_netzbetreiber_eingereicht", "Fertigmeldung beim Netzbetreiber einreichen"),
	("custom_faktisch_in_betrieb_genommen", "Faktisch in Betrieb nehmen"),
	("custom_offiziell_in_betrieb_genommen", "Offiziell in Betrieb nehmen")
]


def before_save(doc: "Project", event: str):
	doc.custom_next_todo = get_next_todo(doc, TODO_FIELDS, doc.custom_next_todo)
