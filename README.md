# Mimie's Closet

Django catalog + WhatsApp ordering site. No cart checkout/payment — the bag
just builds a pre-filled WhatsApp message sent to the shop's number.

## Structure

```
config/settings/   base.py, dev.py, prod.py (python-decouple driven)
apps/catalog/       Category, Product models + shop views
apps/cart/           session cart + WhatsApp link builder
apps/core/           home/about pages, site-wide context processor
templates/, static/
tests/               pytest-django suite
passenger_wsgi.py   cPanel/Passenger entrypoint
```

## Local setup (Termux/mobile friendly)

```bash
pip install -r requirements.txt --break-system-packages
cp .env.example .env          # edit SECRET_KEY, WHATSAPP_ORDER_NUMBER
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

`manage.py` defaults to `config.settings.dev` — no env var needed locally.

## Adding products

Everything is managed through `/admin/`: create Categories first (Men,
Women, Kids, Accessories), then Products. Leave the image blank to fall
back to the placeholder graphic until real photos are ready.

## Running tests

```bash
pytest
```

Covers: slug generation, category/product URLs, placeholder image
fallback, catalog views (in-stock filtering, category scoping), cart add/
update/remove/total logic, and the WhatsApp link generation.

## Deploying to cPanel/Passenger

Same pattern as Shato Sports Bar / Samwa Bakery:

1. Upload the project (minus `db.sqlite3`, `.env`, `__pycache__`) to the
   app's cPanel "Setup Python App" directory.
2. In cPanel's Python App interface, set the app's entry point to
   `passenger_wsgi.py` (already provided at the project root).
3. Create `logs/` if it isn't present — Passenger will crash on startup
   without a writable log path (`base.py` LOGGING points here).
4. Set environment variables in cPanel's Python App UI or a `.env` file:
   `SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`,
   `WHATSAPP_ORDER_NUMBER`. `DJANGO_SETTINGS_MODULE` is already forced to
   `config.settings.prod` inside `passenger_wsgi.py`.
5. `pip install -r requirements.txt` inside the app's virtualenv.
6. `python manage.py migrate`
7. `python manage.py collectstatic --noinput` — WhiteNoise serves these;
   if the domain is an addon/subdomain, double check the media `re_path`
   pattern the way it was fixed for KurudzArt if product images 404.
8. Restart the app (touch `tmp/restart.txt` or use the cPanel UI).

## Notes / things to fill in before launch

- `WHATSAPP_ORDER_NUMBER` in `.env` is a placeholder — set the real
  shop number in international format, digits only.
- `templates/core/about.html` has placeholder copy.
- Category `order` field controls display order on the shop filter —
  set explicitly rather than relying on insertion order.
