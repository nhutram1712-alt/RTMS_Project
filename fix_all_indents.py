import sys

with open('rooms/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
in_def = False
for i, line in enumerate(lines):
    if line.startswith("def "):
        in_def = True
        new_lines.append(line)
    elif line.startswith("class ") or line.startswith("@"):
        in_def = False
        new_lines.append(line)
    elif in_def and len(line) > 1 and not line.startswith(" ") and not line.startswith("\t") and not line.startswith("#"):
        new_lines.append("    " + line)
    else:
        new_lines.append(line)

with open('rooms/views.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("Fixed indentation")

