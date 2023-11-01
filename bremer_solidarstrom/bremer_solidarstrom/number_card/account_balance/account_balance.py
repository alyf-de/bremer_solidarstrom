from datetime import datetime

import frappe
from erpnext.accounts.utils import get_balance_on


@frappe.whitelist()
def get_data(filters: str):
	frappe.only_for("Accounts User", message=True)

	filters = frappe.parse_json(filters)

	party_type = filters.get("party_type", None)
	party = filters.get("party", None)
	account = filters.get("account", None)
	if not account:
		return {
			"value": 0.0,
			"fieldtype": "Currency",
			"route": "/app/query-report/General Ledger",
		}

	balance = get_balance_on(
		account=filters.get("account"),
		date=datetime.now().date(),
		party_type=party_type,
		party=party
	)

	return {
		"value": balance,
		"fieldtype": "Currency",
		"route": "/app/query-report/General Ledger",
		"route_options": {
			"account": [account],
		}
	}
