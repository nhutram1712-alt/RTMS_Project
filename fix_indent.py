import re

with open('rooms/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith("if request.method =="):
        new_lines.append("    " + line)
    elif line.startswith("tenants = User.objects"):
        new_lines.append("    " + line)
    elif line.startswith("room = get_object_or_404"):
        new_lines.append("    " + line)
    elif line.startswith("invoices = Invoice.objects"):
        new_lines.append("    " + line)
    elif line.startswith("invoice = get_object_or_404"):
        new_lines.append("    " + line)
    elif line.startswith("try:"):
        new_lines.append("    " + line)
    else:
        new_lines.append(line)

with open('rooms/views.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("Fixed basic indentations")

