BUILD_DIR   := build/release
RELEASE_DIR := release

SO   := $(BUILD_DIR)/libinkstitch-dialog.so
UI   := src/inkstitch-dialog.ui
IDLG := src/inkstitch.idlg

.PHONY: release clean

ICONS_DST := $(RELEASE_DIR)/icons/hicolor/scalable/actions

release: $(SO)
	@mkdir -p $(RELEASE_DIR) $(ICONS_DST)
	cp $(SO)   $(RELEASE_DIR)/libinkstitch-dialog.so
	cp $(UI)   $(RELEASE_DIR)/inkstitch-dialog.ui
	cp $(IDLG) $(RELEASE_DIR)/inkstitch.idlg
	cp assets/inkstitch-stroke-satin.svg $(ICONS_DST)/inkstitch-stroke-to-satin.svg

$(SO): src/inkstitch-dialog.cpp src/inkstitch-dialog.h
	cmake --workflow --preset release

clean:
	rm -rf $(RELEASE_DIR)
