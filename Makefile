ZUSPEC_WEB_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

ifeq (,$(PACKAGES_DIR))
  PACKAGES_DIR:=$(ZUSPEC_WEB_DIR)/packages
endif

PAPERS += papers/zuspec_pythonic_hw_dev/Zuspec_PythonicModelDrivenHardwareDesign.pdf

all : main

main : $(PAPERS) build-docs

build-docs:
	cd docs && $(MAKE) html
	rm -rf web
	cp -r docs/_build/html web
	touch web/.nojekyll
	$(MAKE) generate-llms

generate-llms:
	@echo "Generating llms.txt..."
	python3 generate-llms-txt.py
	@mkdir -p web
	cp llms.txt web/llms.txt
	@echo "✓ llms.txt generated and copied to web/"

# Optional: Build individual package documentation
build-package-docs:
	./build-package-docs.sh

# Optional: Copy package docs to web output  
copy-package-docs: build-package-docs
	@echo "Copying package documentation to web..."
	@for pkg in zuspec-dataclasses zuspec-be-sv zuspec-be-sw zuspec-be-hdlsim zuspec-be-trace zuspec-be-fv; do \
		if [ -d "packages/$$pkg/docs/_build/html" ]; then \
			echo "  Copying $$pkg docs..."; \
			mkdir -p web/packages/$$pkg/docs; \
			cp -r packages/$$pkg/docs/_build/html/* web/packages/$$pkg/docs/; \
		fi \
	done
	@echo "Package docs copied to web/"

papers/zuspec_pythonic_hw_dev/Zuspec_PythonicModelDrivenHardwareDesign.pdf :
	cd papers/zuspec_pythonic_hw_dev ; \
		pandoc Zuspec_PythonicModelDrivenHardwareDesign.md \
		-o $(notdir $@)

clean :
	rm -rf web
	rm -f llms.txt
	cd docs && $(MAKE) clean

clean-all: clean
	@echo "Cleaning package documentation..."
	@for pkg in zuspec-dataclasses zuspec-be-sv zuspec-be-sw zuspec-be-hdlsim zuspec-be-trace zuspec-be-fv; do \
		if [ -d "packages/$$pkg/docs" ] && [ -f "packages/$$pkg/docs/Makefile" ]; then \
			echo "  Cleaning $$pkg docs..."; \
			cd packages/$$pkg/docs && $(MAKE) clean && cd $(ZUSPEC_WEB_DIR); \
		fi \
	done

.PHONY: all main build-docs generate-llms build-package-docs copy-package-docs clean clean-all
