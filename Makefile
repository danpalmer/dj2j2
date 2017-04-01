version:=$(shell python setup.py --version)

release:
	git diff-index --quiet HEAD
	git tag $(version)
	git push
	git push --tags
	python setup.py sdist bdist_wheel register upload
