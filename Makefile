.PHONY: check
check:
	python3 tools/check.py
	sh tools/test_hook.sh
