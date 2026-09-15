import re

with open('templates/rooms/room_form.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace {{ post_data.X|default:room.X|default:'' }} or default:0
content = re.sub(
    r'\{\{\s*post_data\.(\w+)\|default:room\.\1\|default:(.*?)\s*\}\}',
    r'{% if post_data %}{{ post_data.\1 }}{% elif room %}{{ room.\1 }}{% endif %}',
    content
)

# Also fix the select option for status:
# {% if post_data.status == val or room.status == val %} 
# If room is None, room.status will throw.
content = re.sub(
    r'\{\%\s*if\s*post_data\.status\s*==\s*val\s*or\s*room\.status\s*==\s*val\s*\%\}',
    r'{% if post_data.status == val or room and room.status == val %}',
    content
)

# Fix selected_amenities check if room is None? 
# Wait, room.amenities might be evaluated.
# Let's check amenities.
content = re.sub(
    r'room\.amenities',
    r'(room and room.amenities)',
    content
)

with open('templates/rooms/room_form.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Template fixed!')
