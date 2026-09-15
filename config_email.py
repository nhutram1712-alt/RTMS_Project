with open('rtms/settings.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'EMAIL_BACKEND' not in content:
    content += "\n\n# Configure email backend for development\nEMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'\n"
    with open('rtms/settings.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added EMAIL_BACKEND to settings.py")
else:
    print("EMAIL_BACKEND already configured")
