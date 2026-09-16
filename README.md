# DXF to SACS

Python utility to convert 3D DXF line geometry into SACS2025 (Bentley) structural input files, with automatic node merging, layer-to-group mapping, and an interactive proximity quality check.

## Why?

SACS doesn't natively import CAD files — geometry has to be rebuilt node-by-node, or built through a parametric wizard limited to standard offshore jacket structures. This script reads a DXF file and generates a ready-to-use `sacinp.*` file with all **JOINT** and **MEMBER** cards pre-populated, saving hours of manual modeling.

## Features

- **Automatic file detection** — picks up the single `.dxf` file found in the script's folder.
- **mm → m scaling** — DXF coordinates (mm) are converted to SACS units (m) automatically.
- **Smart node merging** — endpoints closer than ~1 mm are merged into the same joint.
- **Sequential node naming** — 4-digit zero-padded IDs (`0001`, `0002`, ...), up to 9999 nodes.
- **Layer → Group mapping** — each DXF layer name is cleaned and truncated to 3 characters to generate the corresponding SACS `GRUP` ID.
- **Interactive proximity check** — set a distance threshold (default 10 mm) and get flagged if any two nodes are suspiciously close, catching CAD snapping errors before you run the analysis.
- **Datagen-ready formatting** — fixed-width spacing for `JOINT`, `MEMBER`, and `LOAD` cards.
- **Default self-weight** — a standard `DEAD` load block (gravity coefficient `1.0000`, `-Z` direction) is appended automatically.

## CAD Drawing Guidelines

1. **LINE entities only** — no polylines, arcs, or 3D solids.
2. **Draw in millimeters** — the script assumes 1 unit = 1 mm.
3. **Use Endpoint snap** when joining lines, to avoid duplicate nodes.
4. **Export as DXF** — any recent version (AutoCAD 2018+) works.

## How to Run

1. Install the dependency: `pip install ezdxf`
2. Place your `.dxf` file in the **same folder** as `DXF_to_SACS.py` (only one DXF file allowed per run).
3. Run: `python DXF_to_SACS.py`
4. A `sacinp.<filename>` file is generated in the same folder.

> A ready-to-use `.exe` version (no Python required) is also available under **Releases**.

## Sample Files

The `example/` folder contains two test DXF files:

- **`sample_frame.dxf`** — a clean wireframe with multiple layers, to test the **layer-to-group mapping**.
- A second file with two nodes placed abnormally close (but not snapped), to test the **proximity check**.

## Limitations

- Supports `LINE` geometry only.
- Section properties and material groups must still be assigned manually in SACS.
- **9999-node maximum**, due to the 4-digit sequential node naming.
- Tested on **SACS 2025** — older versions may require different card spacing.

---

*Developed by FM using AI – 2026 (v1.2.1)*
