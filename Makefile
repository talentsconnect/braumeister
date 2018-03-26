.DEFAULT_GOAL = usage

.PHONY: clean

clean:
	-rm -rf build dist MANIFEST braumeister.egg-info .braumeister
	-find . -name '*.py[oc]' -exec rm {} \;

test:
	@make clean
	python3 -m unittest Braumeister/tests/*_test.py
	@make clean

usage:
	@echo ""
	@echo "make"
	@echo "  clean   Cleans up the dirt"
	@echo "  test    Execute all tests"
	@echo ""
