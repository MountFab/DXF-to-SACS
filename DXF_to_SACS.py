import ezdxf
import os
import sys
import datetime
import math 

# =================================================================
# GLOBAL CONFIGURATIONS
# =================================================================
ROUND_DECIMALS = 3       # Base tolerance to merge identical nodes (1 mm)

# =================================================================
# AUTOMATIC DXF FILE SEARCH AND NAME GENERATION
# =================================================================

# 1. Determine the folder where the executable (or script) is located
if getattr(sys, 'frozen', False):
    # If the program is running as an .exe
    script_dir = os.path.dirname(sys.executable)
else:
    # If the program is running as a normal .py script
    script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Search for all files ending with '.dxf' in this folder
dxf_files = [f for f in os.listdir(script_dir) if f.lower().endswith('.dxf')]

# 3. Safety checks
if len(dxf_files) == 0:
    print("ERROR: No .dxf files found in this folder!")
    print("Make sure you have placed the DXF file in the same folder as this program.")
    input("Press ENTER to exit...")
    sys.exit()

elif len(dxf_files) > 1:
    print("ATTENTION: There are too many .dxf files in this folder!")
    print("Leave ONLY ONE DXF file to avoid incorrect conversions.")
    input("Press ENTER to exit...")
    sys.exit()

# 4. Set names automatically
FILE_INPUT = dxf_files[0]
nome_base = os.path.splitext(FILE_INPUT)[0] 
FILE_OUTPUT = f"sacinp.{nome_base}"

DXF_FILE = os.path.join(script_dir, FILE_INPUT)
OUTPUT_FILE = os.path.join(script_dir, FILE_OUTPUT)

print(f"Found file: {FILE_INPUT}")

# =================================================================
# INTERACTIVE USER THRESHOLD CONFIGURATION
# =================================================================
print("\n" + "=" * 65)
print(" QUALITY CHECK CONFIGURATION")
print("=" * 65)
user_input = input("Set a threshold for the node distance check [mm] (Press ENTER for default 10.0 mm): ").strip()

if user_input == "":
    SOGLIA_AVVISO_MM = 10.0
    print("Using default threshold: 10.0 mm")
else:
    try:
        SOGLIA_AVVISO_MM = float(user_input)
        print(f"Threshold successfully set to: {SOGLIA_AVVISO_MM} mm")
    except ValueError:
        SOGLIA_AVVISO_MM = 10.0
        print("Invalid input detected! Falling back to default threshold: 10.0 mm")

print("\nStarting processing...\n")

# Opening DXF file
doc = ezdxf.readfile(DXF_FILE)
msp = doc.modelspace()

node_dict = {} 
nodes = [] 
members = [] 
next_node = 1 

def get_node(point):  
    global next_node
    
    # UNIT CHANGE [mm --> m]
    x_m = point[0] / 1000.0
    y_m = point[1] / 1000.0
    z_m = point[2] / 1000.0

    # Rounding to avoid immediate duplicates (under 1 mm)
    key = (
        round(x_m, ROUND_DECIMALS),
        round(y_m, ROUND_DECIMALS),
        round(z_m, ROUND_DECIMALS),
    )

    if key not in node_dict:
        node_name = f"J{next_node:03d}"
        node_dict[key] = node_name 
        nodes.append((node_name, key[0], key[1], key[2]))
        next_node += 1

    return node_dict[key]

def format_sacs_coord(val):
    if val == 0.0:
        s = "0."
    else:
        s = f"{val:.3f}"
        if s.endswith(".000"):
            s = str(int(val)) + "."
            
    return f"{s:>7}"
# Storage unit for layer to Group mapping
detected_groups = set()
# list to sotre member in order
members_database = []

# Reading all LINE entities
for line in msp.query("LINE"):
    p1 = line.dxf.start
    p2 = line.dxf.end
    
    n1 = get_node(p1)
    n2 = get_node(p2)
    members.append((n1, n2))

    # --- STEP 2: STRING MANIPULATION & STORAGE ---
    # Get the raw layer name from AutoCAD (e.g., "Frames Upper")
    raw_layer = line.dxf.layer  
    
    # Clean it: uppercase, replace spaces with underscores, slice the first 3 characters
    sacs_group = raw_layer.strip().upper().replace(" ", "_")[:3] 
    
    # Add the 3-letter group to our unique set
    detected_groups.add(sacs_group)
    
    # Pack the member data into a tuple and append it to our list
    members_database.append((n1, n2, sacs_group))

# =================================================================
# QUALITY CHECK: CLOSE NODES DETECTION (POTENTIAL CAD ERROR)
# =================================================================
nodi_troppo_vicini = []
soglia_metri = SOGLIA_AVVISO_MM / 1000.0

# Compare each node with all subsequent ones to calculate distance
for i in range(len(nodes)):
    for j in range(i + 1, len(nodes)):
        id1, x1, y1, z1 = nodes[i]
        id2, x2, y2, z2 = nodes[j]
        
        # 3D Euclidean distance formula
        dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)
        
        if dist <= soglia_metri:
            dist_mm = dist * 1000.0
            nodi_troppo_vicini.append((id1, id2, dist_mm))

# Retrieve current date in dd/mm/yyyy format
data_oggi = datetime.datetime.now().strftime("%d/%m/%Y")
num_nodi = len(nodes)
num_elementi = len(members)

# Writing SACS geom file
with open(OUTPUT_FILE, "w") as f:
    # 1. INITIAL PART: Date and model statistics
    f.write("**************************************************************************** \n")
    f.write(f"* {data_oggi} - Node number : {num_nodi} - Element Number:{num_elementi}\n")
    
    # 2. LDOPT BLOCK
    f.write("**************************************************************************** \n")
    f.write("LDOPT\n")
    
    # 3. OPTIONS BLOCK
    f.write("**************************************************************************** \n")
    f.write("OPTIONS      MN              1 1\n")
    
    # 4. DISPLAY LOAD COMBINATION / LCSEL BLOCK
    f.write("*******************************************************************************\n")
    f.write("* DISPLAY LOAD COMBINATION                      *\n")
    f.write("***************************************************************************** \n")
    f.write("LCSEL\n")
    
    # 5. SECT AND GROUP BLOCK
    f.write("**************************************************************************** \n")
    f.write("SECT\n")
    f.write("**************************************************************************** \n")
    f.write("GRUP\n")

    # --- STEP 3: WRITING GROUPS FIRST (Fixed f_out to f) ---
    # 'sorted()' organizes our unique groups alphabetically (e.g., COO, COV, FRM)
    for group in sorted(detected_groups):
        # 'GRUP' (4 chars) + 2 spaces = group name starts precisely at column 7
        f.write(f"GRUP {group}\n")

    f.write("**************************************************************************** \n")
    f.write("MEMBER\n")

    # --- STEP 4: WRITING MEMBERS (Fixed f_out to f) ---
    # We unpack the 3 items from each tuple inside our list
    for n_start, n_end, group_id in members_database:
        riga_member = f"MEMBER {n_start:>4}{n_end:>4} {group_id:<3}\n"
        f.write(riga_member)
    
    # Note: Old "6. MEMBER BLOCK" loop removed here to prevent duplicate entries!
    
    # 7. SEPARATION LINE BETWEEN MEMBER AND JOINT
    f.write("**************************************************************************** \n")
    
    # 8. JOINT BLOCK
    f.write("JOINT\n")
    for node_name, x, y, z in nodes:
        x_str = format_sacs_coord(x)
        y_str = format_sacs_coord(y)
        z_str = format_sacs_coord(z)
        f.write(f"JOINT {node_name} {x_str}{y_str}{z_str}\n")
    
    # 9. LOAD BLOCK (AFTER JOINT)
    f.write("***************************************************************************** \n")
    f.write(" *                                  LOAD                                            \n")
    f.write("*****************************************************************************\n")
    f.write("LOAD\n")
    
    # Lines added for the DEAD LOAD block
    f.write("***************************************************************************** \n")
    f.write("***                            model DEAD LOAD                                  \n")
    f.write("***************************************************************************** \n")
    f.write("LOADCNDEA1         1.0000                     DEAD                            \n")
    f.write("DEAD                                                                            \n")
    f.write("DEAD       -Z                               M BML  \n")
    
    # 10. LOAD COMBINATION / LOADCN BLOCK (AFTER LOAD)
    f.write("***************************************************************************** \n")
    f.write(" *                            LOAD COMBINATION                                 \n")
    f.write("*****************************************************************************\n")
    f.write("LOADCN\n")
    
    # 11. STANDARD SACS CLOSURE
    f.write("END\n")
    f.write(" **JNCV** 0 0 0 0 0 0 0 0\n")
    f.write("END\n")

print(f"File {OUTPUT_FILE} SUCCESSFULLY GENERATED! Total nodes: {num_nodi}, Total members: {num_elementi}")

# PRINT WARNINGS IF CLOSE NODES ARE FOUND BASED ON USER THRESHOLD
if nodi_troppo_vicini:
    print("\n" + "!" * 80)
    print(f"⚠️  WARNING : POTENTIAL CAD DRAWING ERRORS DETECTED!")
    print(f"The following nodes are LESS than {SOGLIA_AVVISO_MM} mm apart:")
    for id1, id2, d_mm in nodi_troppo_vicini:
        print(f"  - {id1} and {id2} -> Distance: {d_mm:.1f} mm")
    print(f"Advice: Check in the CAD if lines were snapped correctly. If you are sure of the drawing, ignore this warning.")
    print("!" * 80 + "\n")

input("\nProcessing complete! Press ENTER to close this window...")

#   FM – 07/2026 v3.1.0