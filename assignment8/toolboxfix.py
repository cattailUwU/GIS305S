import arcpy
import os


def buffer_layer(input_gdb, layer_name, dist_miles, output_gdb):
    """
    Buffer the feature class `layer_name` inside `input_gdb` by `dist_miles` miles,
    writing the result into `output_gdb`. Returns the full path to the buffer FC.
    """
    in_fc = os.path.join(input_gdb, layer_name)
    out_name = f"{layer_name}_buf"
    out_fc = os.path.join(output_gdb, out_name)

    distance = f"{dist_miles} Miles"
    arcpy.Buffer_analysis(
        in_fc, out_fc, distance,
        line_side="FULL",
        line_end_type="ROUND",
        dissolve_option="ALL"
    )
    return out_fc


def intersect_layers(layers, output_name):
    """
    Intersect the list of buffer layers into a new feature class named `output_name`
    in the current workspace.
    """
    arcpy.Intersect_analysis(layers, output_name)


def main():
    # ─── SCRIPT TOOL PARAMETERS ────────────────────────────────────────────────
    # 0: River buffer distance (miles)      → Data Type: Double
    # 1: Cities buffer distance (miles)     → Data Type: Double
    # 2: Intersect output feature class name→ Data Type: String
    river_dist = arcpy.GetParameterAsText(0)
    city_dist = arcpy.GetParameterAsText(1)
    intersect_name = arcpy.GetParameterAsText(2)

    # ─── HARDCODED PATHS ─────────────────────────────────────────────────────────
    # (You can promote these to parameters too if you like)
    input_gdb = r"C:\Users\paint\Downloads\Admin\Admin\AdminData.gdb\USA"
    project_gdb = r"C:\Users\paint\Documents\ArcGIS\Projects\BodelMuilder\BodelMuilder.gdb"

    # ─── ENVIRONMENT SETUP ───────────────────────────────────────────────────────
    arcpy.env.workspace = project_gdb
    arcpy.env.overwriteOutput = True

    # ─── BUFFER RIVERS ───────────────────────────────────────────────────────────
    buf_rivers = buffer_layer(input_gdb, "us_rivers", river_dist, project_gdb)
    arcpy.AddMessage(f"✅ River buffer created: {buf_rivers}")

    # ─── BUFFER CITIES ───────────────────────────────────────────────────────────
    buf_cities = buffer_layer(input_gdb, "cities", city_dist, project_gdb)
    arcpy.AddMessage(f"✅ City buffer created: {buf_cities}")

    # ─── INTERSECT ───────────────────────────────────────────────────────────────
    intersect_layers([buf_rivers, buf_cities], intersect_name)
    arcpy.AddMessage(f"🔀 Intersect feature class created: {intersect_name}")

    # ─── ADD TO MAP & SAVE ───────────────────────────────────────────────────────
    aprx = arcpy.mp.ArcGISProject("CURRENT")  # hook into the open Pro project
    m = aprx.listMaps()[0]
    intersect_path = os.path.join(project_gdb, intersect_name)
    m.addDataFromPath(intersect_path)

    aprx.save()
    arcpy.AddMessage("🎉 Script complete—project saved with new layers!")


if __name__ == "__main__":
    main()
