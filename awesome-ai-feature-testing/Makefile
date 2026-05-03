.PHONY: refresh check-links lint csv-shape site

refresh:
	python scripts/refresh_index.py

check-links:
	python scripts/check_links.py

lint: check-links csv-shape

csv-shape:
	@python -c "import csv, sys; required={'tool_id','name','url','categories','license','description'}; \
	rows=list(csv.DictReader(open('data/tools.csv', encoding='utf-8'))); \
	missing=required-set(rows[0].keys()); \
	sys.exit(1) if missing else print('CSV shape OK.')"

site:
	mkdocs serve
