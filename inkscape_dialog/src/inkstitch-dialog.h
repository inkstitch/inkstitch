#pragma once

#include <gtkmm/label.h>
#include "ui/dialog/dialog-base.h"

namespace Inkstitch {

class InkstitchDialog final : public Inkscape::UI::Dialog::DialogBase
{
public:
    InkstitchDialog(const char *plugin_dir, const char *ui_file);

    void selectionChanged(Inkscape::Selection *) override;
    void selectionModified(Inkscape::Selection *, guint flags) override;

private:
    void update_from_selection(Inkscape::Selection *);

    Gtk::Label *_stroke_method_value = nullptr;
    Gtk::Label *_fill_method_value   = nullptr;
};

} // namespace Inkstitch
