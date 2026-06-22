#!/bin/bash
# ============================================================
# Setup script: FBR POS Platform — Django + DRF project
# Phase 1 apps only: common, companies, users
# (pos, digital_invoicing, crm get added with `startapp` later,
#  when we actually reach those phases)
# ============================================================

set -e  # stop immediately if any command fails

PROJECT_DIR="fbr_pos_platform"

echo "==> Creating project folder: $PROJECT_DIR"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

echo "==> Creating virtual environment"
python3 -m venv venv
source venv/bin/activate

echo "==> Installing Django, DRF, python-decouple"
pip install --upgrade pip --quiet
pip install django djangorestframework python-decouple --quiet

echo "==> Starting Django project (config = settings package, not an app)"
django-admin startproject config .

echo "==> Creating Django apps: common, companies, users"
python manage.py startapp common
python manage.py startapp companies
python manage.py startapp users

echo "==> Adding serializers.py / urls.py (DRF needs these, Django doesn't create them by default)"
touch common/serializers.py
touch companies/serializers.py companies/urls.py
touch users/serializers.py users/urls.py users/managers.py

echo "==> Creating supporting folders (plain directories, NOT Django apps)"
mkdir -p static media docs
touch docs/architecture.md

echo "==> Registering apps + custom user model in settings.py"
python3 - <<'PYEOF'
import re

path = "config/settings.py"
with open(path) as f:
    content = f.read()

# Insert our apps right after the staticfiles entry, whatever quote style this
# Django version uses (single or double quotes) for the generated file.
content = re.sub(
    r"(django\.contrib\.staticfiles[\"'],)",
    r"\1\n\n    # Third-party\n    \"rest_framework\",\n\n    # Local apps\n    \"common\",\n    \"companies\",\n    \"users\",",
    content,
    count=1,
)

content += "\n\nAUTH_USER_MODEL = \"users.User\"\n"

with open(path, "w") as f:
    f.write(content)
PYEOF

echo "==> Writing .gitignore"
cat > .gitignore <<'EOF'
venv/
__pycache__/
*.pyc
.env
db.sqlite3
media/
*.log
EOF

echo "==> Writing .env / .env.example placeholders"
touch .env
cat > .env.example <<'EOF'
SECRET_KEY=replace-me
DEBUG=True
EOF

echo "==> Freezing installed packages to requirements.txt"
pip freeze > requirements.txt

echo ""
echo "============================================================"
echo " Done. Project created at: $(pwd)"
echo " Django apps created:  common, companies, users"
echo ""
echo " Next steps (run these yourself):"
echo "   cd $PROJECT_DIR"
echo "   source venv/bin/activate"
echo "   python manage.py makemigrations   # will say 'no changes' — expected, no models yet"
echo "   python manage.py migrate"
echo "============================================================"
