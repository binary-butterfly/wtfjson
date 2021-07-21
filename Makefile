.PHONY: all tox open-coverage clean clean-all

# Default target
all: tox


# Test suite
# ----------
tox:
	tox

# Open HTML coverage report in browser
open-coverage:
	$(or $(BROWSER),firefox) ./reports/coverage_html/index.html


# Cleanup
# -------
clean:
	rm -rf .coverage reports

clean-all: clean
	rm -rf .tox .eggs venv
