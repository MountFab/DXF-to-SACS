# DXF-to-SACS

A Python utility to convert 3D DXF line-geometry into SACS2025 (Bentley) structural input files, featuring an interactive node-distance quality check and layer-to-group mapping.

# Why?

SACS does not natively allow you to import standard CAD files directly. Traditionally, engineers must manually recreate structural geometry node-by-node inside the software or rely on the built-in parametric wizard, which is heavily limited to standard offshore jacket structures and lacks the flexibility needed for custom or complex topside framing. 

This Python utility eliminates this limitation. It automatically reads an AutoCAD DXF file and generates a compatible SACS input text file (`sacinp.*`), pre-populating all **JOINT** and **MEMBER** cards, saving hours of manual modeling.

---

## 🚀 Features & Version History

### 🔹 V1.2.0 (Current Version)
* **Layer Characterization & Group Mapping:** Automatically reads AutoCAD layer names and maps them directly to SACS **Group** IDs, letting you define structural group properties based on your CAD layering system.

### 🔹 V1.1.3
* **Interactive Proximity Self-Check:** Prompts you to set a geometric distance threshold (e.g., 10mm) and alerts you if nodes are dangerously close to each other, catching potential CAD snapping errors before you run your structural analysis.

### 🔹 V1.1.2
* **Datagen Optimization:** Automatically formats and spaces the input text file for a clean, organized, and perfectly aligned view inside the SACS **Datagen** module.
* **Default Self-Weight:** Automatically appends a standard `DEAD` load block with a gravity multiplier coefficient of `1.0000` acting in the `-Z` direction, eliminating the need to set up basic self-weight cards manually.

### 🔹 Core Capabilities
* **Automatic Scaling:** mm (CAD) → m (SACS).
* **Smart Node Merging:** overlapping endpoints are automatically merged into a single joint.
* **Strict Column Alignment:** fixed-width spacing for `JOINT`, `MEMBER`, and `LOAD` cards, ensuring zero syntax errors upon import.
* **Sequential Node Naming (`J001`, `J002`, ...):** 3-digit padding, cleanly isolating script-generated nodes from any joints you might add manually inside SACS later.

---

## 📐 CAD Drawing Guidelines

To ensure a perfect conversion, please prepare your DXF file following these simple rules:

1. **Use LINE Entities Only:** The script reads standard `LINE` elements. Ensure your wireframe structural model doesn't use polylines, arcs, or 3D solids.
2. **Draw in Millimeters:** The script assumes your CAD workspace is set up in millimeters (1 unit = 1 mm).
3. **Use Object Snap:** Always use `Endpoint` snap when joining lines. This prevents the generation of unwanted duplicate nodes.
4. **DXF Format:** Export or save your AutoCAD file as a `.dxf` file using the **Save As** (`SAVEAS`) command. Any recent DXF version (e.g., AutoCAD 2018 DXF or newer) works perfectly.

---

## 🔒 Security & Trust (EXE vs Python)

Because company PCs often have strict IT policies regarding unknown executable files, you have two ways to run this tool:

### Option A: Run the Python Script (Recommended)

If you already have Python installed, this is the most transparent and flexible option.
Just place your `.dxf` file in the **same folder** as the script — it will be picked up automatically.

1. Download `DXF_to_SACS.py`.
2. Install the required library: `pip install ezdxf`.
3. Copy your `.dxf` file into the **same folder** as `DXF_to_SACS.py`
4. Run the script: `python DXF_to_SACS.py`
5. A fully compatible `sacinp.*` file will be created in the same folder.

---

### Option B: Ready-to-Use Executable

For users who prefer not to run Python directly.

1. Go to the **Releases** section on the right side of this page.
2. Download **`v1.2.0.zip`** and extract it anywhere on your computer.
3. Copy your `.dxf` file into the **same folder** as `DXF_to_SACS.exe`.
4. Double-click `DXF_to_SACS.exe` and follow the on-screen prompts.

> ⚠️ Windows SmartScreen may flag the file as "unknown publisher" due to the absence of a paid digital certificate. Click **"More info" → "Run anyway"** to proceed safely.

---

## 🧪 Sample Files & Testing

Inside the `example/` folder you'll find a set of ready-to-use DXF files so you can test the script immediately without needing your own CAD model:

* **`sample_frame.dxf`** — a clean structural wireframe with multiple distinct AutoCAD layers, useful for testing the **Layer Characterization & Group Mapping** feature (V1.2.0). Each layer maps to a different SACS Group ID, so you can see the mapping logic in action.
* **A second sample file with an intentional geometry error** — two nodes placed abnormally close together (but not perfectly overlapping/snapped). Use this file to test the **Interactive Proximity Self-Check** (V1.1.3): run the script, set a distance threshold, and confirm the tool correctly flags the suspicious node pair before you proceed to SACS.

💡 **Tip:** Running both sample files is the fastest way to confirm your installation (EXE or Python) is working correctly before feeding in your own project geometry.

---

## ⚠️ Current Limitations
* Supports only `LINE` geometry (Structural wireframes).
* SACS section properties and material groups must still be assigned manually inside SACS after importing the geometry.
* **999-Node Maximum:** due to the `J001`–`J999` sequential nomenclature (3-digit padding), the script currently supports a maximum of 999 unique nodes per DXF file to strictly preserve the SACS card spacing format.
* The Script is tested on the **2025 SACS** version, older version may have different spacing requirement for the elements set-up. 

---

## 🤝 Contributing & Feedback

Found a bug, have a feature request, or want to contribute improvements? Feel free to open an **Issue** or submit a **Pull Request** on this repository — feedback from real-world SACS/DXF workflows is always welcome.

---

*Developed by FM using IA – 2026*
