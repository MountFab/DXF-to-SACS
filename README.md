# DXF-to-SACS
A Python utility to convert 3D DXF line-geometry into SACS (Betley) structural input files, featuring an interactive node-distance quality check.
# Why?

SACS does not natively allow you to import standard CAD files directly. Traditionally, engineers must manually recreate structural geometry node-by-node inside the software or rely on the built-in parametric wizard, which is heavily limited to standard offshore jacket structures and lacks the flexibility needed for custom or complex topside framing. 

This Python utility eliminates this limitation. It automatically reads an AutoCAD DXF file and generates a compatible SACS input text file (`sacinp.*`), pre-populating all **JOINT** and **MEMBER** cards, saving time of manually modeling.

---

## 🚀 Features & Quality Check
* **Automatic Scaling:** Converts CAD geometry from millimeters (mm) to SACS meters (m).
* **Smart Node Merging:** Identifies overlapping endpoints and automatically merges them into a single joint.
* **Interactive Quality Check:** Prompts you to set a distance threshold (e.g., 10mm). If the script detects nodes that are dangerously close to each other, it alerts you to potential CAD snapping errors before you run your analysis.
* **Strict Column Alignment:** Automatically formats the output text file using SACS's mandatory fixed-width spacing for `JOINT`, `MEMBER`, and `LOAD` cards, ensuring zero syntax errors upon import.
* **Sequential Node Naming (`J001`, `J002`, ...):** Names joints sequentially using a 3-digit padding system. This cleanly isolates script-generated nodes from any structural joints you might manually add inside SACS later.
* **Pre-configured DEAD Load Case:** Automatically appends a standard `DEAD` load block to the input file with a gravity multiplier coefficient of `1.0000` acting in the `-Z` direction, saving you from setting up basic self-weight cards manually.  

---

## 📐 CAD Drawing Guidelines
To ensure a perfect conversion, please prepare your DXF file following these simple rules:
1. **Use LINE Entities Only:** The script reads standard `LINE` elements. Ensure your wireframe structural model doesn't use polylines, arcs, or 3D solids.
2. **Draw in Millimeters:** The script assumes your CAD workspace is set up in millimeters ($1 \text{ unit} = 1 \text{ mm}$).
3. **Use Object Snap:** Always use `Endpoint` snap when joining lines. This prevents the generation of unwanted duplicate nodes.
4. **DXF Format:** Export or save your AutoCAD file as a `.dxf` file using the **Save As** (`SAVEAS`) command. Any recent DXF version (e.g., AutoCAD 2018 DXF or newer) works perfectly with the script.

---

## 🔒 Security & Trust (EXE vs Python)
Because company PCs often have strict IT policies regarding unknown executable files, you have two ways to run this tool:

### Option A: The Ready-to-Use Executable (Fastest)
1. Go to the **Releases** section on the right side of this page.
2. Download the compressed archive **`v3.1.0.zip`**. It contains both the executable (`DXF_to_SACSv2.exe`) and a sample CAD file (`sample_frame.dxf`) ready for immediate testing.
3. Place your `.dxf` file and the `.exe` in the **same folder**.
4. Double-click the `.exe` to run it. *(Note: Windows SmartScreen might flag it as an "unknown publisher" because it lacks a paid digital certificate. You can safely bypass this).*
5. A `sacinp.` file will be created in the same folder.

### Option B: Run the Python Script (Fully Transparent)
If you prefer not to run pre-compiled binaries on your machine, you can inspect and run the raw Python code directly:
1. Download `DXF_to_SACS.py`.
2. Install the required library via terminal: `pip install ezdxf`
3. Run the script: `python DXF_to_SACS.py`
4. **Build Your Own EXE:** If you prefer the convenience of an executable but want 100% security transparency, you can easily compile the raw script yourself using the `pyinstaller` library. It takes less than 5 minutes! Simply ask your preferred AI assistant to guide you through the process.

💡 **Tip:** You can find a ready-to-use CAD file named `sample_frame.dxf` inside the `example/` folder of this repository to test the script immediately!

---

## ⚠️ Current Limitations
* Supports only `LINE` geometry (Structural wireframes).
* SACS section properties and material groups must still be assigned manually inside SACS after importing the geometry.
* 999-Node Maximum due to the `J001`–`J999` sequential nomenclature (3-digit padding), the script currently supports a maximum of 999 unique nodes per DXF file to strictly preserve the SACS card spacing format.

---
*Developed by FM – 2026*
