#pragma once

#include "ui/dialog/dialog-base.h"

namespace Gtk { class Label; }
namespace Inkscape { class Selection; }

namespace Inkstitch {

class InkstitchDialog final : public Inkscape::UI::Dialog::DialogBase
{
public:
    explicit InkstitchDialog(const char *plugin_dir);
    ~InkstitchDialog() final = default;

    void selectionChanged(Inkscape::Selection *selection) override;
    void selectionModified(Inkscape::Selection *selection, guint flags) override;

private:
    void update_from_selection(Inkscape::Selection *selection);

    Gtk::Label *_stroke_method_value = nullptr;
    Gtk::Label *_fill_method_value = nullptr;
};

} // namespace Inkstitch
