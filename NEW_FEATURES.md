# New InkStitch Features - MVP Implementation

This document describes the new features added to InkStitch to close the gap with commercial embroidery software.

## Features Implemented

### 1. Appliqué Automation ✅
**File**: `lib/extensions/applique_auto.py`
**Template**: `templates/applique_auto.xml`
**Menu**: Tools: Fill > Appliqué (Auto)

**What it does**:
- Automatically converts fill shapes to complete appliqué designs
- Creates three layers:
  1. **Placement line** - Shows where to position the fabric (offset inward)
  2. **Tack-down stitches** - Secures fabric to base (zigzag or running stitch)
  3. **Cover stitch** - Satin stitch covering raw edges

**Parameters**:
- Placement offset (0-5mm, default 0.5mm)
- Tack-down type (zigzag or running)
- Tack-down offset (0-10mm, default 1.0mm)
- Cover satin width (1-10mm, default 3.0mm)
- Keep original fill option

**Usage**:
1. Select a fill object
2. Extensions > Ink/Stitch > Tools: Fill > Appliqué (Auto)
3. Adjust parameters as needed
4. Apply

---

### 2. Intelligent Color Optimization ✅
**File**: `lib/extensions/optimize_colors.py`
**Template**: `templates/optimize_colors.xml`
**Menu**: Edit > Optimize Thread Colors

**What it does**:
- Analyzes design and reorders stitch groups to minimize thread changes
- Reduces production time and thread waste
- Shows before/after improvement statistics

**Strategies**:
- **Greedy**: Groups all same-color stitches together (maximum color reduction)
- **Spatial**: Balances color grouping with jump stitch length (balanced approach)

**Parameters**:
- Optimization strategy (greedy or spatial)
- Maximum jump stitch length (10-200mm, default 50mm)

**Usage**:
1. Select your design (or work on entire document)
2. Extensions > Ink/Stitch > Edit > Optimize Thread Colors
3. Choose strategy
4. Apply

**Example Output**:
```
Color optimization complete!
Original thread changes: 47
Optimized thread changes: 12
Improvement: 35 fewer changes
```

---

### 3. Multi-Hooping Support ✅
**File**: `lib/extensions/multi_hoop.py`
**Template**: `templates/multi_hoop.xml`
**Menu**: Edit > Multi-hooping

**What it does**:
- Splits large designs across multiple hoops
- Adds registration marks for accurate alignment
- Creates separate layers for each hoop section
- Calculates optimal grid layout

**Parameters**:
- Hoop width (50-400mm, default 100mm)
- Hoop height (50-400mm, default 100mm)
- Overlap between hoops (0-50mm, default 10mm)
- Add registration marks (on/off)
- Registration mark size (2-20mm, default 5mm)

**Usage**:
1. Select your entire design
2. Extensions > Ink/Stitch > Edit > Multi-hooping
3. Enter your hoop dimensions
4. Apply
5. Export each layer separately for stitching

**Output**:
- Creates layers named "Hoop 1 (Row 1, Col 1)", "Hoop 2 (Row 1, Col 2)", etc.
- Each layer contains:
  - Hoop boundary rectangle (dashed line, ignored by stitcher)
  - Registration crosshairs at corners
  - Design elements that fall within that hoop

---

### 4. 3D/Dimensional Stitch Effects ✅
**File**: `lib/extensions/dimensional_effect.py`
**Template**: `templates/dimensional_effect.xml`
**Menu**: Tools: Fill > 3D/Dimensional Effect

**What it does**:
- Applies raised, textured effects to fill stitches
- Modifies stitch density and adds perpendicular underlay
- Creates dimensional appearance in embroidery

**Parameters**:
- Effect height (50-200%, default 150%)
- Wave frequency (1-10, default 3.0)

**Usage**:
1. Select fill objects
2. Extensions > Ink/Stitch > Tools: Fill > 3D/Dimensional Effect
3. Adjust height and frequency
4. Apply

**Technical Details**:
- Increases row spacing proportionally to height %
- Adds perpendicular underlay for dimension
- Adjusts max stitch length for texture
- Labels modified fills with "(3D)" suffix

---

### 5. Built-in Design Library ✅
**File**: `lib/extensions/design_library.py`
**Template**: `templates/design_library.xml`
**Menu**: Tools: Fill > Design Library

**What it does**:
- Provides access to pre-made embroidery designs
- Allows browsing and inserting designs into documents
- Creates sample designs on first run
- Supports custom design additions

**Built-in Designs**:
- Simple Flower
- Star
- Heart
- (Users can add more to `designs/library/` directory)

**Parameters**:
- Category filter (all, flowers, shapes, borders, motifs)
- Design name to insert

**Usage**:
1. Extensions > Ink/Stitch > Tools: Fill > Design Library
2. Select category
3. Enter design name (e.g., "flower_simple")
4. Apply - design is inserted at current layer

**Adding Custom Designs**:
- Save embroidery-ready SVG files to `inkstitch/designs/library/`
- Use descriptive filenames (e.g., `rose_border.svg`)
- Designs appear automatically in the library

---

### 6. TrueType Font Instant Conversion ✅
**File**: `lib/extensions/ttf_to_embroidery.py`
**Template**: `templates/ttf_to_embroidery.xml`
**Menu**: Lettering > TrueType to Embroidery

**What it does**:
- Converts text using any system font to embroidery-ready format
- Supports both satin (outline) and fill lettering
- Applies appropriate embroidery parameters automatically

**Parameters**:
- Stitch type (satin or fill)
- Satin width (1-10mm, default 2.0mm)
- Fill angle (0-360°, default 0°)
- Keep original text option

**Usage**:
1. Create text with Inkscape text tool
2. **IMPORTANT**: Convert to path first (Path > Object to Path)
3. Select the path
4. Extensions > Ink/Stitch > Lettering > TrueType to Embroidery
5. Choose stitch type and parameters
6. Apply

**Notes**:
- Works best when text is converted to path first
- Satin creates outline stitching (good for larger text)
- Fill creates solid lettering (good for bold fonts)
- Automatically adds pull compensation for satin

---

## Installation

These features are part of the InkStitch extension. To use them:

1. **Build InkStitch** (generates INX files):
   ```bash
   make
   ```

2. **Install/Update** InkStitch in Inkscape:
   - Follow standard InkStitch installation procedures
   - Or use development mode with symlinks

3. **Restart Inkscape**

4. **Access new features** via:
   - Extensions > Ink/Stitch menu

---

## Feature Comparison Update

### What InkStitch Now Has:

✅ Appliqué automation
✅ Intelligent color optimization
✅ Multi-hooping support
✅ 3D/dimensional effects
✅ TrueType font conversion (with path conversion step)
✅ Built-in design library

### Still Missing (for future development):

❌ Full auto-digitizing from photos (requires complex image processing)
❌ Wireless machine transfer (hardware/protocol dependent)
❌ One-click TrueType conversion (requires deeper Inkscape integration)
❌ Fabric selector with auto-adjustment
❌ Extensive built-in design library (currently 3 samples, expandable)

---

## Technical Notes

### File Structure

```
inkstitch/
├── lib/
│   ├── extensions/
│   │   ├── applique_auto.py          # New
│   │   ├── optimize_colors.py        # New
│   │   ├── multi_hoop.py             # New
│   │   ├── dimensional_effect.py     # New
│   │   ├── design_library.py         # New
│   │   └── ttf_to_embroidery.py      # New
│   └── stitches/
│       └── dimensional_fill.py        # New (experimental)
├── templates/
│   ├── applique_auto.xml              # New
│   ├── optimize_colors.xml            # New
│   ├── multi_hoop.xml                 # New
│   ├── dimensional_effect.xml         # New
│   ├── design_library.xml             # New
│   └── ttf_to_embroidery.xml          # New
└── designs/
    └── library/                       # New (created on first run)
        ├── flower_simple.svg
        ├── star.svg
        └── heart.svg
```

### Dependencies

All new features use existing InkStitch dependencies:
- `inkex` - Inkscape extension API
- `shapely` - Geometric operations
- Standard Python library

No additional dependencies required.

### Code Style

- Follows existing InkStitch conventions
- Uses InkstitchExtension base class
- Includes i18n support via `_()` function
- Includes help documentation in XML templates

---

## Future Enhancements

### Potential Improvements:

1. **Appliqué**:
   - Multiple fabric layers
   - Custom stitch sequences
   - Appliqué templates

2. **Color Optimization**:
   - Machine learning-based optimization
   - User-defined priority rules
   - Undo/redo optimization

3. **Multi-Hooping**:
   - Automatic splitting suggestions
   - Export multiple files at once
   - Visual preview of hoop positions

4. **3D Effects**:
   - Additional dimensional patterns
   - Trapunto support
   - Custom height maps

5. **Design Library**:
   - Web-based design browser
   - Download designs from repository
   - Design rating and search

6. **Font Conversion**:
   - Direct font file parsing
   - Font preview before conversion
   - Batch text conversion

---

## Contributing

These features are MVPs (Minimum Viable Products). Contributions to enhance them are welcome!

- Report issues on GitHub
- Submit pull requests
- Add designs to the library
- Improve documentation

---

## License

Copyright (c) 2025 Authors
Licensed under GNU GPL version 3.0 or later

---

## Credits

Developed to close the feature gap between InkStitch and commercial embroidery software, making professional-grade embroidery design accessible to everyone.
