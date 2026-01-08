ZUSPEC_WEB_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

ifeq (,$(PACKAGES_DIR))
  PACKAGES_DIR:=$(ZUSPEC_WEB_DIR)/packages
endif

PAPERS += papers/zuspec_pythonic_hw_dev/Zuspec_PythonicModelDrivenHardwareDesign.pdf

all : main

main : $(PAPERS) build-docs

build-docs: $(PAPERS)
	$(MAKE) -C docs html
	rm -rf web
	cp -r docs/_build/html web
#	mkdir -p web/papers
#	cp $(PAPERS) web/papers
	touch web/.nojekyll

papers/zuspec_pythonic_hw_dev/Zuspec_PythonicModelDrivenHardwareDesign.pdf :
	cd papers/zuspec_pythonic_hw_dev ; \
		pandoc Zuspec_PythonicModelDrivenHardwareDesign.md \
		-o $(notdir $@)

clean :
	rm -rf web
	rm -f llms.txt
	cd docs && $(MAKE) clean

.PHONY: all main build-docs generate-llms build-package-docs copy-package-docs clean clean-all
