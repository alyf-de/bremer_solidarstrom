frappe.ui.form.on("Quotation", {
	global_margin(frm) {
		frm.trigger("update_item_rates");
	},
	custom_profit_margin(frm) {
		frm.trigger("update_item_rates");
	},
	update_item_rates(frm) {
		const total = frm.doc.items.reduce(
			(acc, item) =>
				acc + (item.valuation_rate || item.base_price_list_rate) * item.qty,
			0
		);

		const margin_factor = (total + (frm.doc.global_margin || 0)) / total;
		const profit_factor = 1 + (frm.doc.custom_profit_margin || 0) / 100;
		const handling_factor = 1.1;

		for (const item of frm.doc.items) {
			let base_rate = item.valuation_rate || item.base_price_list_rate;
			frappe.model.set_value(
				item.doctype,
				item.name,
				"rate",
				Math.round(
					(base_rate *
						frm.doc.conversion_rate *
						handling_factor *
						margin_factor *
						profit_factor +
						Number.EPSILON) *
						100
				) / 100
			);
		}
	},
	custom_fetch_global_margin(frm) {
		if (frm.doc.docstatus !== 0) {
			frappe.throw(__("Quotation must be in draft state"));
		}

		const ITEM_CODE = "000.000.250";
		const management_cost = frm.doc.items
			.filter((item) => item.item_code === ITEM_CODE)
			.reduce((acc, item) => acc + item.price_list_rate * item.qty, 0);
		if (management_cost === 0) {
			frappe.throw("No item with code 000.000.250 found");
		}

		frappe
			.xcall(
				"bremer_solidarstrom.bremer_solidarstrom.custom.quotation.get_global_margin",
				{
					to_date: frm.doc.transaction_date,
					quotation_management_cost: management_cost,
				}
			)
			.then((res) => {
				frm.set_value("global_margin", res);
			});
	},
});
