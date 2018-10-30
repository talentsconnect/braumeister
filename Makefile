.DEFAULT_GOAL = usage

.PHONY: clean

clean:
	-rm -rf build dist MANIFEST braumeister.egg-info .braumeister
	-find . -name '*.py[oc]' -exec rm {} \;

test:
	@make clean
	python3 -m unittest Braumeister/tests/*_test.py
	@make clean

publish_test:
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

usage:
	@echo ""
	@echo "make"
	@echo "  clean   Cleans up the dirt"
	@echo "  test    Execute all tests"
	@echo ""
