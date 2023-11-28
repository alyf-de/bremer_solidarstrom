frappe.ui.form.on("Quotation", {
	refresh(frm) {
		if (frm.doc.global_margin) {
			var total = 0;
			var i = 0;
			var items = frm.doc.items;
			for (i = 0; i < items.length; i++) {
				total += items[i].price_list_rate * items[i].qty;
			}
			var margin_factor = (total + frm.doc.global_margin) / total;
			for (i = 0; i < items.length; i++) {
				items[i].rate =
					Math.round(
						(items[i].price_list_rate * margin_factor + Number.EPSILON) * 100
					) / 100;
				items[i].amount = items[i].rate * items[i].qty;
			}
			frm.doc.total_qty =
				frm.doc.total =
				frm.doc.base_total =
				frm.doc.net_total =
				frm.doc.base_net_total =
					0.0;

			$.each(items || [], function (i, item) {
				frm.doc.total += item.amount;
				frm.doc.total_qty += item.qty;
				frm.doc.base_total += item.base_amount;
				frm.doc.net_total += item.net_amount;
				frm.doc.base_net_total += item.base_net_amount;
			});

			frappe.model.round_floats_in(frm.doc, [
				"total",
				"base_total",
				"net_total",
				"base_net_total",
			]);
		}
	},
});
