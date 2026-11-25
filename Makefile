.PHONY: install test validate site brief diagrams labs
install:
	pip install -e ".[dev]"
test:
	python -m pytest -q
validate:
	cloudequiv validate
site:
	cloudequiv site --out site
brief:
	cloudequiv brief --from aws --to oci
diagrams:
	cloudequiv diagrams
labs:
	./labs/run_all.sh
