#include "inkstitch-dialog.h"

#include <gtkmm/button.h>
#include <gtkmm/icontheme.h>
#include <gtkmm/label.h>
#include <gdkmm/display.h>
#include <glibmm/miscutils.h>
#include <glibmm/ustring.h>

#include "inkscape-version.h"
#include "inkscape-application.h"
#include "object/sp-item.h"
#include "selection.h"
#include "ui/builder-utils.h"
#include "xml/node.h"
#include "extension/db.h"
#include "extension/effect.h"
#include "extension/implementation/implementation.h"

namespace Inkstitch {

static void run_effect(const char *id)
{
    auto *ext = Inkscape::Extension::db.get(id);
    auto *effect = dynamic_cast<Inkscape::Extension::Effect *>(ext);
    if (!effect) {
        g_warning("inkstitch: extension not found: %s", id);
        return;
    }
    effect->prefs(InkscapeApplication::instance()->get_active_desktop());
}

InkstitchDialog::InkstitchDialog(const char *plugin_dir, const char *ui_file)
    : DialogBase("/dialogs/inkstitch", "org.inkstitch.dialog")
{
    if (auto display = Gdk::Display::get_default()) {
        Gtk::IconTheme::get_for_display(display)->add_search_path(
            Glib::build_filename(plugin_dir, "icons"));
    }

    auto builder = Inkscape::UI::create_builder_from_path(ui_file);

    _stroke_method_value = &Inkscape::UI::get_widget<Gtk::Label>(builder, "stroke-method-value");
    _fill_method_value   = &Inkscape::UI::get_widget<Gtk::Label>(builder, "fill-method-value");

    auto connect = [&](const char *widget_id, const char *ext_id) {
        Inkscape::UI::get_widget<Gtk::Button>(builder, widget_id)
            .signal_clicked().connect([ext_id]{ run_effect(ext_id); });
    };

    // Fill tools
    connect("btn-break-apart",     "org.inkstitch.break_apart");
    connect("btn-cross-stitch",    "org.inkstitch.cross_stitch_helper");
    connect("btn-gradient-blocks", "org.inkstitch.gradient_blocks");
    connect("btn-knockdown-fill",  "org.inkstitch.knockdown_fill");
    connect("btn-tartan",          "org.inkstitch.tartan");

    // Satin tools
    connect("btn-auto-satin",       "org.inkstitch.auto_satin");
    connect("btn-cut-satin",        "org.inkstitch.cut_satin");
    connect("btn-fill-to-satin",    "org.inkstitch.fill_to_satin");
    connect("btn-flip-satins",      "org.inkstitch.flip_satins");
    connect("btn-satin-multicolor", "org.inkstitch.satin_multicolor");
    connect("btn-stroke-lpe-satin", "org.inkstitch.stroke_lpe_satin");
    connect("btn-stroke-to-satin",  "org.inkstitch.stroke_to_satin");
    connect("btn-zigzag-to-satin",  "org.inkstitch.zigzag_line_to_satin");

    // Stroke tools
    connect("btn-auto-run",        "org.inkstitch.auto_run");
    connect("btn-fill-to-stroke",  "org.inkstitch.fill_to_stroke");
    connect("btn-jump-to-stroke",  "org.inkstitch.jump_to_stroke");
    connect("btn-outline",         "org.inkstitch.outline");
    connect("btn-redwork",         "org.inkstitch.redwork");
    connect("btn-satin-to-stroke", "org.inkstitch.satin_to_stroke");
    connect("btn-preview",         "org.inkstitch.stitch_plan_preview");

    append(Inkscape::UI::get_widget<Gtk::Widget>(builder, "dialog-root"));
}

void InkstitchDialog::update_from_selection(Inkscape::Selection *selection)
{
    if (!_stroke_method_value)
        return;

    auto reset = [&]() {
        _stroke_method_value->set_text("—");
        _fill_method_value->set_text("—");
    };

    if (!selection) { reset(); return; }

    auto *item = selection->singleItem();
    if (!item) { reset(); return; }

    auto *repr = item->getRepr();
    if (!repr) { reset(); return; }

    // Read the inline CSS string — same data that element.py's get_style() inspects.
    // Inkscape normalises inline CSS so "stroke:none" has no spaces around the colon.
    Glib::ustring css(repr->attribute("style") ? repr->attribute("style") : "");

    auto css_is_none = [&](const char *prop) {
        Glib::ustring needle = Glib::ustring(prop) + ":none";
        return css.find(needle) != Glib::ustring::npos;
    };

    if (!css_is_none("stroke")) {
        const char *val = repr->attribute("inkstitch:stroke_method");
        _stroke_method_value->set_text(val ? val : "bean_stitch");
    } else {
        _stroke_method_value->set_text("N/A");
    }

    if (!css_is_none("fill")) {
        const char *val = repr->attribute("inkstitch:fill_method");
        _fill_method_value->set_text(val ? val : "auto_fill");
    } else {
        _fill_method_value->set_text("N/A");
    }
}

void InkstitchDialog::selectionChanged(Inkscape::Selection *selection)
{
    update_from_selection(selection);
}

void InkstitchDialog::selectionModified(Inkscape::Selection *selection, guint)
{
    update_from_selection(selection);
}

} // namespace Inkstitch

// ── Implementation plugin ────────────────────────────────────────────────────

class InkstitchImpl : public Inkscape::Extension::Implementation::Implementation
{
public:
    Inkscape::UI::Dialog::DialogBase *
    create_dialog(const char *plugin_dir, const char *ui_file) override
    {
        return new Inkstitch::InkstitchDialog(plugin_dir, ui_file);
    }
};

extern "C" G_MODULE_EXPORT
Inkscape::Extension::Implementation::Implementation *GetImplementation()
{
    return new InkstitchImpl();
}

extern "C" G_MODULE_EXPORT
const gchar *GetInkscapeVersion()
{
    return Inkscape::version_string;
}
