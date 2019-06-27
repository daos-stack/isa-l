NAME    := isa-l
DEB_NAME := libisal
SRC_EXT := gz
SOURCE   = https://github.com/01org/$(NAME)/archive/v$(VERSION).tar.$(SRC_EXT)
#PATCHES := $(NAME)-553f01f.patch

include Makefile_packaging.mk

