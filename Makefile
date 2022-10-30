ZUSPEC_WEB_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

ifeq (,$(PACKAGES_DIR))
  PACKAGES_DIR:=$(ZUSPEC_WEB_DIR)/packages
endif

all : main
	touch web/.nojekyll

main :
	rm -rf web
	jekyll build -d web

clean :
	rm -rf web
