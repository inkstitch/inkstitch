cmake_minimum_required(VERSION 3.20)
project(inkstitch-dialog-plugin VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# INKSCAPE_DIR   : root of the Inkscape source/build tree
# The build subdirectory is assumed to be ${INKSCAPE_DIR}/build (the default
# produced by following Inkscape's own build instructions).
set(INKSCAPE_DIR "" CACHE PATH
    "Root of the Inkscape source tree (the one containing src/ and build/)")

if(NOT INKSCAPE_DIR)
    message(FATAL_ERROR
        "Set -DINKSCAPE_DIR=/path/to/inkscape, or use a CMakePresets.json preset.")
endif()

set(INKSCAPE_SRC     "${INKSCAPE_DIR}/src")
set(INKSCAPE_GEN     "${INKSCAPE_DIR}/build/src")    # generated headers (inkscape-version.h)
set(INKSCAPE_LIB_DIR "${INKSCAPE_DIR}/build/install_dir/lib/inkscape")

if(NOT EXISTS "${INKSCAPE_SRC}/ui/dialog/dialog-plugin.h")
    message(FATAL_ERROR
        "Cannot find dialog-plugin.h under ${INKSCAPE_SRC}. "
        "Is INKSCAPE_DIR set to the correct Inkscape source root?")
endif()

find_package(PkgConfig REQUIRED)
pkg_check_modules(GTKMM  REQUIRED IMPORTED_TARGET gtkmm-4.0)
pkg_check_modules(GLIBMM REQUIRED IMPORTED_TARGET glibmm-2.68)

# 2Geom: use the copy that was built with Inkscape (installed under build/install_dir)
find_package(2Geom REQUIRED
    HINTS "${INKSCAPE_DIR}/build/install_dir/lib/cmake/2Geom"
)
message(STATUS "2Geom         : ${2Geom_DIR}")

find_library(INKSCAPE_BASE_LIB
    NAMES inkscape_base
    HINTS "${INKSCAPE_LIB_DIR}"
    REQUIRED
)
message(STATUS "inkscape_base : ${INKSCAPE_BASE_LIB}")

add_library(inkstitch-dialog SHARED
    src/inkstitch-dialog.cpp
)

target_include_directories(inkstitch-dialog PRIVATE
    ${INKSCAPE_SRC}    # all Inkscape headers
    ${INKSCAPE_GEN}    # generated headers (inkscape-version.h, config.h, …)
)

target_link_libraries(inkstitch-dialog PRIVATE
    ${INKSCAPE_BASE_LIB}
    2Geom::2geom
    PkgConfig::GTKMM
    PkgConfig::GLIBMM
)

set_target_properties(inkstitch-dialog PROPERTIES
    PREFIX          "lib"
    OUTPUT_NAME     "inkstitch-dialog"
    # Allow the .so to find libinkscape_base.so wherever Inkscape is installed.
    BUILD_RPATH     "${INKSCAPE_LIB_DIR}"
    INSTALL_RPATH   "${INKSCAPE_LIB_DIR}"
    INSTALL_RPATH_USE_LINK_PATH ON
)

# Default: user extension directory.  Override with -DPLUGIN_INSTALL_DIR=…
# The plugin files land in inkscape_dialog/ so Inkscape's scanner can find them.
set(PLUGIN_INSTALL_DIR "$ENV{HOME}/.config/inkscape/extensions/inkstitch/inkscape_dialog"
    CACHE PATH "Destination directory for the installed plugin files")

install(TARGETS inkstitch-dialog
    LIBRARY DESTINATION "${PLUGIN_INSTALL_DIR}"
)
install(FILES
    manifest/inkstitch.idlg
    src/inkstitch-dialog.ui
    DESTINATION "${PLUGIN_INSTALL_DIR}"
)
