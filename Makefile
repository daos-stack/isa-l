NAME    := isa-l
SRC_EXT := gz
SOURCE   = https://github.com/01org/$(NAME)/archive/v$(VERSION).tar.$(SRC_EXT)
PATCHES := $(NAME)-553f01f.patch

COMMON_RPM_ARGS := --define "%_topdir $$PWD/_topdir"
DIST    := $(shell rpm $(COMMON_RPM_ARGS) --eval %{?dist})
ifeq ($(DIST),)
SED_EXPR := 1p
else
SED_EXPR := 1s/$(DIST)//p
endif
VERSION := $(shell rpm $(COMMON_RPM_ARGS) --specfile --qf '%{version}\n' $(NAME).spec | sed -n '1p')
RELEASE := $(shell rpm $(COMMON_RPM_ARGS) --specfile --qf '%{release}\n' $(NAME).spec | sed -n '$(SED_EXPR)')
SRPM    := _topdir/SRPMS/$(NAME)-$(VERSION)-$(RELEASE)$(DIST).src.rpm
RPMS    := $(addsuffix .rpm,$(addprefix _topdir/RPMS/x86_64/,$(shell rpm --specfile $(NAME).spec)))
SPEC    := $(NAME).spec
SOURCES := $(addprefix _topdir/SOURCES/,$(notdir $(SOURCE)) $(PATCHES))
TARGETS  := $(RPMS) $(SRPM)

all: $(TARGETS)

%/:
	mkdir -p $@

_topdir/SOURCES/%: % | _topdir/SOURCES/
	rm -f $@
	ln $< $@

$(NAME)-$(VERSION).tar.$(SRC_EXT).asc:
	curl -f -L -O '$(SOURCE).asc'

$(NAME)-$(VERSION).tar.$(SRC_EXT):
	curl -f -L -O '$(SOURCE)'

v$(VERSION).tar.$(SRC_EXT):
	curl -f -L -O '$(SOURCE)'

$(VERSION).tar.$(SRC_EXT):
	curl -f -L -O '$(SOURCE)'

# see https://stackoverflow.com/questions/2973445/ for why we subst
# the "rpm" for "%" to effectively turn this into a multiple matching
# target pattern rule
$(subst rpm,%,$(RPMS)): $(SPEC) $(SOURCES)
	rpmbuild -bb $(COMMON_RPM_ARGS) $(SPEC)

$(SRPM): $(SPEC) $(SOURCES)
	rpmbuild -bs $(COMMON_RPM_ARGS) $(SPEC)

srpm: $(SRPM)

$(RPMS): Makefile

rpms: $(RPMS)

ls: $(TARGETS)
	ls -ld $^

mockbuild: $(SRPM) Makefile
	mock $<

rpmlint: $(SPEC)
	rpmlint $<

show_version:
	@echo $(VERSION)

show_release:
	@echo $(RELEASE)

show_rpms:
	@echo $(RPMS)

show_source:
	@echo $(SOURCE)

show_sources:
	@echo $(SOURCES)

.PHONY: srpm rpms ls mockbuild rpmlint FORCE show_version show_release show_rpms show_source show_sources
