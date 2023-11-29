# Copyright (c) 2023, ALYF GmbH and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.query_builder.functions import Sum, Round


def execute(filters=None):
	return get_columns(), get_data(filters.get("company"), filters.get("warehouse"))


def get_columns():
	return [
		{
			"fieldname": "item_group",
			"label": _("Item Group"),
			"fieldtype": "Link",
			"options": "Item Group",
			"width": 200,
		},
		{
			"fieldname": "stock_uom",
			"label": _("Stock UOM"),
			"fieldtype": "Link",
			"options": "UOM",
			"width": 200,
		},
		{
			"fieldname": "qty",
			"label": _("Quantity"),
			"fieldtype": "Float",
			"width": 120,
			"precision": 0,
		},
		{
			"fieldname": "value",
			"label": _("Value"),
			"fieldtype": "Currency",
			"width": 120,
		},
	]


def get_data(company, warehouse):
	bin_table = frappe.qb.DocType("Bin")
	item_table = frappe.qb.DocType("Item")
	item_group_table = frappe.qb.DocType("Item Group")
	warehouse_table = frappe.qb.DocType("Warehouse")

	value = Round(Sum(bin_table.valuation_rate * bin_table.actual_qty), 2)

	query = (
		frappe.qb.from_(bin_table)
		.select(
			item_table.item_group,
			bin_table.stock_uom,
			Round(Sum(bin_table.actual_qty), 2),
			value,
		)
		.left_join(item_table)
		.on(bin_table.item_code == item_table.name)
		.left_join(item_group_table)
		.on(item_table.item_group == item_group_table.name)
		.left_join(warehouse_table)
		.on(bin_table.warehouse == warehouse_table.name)
		.where(
			(warehouse_table.company == company)
			& (bin_table.actual_qty > 0)
		)
		.groupby(item_table.item_group, bin_table.stock_uom)
		.orderby(value, order=frappe.qb.desc)
	)

	if warehouse:
		query = query.where(bin_table.warehouse == warehouse)

	return query.run()
