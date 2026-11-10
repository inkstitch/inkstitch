from unittest.mock import patch, sentinel

from lib.extensions.output import Output


def test_apply_thread_palette_can_be_skipped():
    extension = Output.__new__(Output)
    extension.settings = {"skip_palette": True}
    extension.metadata = {"thread-palette": "Selected"}

    with patch("lib.threads.ThreadCatalog") as thread_catalog:
        extension.apply_thread_palette(sentinel.stitch_plan)

    thread_catalog.assert_not_called()
    assert extension.settings == {}


def test_apply_thread_palette_uses_catalog_by_default():
    extension = Output.__new__(Output)
    extension.settings = {}
    extension.metadata = {"thread-palette": "Selected"}

    with patch("lib.threads.ThreadCatalog") as thread_catalog:
        extension.apply_thread_palette(sentinel.stitch_plan)

    thread_catalog.return_value.match_and_apply_palette.assert_called_once_with(
        sentinel.stitch_plan,
        "Selected",
    )
