# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

# Lazy import mapping: ClassName -> module_name (relative to this package)
_EXTENSION_MAP = {
    "About": "about",
    "ApplyAttribute": "apply_attribute",
    "ApplyPalette": "apply_palette",
    "ApplyThreadlist": "apply_threadlist",
    "AutoRun": "auto_run",
    "AutoSatin": "auto_satin",
    "BatchLettering": "batch_lettering",
    "BreakApart": "break_apart",
    "Cleanup": "cleanup",
    "CommandsScaleSymbols": "commands_scale_symbols",
    "CrossStitchHelper": "cross_stitch_helper",
    "CutSatin": "cut_satin",
    "CutworkSegmentation": "cutwork_segmentation",
    "DensityMap": "density_map",
    "DisplayStackingOrder": "display_stacking_order",
    "DuplicateParams": "duplicate_params",
    "ElementInfo": "element_info",
    "FillToSatin": "fill_to_satin",
    "FillToStroke": "fill_to_stroke",
    "Flip": "flip",
    "GeneratePalette": "generate_palette",
    "GlobalCommands": "global_commands",
    "GradientBlocks": "gradient_blocks",
    "Input": "input",
    "Install": "install",
    "InstallCustomPalette": "install_custom_palette",
    "JumpToStroke": "jump_to_stroke",
    "JumpToTrim": "jump_to_trim",
    "KnockdownFill": "knockdown_fill",
    "LayerCommands": "layer_commands",
    "Lettering": "lettering",
    "LetteringAlongPath": "lettering_along_path",
    "LetteringCustomFontDir": "lettering_custom_font_dir",
    "LetteringEditJson": "lettering_edit_json",
    "LetteringFontSample": "lettering_font_sample",
    "LetteringForceLockStitches": "lettering_force_lock_stitches",
    "LetteringGenerateJson": "lettering_generate_json",
    "LetteringOrganizeGlyphs": "lettering_organize_glyphs",
    "LetteringRemoveKerning": "lettering_remove_kerning",
    "LetteringSetColorSortIndex": "lettering_set_color_sort_index",
    "LetteringSvgFontToLayers": "lettering_svg_font_to_layers",
    "LettersToFont": "letters_to_font",
    "ObjectCommands": "object_commands",
    "ObjectCommandsToggleVisibility": "object_commands_toggle_visibility",
    "Outline": "outline",
    "Output": "output",
    "PaletteSplitText": "palette_split_text",
    "PaletteToText": "palette_to_text",
    "Params": "params",
    "PngRealistic": "png_realistic",
    "PngSimple": "png_simple",
    "Preferences": "preferences",
    "Print": "print_pdf",
    "Redwork": "redwork",
    "RemoveDuplicatedPoints": "remove_duplicated_points",
    "RemoveEmbroiderySettings": "remove_embroidery_settings",
    "Reorder": "reorder",
    "SatinMulticolor": "satin_multicolor",
    "SatinToStroke": "satin_to_stroke",
    "SelectElements": "select_elements",
    "SelectionToAnchorLine": "selection_to_anchor_line",
    "SelectionToGuideLine": "selection_to_guide_line",
    "SelectionToPattern": "selection_to_pattern",
    "SewStackEditor": "sew_stack_editor",
    "Simulator": "simulator",
    "StitchPlanPreview": "stitch_plan_preview",
    "StitchPlanPreviewUndo": "stitch_plan_preview_undo",
    "StrokeToLpeSatin": "stroke_to_lpe_satin",
    "StrokeToSatin": "stroke_to_satin",
    "Tartan": "tartan",
    "TestSwatches": "test_swatches",
    "ThreadList": "thread_list",
    "TransformElements": "transform_elements",
    "Troubleshoot": "troubleshoot",
    "UnlinkClone": "unlink_clone",
    "UpdateSvg": "update_svg",
    "ZigzagLineToSatin": "zigzag_line_to_satin",
    "Zip": "zip",
}


def __getattr__(name):
    if name in _EXTENSION_MAP:
        import importlib
        module = importlib.import_module(f".{_EXTENSION_MAP[name]}", __name__)
        cls = getattr(module, name)
        globals()[name] = cls
        return cls
    if name == "extensions":
        # Lazily build the extensions list only when explicitly requested
        ext_list = [__getattr__(cls_name) for cls_name in _EXTENSION_MAP]
        globals()["extensions"] = ext_list
        return ext_list
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
