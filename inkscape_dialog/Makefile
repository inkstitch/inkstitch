BUILD_DIR := build/release
SO        := $(BUILD_DIR)/libinkstitch-dialog.so
ICONS_DST := icons/hicolor/scalable/actions

.PHONY: all clean

all: $(SO)
	cp $(SO) libinkstitch-dialog.so
	mkdir -p $(ICONS_DST)
	cp assets/*.svg $(ICONS_DST)/

$(SO): src/inkstitch-dialog.cpp src/inkstitch-dialog.h
	cmake --workflow --preset release

clean:
	rm -rf build libinkstitch-dialog.so icons
