import sys

with open('rooms/urls.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "path('', views.dashboard, name='dashboard'),",
    "path('', views.dashboard, name='dashboard'),\n    path('tenant/dashboard/', views.tenant_dashboard, name='tenant_dashboard'),"
)

with open('rooms/urls.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated urls.py")
