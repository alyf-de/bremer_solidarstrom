frappe.ui.form.on("Quotation", {
	global_margin (frm) {
		const total = frm.doc.items.reduce((acc, item) => acc + item.price_list_rate * item.qty, 0);
		const margin_factor = (total + (frm.doc.global_margin || 0) ) / total;
		for (const item of frm.doc.items) {
			frappe.model.set_value(
				item.doctype,
				item.name,
				"rate",
				Math.round(
					(item.price_list_rate * margin_factor + Number.EPSILON) * 100
				) / 100
			);
		}
	},
});
