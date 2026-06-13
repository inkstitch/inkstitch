cmake_minimum_required(VERSION 3.20)
project(inkstitch-dialog CXX)
set(CMAKE_CXX_STANDARD 20)

set(INKSCAPE_DIR "" CACHE PATH "Path to Inkscape source tree root")
if(NOT INKSCAPE_DIR)
    message(FATAL_ERROR "Set INKSCAPE_DIR to the Inkscape source tree root")
endif()

find_package(PkgConfig REQUIRED)
pkg_check_modules(GTKMM  gtkmm-4.0   REQUIRED IMPORTED_TARGET)
pkg_check_modules(GLIBMM glibmm-2.68 REQUIRED IMPORTED_TARGET)
pkg_check_modules(TWGEOM 2geom       REQUIRED IMPORTED_TARGET)

add_library(inkstitch-dialog SHARED src/inkstitch-dialog.cpp)

target_include_directories(inkstitch-dialog PRIVATE
    ${INKSCAPE_DIR}/src
)

target_link_libraries(inkstitch-dialog PRIVATE
    PkgConfig::GTKMM
    PkgConfig::GLIBMM
    PkgConfig::TWGEOM
    ${INKSCAPE_DIR}/build/lib/libinkscape_base.so
)

# Loader: g_build_filename(base_dir, name) then g_module_open(), which appends
# the platform suffix (.so) automatically. Name in .inx is "libinkstitch-dialog".
set_target_properties(inkstitch-dialog PROPERTIES
    PREFIX "lib"
    BUILD_RPATH  "${INKSCAPE_DIR}/build/lib"
    INSTALL_RPATH "${INKSCAPE_DIR}/build/lib"
)
