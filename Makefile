SRC_PATH      = icinga2client
DOC_BUILDER  := html
DOC_SOURCEDIR = docs/source
DOC_BUILDDIR  = docs/build
DOC_APIDIR    = docs/source/api

NPROCS:=$(shell grep -c ^processor /proc/cpuinfo 2>/dev/null || echo 1)

.PHONY: clean
clean:
	find $(DOC_BUILDDIR) $(DOC_APIDIR) -mindepth 1 -delete

.PHONY: docs
docs: apidocs
	sphinx-build -b $(DOC_BUILDER) -j $(NPROCS) -q $(DOC_SOURCEDIR) $(DOC_BUILDDIR)

.PHONY: apidocs
apidocs:
	sphinx-apidoc -o $(DOC_APIDIR) -T -e $(SRC_PATH)
