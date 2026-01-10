# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

"""Utility functions for managing Inkscape keyboard shortcuts."""

import os
from typing import Dict, List, Optional, Set

from lxml import etree

from .inkscape import guess_inkscape_config_path


# Ink/Stitch keyboard shortcuts configuration
# Format: {shortcut_key: gaction_id}
#
# These shortcuts match the official Ink/Stitch documentation:
# https://inkstitch.org/docs/customize/
#
# IMPORTANT: Inkscape uses:
#   - "app." prefix for extension gactions
#   - Underscores in extension IDs (org.inkstitch.extension_name)
#   - Capitalized modifier names like <Primary> (Ctrl) and <Shift>
#
# Note: Some shortcuts replace Inkscape defaults as documented.
INKSTITCH_SHORTCUTS: Dict[str, str] = {
    # Core functions
    "<Primary><Shift>p": "app.org.inkstitch.params",                # Params (replaces Edit > Preferences)
    "<Primary><Shift>l": "app.org.inkstitch.simulator",             # Simulator live simulation
    "<Primary><Shift>greater": "app.org.inkstitch.stitch-plan-preview",  # Stitch plan preview (replaces Path > Division)
    "<Primary><Shift>q": "app.org.inkstitch.lettering",             # Lettering (replaces Object > Selectors and CSS)
    "<Primary><Shift>Delete": "app.org.inkstitch.troubleshoot",     # Troubleshoot objects
    "<Primary><Shift>i": "app.org.inkstitch.print",                 # PDF export

    # Fill operations
    "<Primary><Shift>o": "app.org.inkstitch.break_apart",           # Break apart fill objects (replaces Object Properties)

    # Satin column operations
    "<Primary><Shift>u": "app.org.inkstitch.stroke_to_satin",       # Convert stroke to satin (replaces Object > Group)
    "<Primary><Shift>j": "app.org.inkstitch.flip_satins",           # Flip satin column rails
    "<Primary><Shift>b": "app.org.inkstitch.cut_satin",             # Cut satin column (replaces Path > Union)
    "<Primary><Shift>equal": "app.org.inkstitch.auto_satin",        # Auto route satin objects

    # Commands
    "<Primary><Shift>exclam": "app.org.inkstitch.commands",         # Attach commands to objects

    # Restack
    "<Primary><Shift>apostrophe": "app.org.inkstitch.reorder",      # Restack objects based on selection order
}


def get_inkscape_keys_path() -> str:
    """Return the path to Inkscape's keys directory."""
    config_path = guess_inkscape_config_path()
    return os.path.join(config_path, "keys")


def get_default_keymap_path() -> str:
    """Return the path to the user's default.xml keymap file."""
    return os.path.join(get_inkscape_keys_path(), "default.xml")


def ensure_keys_directory() -> None:
    """Create the keys directory if it doesn't exist."""
    keys_path = get_inkscape_keys_path()
    if not os.path.exists(keys_path):
        os.makedirs(keys_path)


def parse_keymap(path: str) -> Optional[etree._Element]:
    """Parse an Inkscape keymap XML file.

    Args:
        path: Path to the keymap XML file

    Returns:
        The root element of the parsed XML, or None if file doesn't exist
    """
    if not os.path.exists(path):
        return None
    try:
        tree = etree.parse(path)
        return tree.getroot()
    except etree.XMLSyntaxError:
        return None


def create_empty_keymap() -> etree._Element:
    """Create an empty keymap XML structure compatible with Inkscape.

    The 'name' attribute should be "User Shortcuts" to match what Inkscape
    generates when users add shortcuts via the Preferences dialog.
    """
    root = etree.Element("keys")
    root.set("name", "User Shortcuts")
    root.append(etree.Comment(" Ink/Stitch keyboard shortcuts "))
    return root


def get_existing_shortcuts(keymap: etree._Element) -> Set[str]:
    """Extract existing shortcut key bindings from a keymap.

    Args:
        keymap: Root element of the keymap XML

    Returns:
        Set of shortcut keys (lowercased) that are already bound
    """
    shortcuts: Set[str] = set()
    for bind in keymap.findall(".//bind"):
        keys = bind.get("keys", "")
        if keys:
            # Handle multiple keys separated by comma
            for key in keys.split(","):
                key = key.strip()
                if key:
                    shortcuts.add(key.lower())
    return shortcuts


def get_existing_inkstitch_actions(keymap: etree._Element) -> Set[str]:
    """Get the set of Ink/Stitch actions already in the keymap.

    Args:
        keymap: Root element of the keymap XML

    Returns:
        Set of Ink/Stitch gaction IDs that already have shortcuts
    """
    actions: Set[str] = set()
    for bind in keymap.findall(".//bind"):
        gaction = bind.get("gaction", "")
        if gaction.startswith("app.org.inkstitch."):
            actions.add(gaction)
    return actions


def add_inkstitch_shortcuts(keymap: etree._Element, shortcuts: Dict[str, str]) -> tuple[List[str], List[str]]:
    """Add Ink/Stitch shortcuts to a keymap, avoiding conflicts.

    Args:
        keymap: Root element of the keymap XML
        shortcuts: Dictionary of shortcuts to add {key: extension_id}

    Returns:
        Tuple of (shortcuts added, shortcuts skipped due to conflicts)
    """
    existing_shortcuts = get_existing_shortcuts(keymap)
    existing_actions = get_existing_inkstitch_actions(keymap)
    added: List[str] = []
    skipped: List[str] = []

    for shortcut_key, extension_id in shortcuts.items():
        # Skip if this key is already bound to something else
        if shortcut_key.lower() in existing_shortcuts:
            skipped.append(shortcut_key)
            continue

        # Skip if this extension already has a shortcut
        if extension_id in existing_actions:
            continue

        # Add the new shortcut
        bind = etree.SubElement(keymap, "bind")
        bind.set("gaction", extension_id)
        bind.set("keys", shortcut_key)
        added.append(shortcut_key)

    return added, skipped


def write_keymap(keymap: etree._Element, path: str) -> None:
    """Write a keymap to disk.

    Args:
        keymap: Root element of the keymap XML
        path: Path to write the file to
    """
    ensure_keys_directory()

    # Format the XML nicely using lxml's pretty_print
    xml_bytes = etree.tostring(keymap, encoding="utf-8", xml_declaration=True, pretty_print=True)

    with open(path, "wb") as f:
        f.write(xml_bytes)


def install_keyboard_shortcuts() -> tuple[List[str], List[str]]:
    """Install Ink/Stitch keyboard shortcuts into Inkscape's keymap.

    Preserves existing user shortcuts and only adds non-conflicting bindings.

    Returns:
        Tuple of (shortcuts added, shortcuts skipped due to conflicts)
    """
    keymap_path = get_default_keymap_path()

    # Try to load existing keymap
    keymap = parse_keymap(keymap_path)
    if keymap is None:
        # No user keymap exists, create a new one
        keymap = create_empty_keymap()

    # Add shortcuts
    added, skipped = add_inkstitch_shortcuts(keymap, INKSTITCH_SHORTCUTS)

    # Only write if we added something
    if added:
        write_keymap(keymap, keymap_path)

    return added, skipped
