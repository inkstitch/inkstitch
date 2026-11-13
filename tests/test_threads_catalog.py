from unittest.mock import Mock, patch

from lib.threads.catalog import _ThreadCatalog, get_palette_paths


def _write_palette(path, name):
    path.write_text(
        f"GIMP Palette\nName: Ink/Stitch: {name}\nColumns: 1\n",
        encoding="utf8",
    )


def test_load_palettes_parses_each_palette_once():
    catalog = _ThreadCatalog.__new__(_ThreadCatalog)
    catalog.palettes = []
    palette = Mock(is_gimp_palette=True)
    palette_path = "/palettes/InkStitch Test.gpl"

    with patch(
        "lib.threads.catalog.glob",
        return_value=[palette_path],
    ), patch(
        "lib.threads.catalog.ThreadPalette",
        return_value=palette,
    ) as parse_palette:
        catalog.load_palettes(["/palettes"])

    parse_palette.assert_called_once_with(palette_path)
    assert catalog.palettes == [palette]


def test_get_palette_by_name_loads_only_selected_palette(tmp_path):
    user_palettes = tmp_path / "user"
    bundled_palettes = tmp_path / "bundled"
    user_palettes.mkdir()
    bundled_palettes.mkdir()
    user_palette = user_palettes / "InkStitch Selected.gpl"
    bundled_palette = bundled_palettes / "InkStitch Selected.gpl"
    _write_palette(user_palette, "Selected")
    _write_palette(bundled_palette, "Selected")
    palette = Mock(is_gimp_palette=True)
    catalog = _ThreadCatalog()

    with patch(
        "lib.threads.catalog.get_palette_paths",
        return_value=[str(user_palettes), str(bundled_palettes)],
    ), patch(
        "lib.threads.catalog.ThreadPalette",
        return_value=palette,
    ) as parse_palette:
        assert catalog.get_palette_by_name("Selected") is palette

    parse_palette.assert_called_once_with(str(user_palette))
    assert catalog._palettes_loaded is False


def test_matching_without_named_palette_loads_catalog():
    catalog = _ThreadCatalog()

    with patch.object(catalog, "load_palettes") as load_palettes:
        assert catalog.match_and_apply_palette([]) is None

    load_palettes.assert_called_once_with(get_palette_paths())
