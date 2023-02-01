import datetime

def generate_order_number(pk):
    current_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M")
    order_no = current_datetime + str(pk)
    return order_no

def order_total_by_vendor(order,vendor):
    subtotal,total_tax=0,0
    tax_dict = {}

    if order.total_data:
        vendor_data = order.total_data.get(str(vendor.id))  #type:ignore

        # calculate tax_dict and subtotal
        subtotal = 0
        tax_dict = {}
        for sub_total,tax in vendor_data.items():
            subtotal += float(sub_total)
            tax_dict.update(tax)

        # calculate total tax
        total_tax = 0
        for tax in tax_dict:
            for value in tax_dict[tax]:
                total_tax += tax_dict[tax][value]

    context = {
        'grand_total':round(subtotal+total_tax,2),
        'subtotal':round(subtotal,2),
        'total_tax':round(total_tax,2),
        'tax_dict':tax_dict,
    }
    return context
