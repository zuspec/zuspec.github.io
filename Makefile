ZUSPEC_WEB_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

ifeq (,$(PACKAGES_DIR))
  PACKAGES_DIR:=$(ZUSPEC_WEB_DIR)/packages
endif

PAPERS += papers/zuspec_pythonic_hw_dev/Zuspec_PythonicModelDrivenHardwareDesign.pdf

all : main
	touch web/.nojekyll

main : $(PAPERS)
	rm -rf web
	jekyll build -d web

papers/zuspec_pythonic_hw_dev/Zuspec_PythonicModelDrivenHardwareDesign.pdf :
	cd papers/zuspec_pythonic_hw_dev ; \
		pandoc Zuspec_PythonicModelDrivenHardwareDesign.md \
		-o $(notdir $@)


clean :
	rm -rf web
