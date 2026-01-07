# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

"""Utility functions for managing Inkscape keyboard shortcuts."""

import os
from typing import Dict, List, Optional, Set
from xml.etree import ElementTree as ET

from .inkscape import guess_inkscape_config_path


# Ink/Stitch keyboard shortcuts configuration
# Format: {shortcut_key: gaction_id}
# Using Alt+letter combinations that don't conflict with default Inkscape shortcuts
#
# IMPORTANT: Inkscape uses:
#   - "app." prefix for extension gactions
#   - Hyphens in extension names (not underscores)
#   - Capitalized modifier names like <Alt> not <alt>
INKSTITCH_SHORTCUTS: Dict[str, str] = {
    "<Alt>e": "app.org.inkstitch.params",               # Edit parameters (most used)
    "<Alt>s": "app.org.inkstitch.simulator",            # Simulator preview
    "<Alt>v": "app.org.inkstitch.stitch-plan-preview",  # View stitch plan
    "<Alt>t": "app.org.inkstitch.troubleshoot",         # Troubleshoot issues
    "<Alt>l": "app.org.inkstitch.lettering",            # Lettering tool
    "<Alt>r": "app.org.inkstitch.reorder",              # Reorder elements
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


def parse_keymap(path: str) -> Optional[ET.Element]:
    """Parse an Inkscape keymap XML file.

    Args:
        path: Path to the keymap XML file

    Returns:
        The root element of the parsed XML, or None if file doesn't exist
    """
    if not os.path.exists(path):
        return None
    try:
        tree = ET.parse(path)
        return tree.getroot()
    except ET.ParseError:
        return None


def create_empty_keymap() -> ET.Element:
    """Create an empty keymap XML structure compatible with Inkscape.

    The 'name' attribute should be "User Shortcuts" to match what Inkscape
    generates when users add shortcuts via the Preferences dialog.
    """
    root = ET.Element("keys")
    root.set("name", "User Shortcuts")
    root.text = "\n"
    comment = ET.Comment(" Ink/Stitch keyboard shortcuts ")
    root.insert(0, comment)
    return root


def get_existing_shortcuts(keymap: ET.Element) -> Dict[str, str]:
    """Extract existing shortcut bindings from a keymap.

    Args:
        keymap: Root element of the keymap XML

    Returns:
        Dictionary mapping shortcut keys to action/extension IDs
    """
    shortcuts: Dict[str, str] = {}
    for bind in keymap.findall(".//bind"):
        keys = bind.get("keys", "")
        gaction = bind.get("gaction", "")
        if keys and gaction:
            # Handle multiple keys separated by comma
            for key in keys.split(","):
                key = key.strip()
                if key:
                    shortcuts[key.lower()] = gaction
    return shortcuts


def get_existing_inkstitch_actions(keymap: ET.Element) -> Set[str]:
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


def add_inkstitch_shortcuts(keymap: ET.Element, shortcuts: Dict[str, str]) -> List[str]:
    """Add Ink/Stitch shortcuts to a keymap, avoiding conflicts.

    Args:
        keymap: Root element of the keymap XML
        shortcuts: Dictionary of shortcuts to add {key: extension_id}

    Returns:
        List of shortcuts that were actually added
    """
    existing_shortcuts = get_existing_shortcuts(keymap)
    existing_actions = get_existing_inkstitch_actions(keymap)
    added: List[str] = []

    for shortcut_key, extension_id in shortcuts.items():
        # Skip if this key is already bound to something else
        if shortcut_key.lower() in [k.lower() for k in existing_shortcuts.keys()]:
            continue

        # Skip if this extension already has a shortcut
        if extension_id in existing_actions:
            continue

        # Add the new shortcut
        bind = ET.SubElement(keymap, "bind")
        bind.set("gaction", extension_id)
        bind.set("keys", shortcut_key)
        bind.tail = "\n"
        added.append(shortcut_key)

    return added


def write_keymap(keymap: ET.Element, path: str) -> None:
    """Write a keymap to disk.

    Args:
        keymap: Root element of the keymap XML
        path: Path to write the file to
    """
    ensure_keys_directory()

    # Format the XML nicely
    indent_xml(keymap)

    tree = ET.ElementTree(keymap)
    tree.write(path, encoding="utf-8", xml_declaration=True)


def indent_xml(elem: ET.Element, level: int = 0) -> None:
    """Add indentation to XML elements for pretty printing."""
    indent = "  "
    i = "\n" + level * indent
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + indent
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for child in elem:
            indent_xml(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def install_keyboard_shortcuts() -> List[str]:
    """Install Ink/Stitch keyboard shortcuts into Inkscape's keymap.

    Preserves existing user shortcuts and only adds non-conflicting bindings.

    Returns:
        List of shortcuts that were added
    """
    keymap_path = get_default_keymap_path()

    # Try to load existing keymap
    keymap = parse_keymap(keymap_path)
    if keymap is None:
        # No user keymap exists, create a new one
        keymap = create_empty_keymap()

    # Add shortcuts
    added = add_inkstitch_shortcuts(keymap, INKSTITCH_SHORTCUTS)

    # Only write if we added something
    if added:
        write_keymap(keymap, keymap_path)

    return added


def remove_keyboard_shortcuts() -> List[str]:
    """Remove Ink/Stitch keyboard shortcuts from Inkscape's keymap.

    Returns:
        List of shortcuts that were removed
    """
    keymap_path = get_default_keymap_path()
    keymap = parse_keymap(keymap_path)

    if keymap is None:
        return []

    removed: List[str] = []
    # Find and remove Ink/Stitch bindings
    for bind in list(keymap.findall(".//bind")):
        gaction = bind.get("gaction", "")
        if gaction.startswith("app.org.inkstitch."):
            keys = bind.get("keys", "")
            keymap.remove(bind)
            removed.append(keys)

    if removed:
        write_keymap(keymap, keymap_path)

    return removed
