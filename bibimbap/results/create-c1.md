# BIBIMBAP C1 perfect-answer check: the 15 CREATE tasks

**Method.** For each CREATE row in `all_questions.csv`, I worked out the correct edit from the prompt and the model geometry, without reading the test's expectations first. I built it with `ifcopenshell.api` the way a modelling tool would: proper class, storey containment, an extruded SweptSolid body, an IfcOpeningElement with IfcRelVoidsElement and IfcRelFillsElement for doors, and an opening for the slab hole. I then scored it with BIBIMBAP's own `data.tests.<name>.execute_test`, where the score is the mean of the metrics. Some tasks also got alternative variants: a different reasonable interpretation, or a different but equally correct modelling style.

**ifcopenshell version matters.** `requirements.txt:1` pins `ifcopenshell~=0.8.3.post2`. The container has 0.9.0. I scored everything twice:
- with the pinned 0.8.3.post2, run from the official wheel extracted into `create/ios083/` and put on `PYTHONPATH`. Nothing was installed system-wide.
- with the installed 0.9.0.

The main table uses the pinned version. Under 0.9.0 **every** answer scores 0 (see section 2).

Scripts are in `create/`: `lib.py` (builders), `build.py` (all tasks and variants), `build_bonsai_doors.py`, `build_probe.py`, `score.py` (scoring plus debug: bbox, sub-checks, clash partners) and `existing_door_check.py`. The edited IFCs are in `create/out/`. Raw metrics are in `create/metrics_ios0.8.3.post2.json` and `create/metrics_ios0.9.0.json`.

## 1. Results (pinned ifcopenshell 0.8.3.post2)

| task | prompt (short) | what I created (variant A = primary answer) | metrics: exists / location / dims / integrity | score | full marks? | if not: cause, code line, whose fault |
|---|---|---|---|---|---|---|
| test_01 | 2×1 m door in wall 2UsX…Hvf | IfcDoor 1.0 w × 2.0 h (box body, 200 mm deep), centred in the wall at x=24.3, sill 0. The 1.0×0.22×2.0 IfcOpeningElement voids the wall and the door fills it. Contained in L1. | 1 / 1 / 1 / 1.0 | **1.00** | yes | **Variant B** (Bonsai's parametric `add_door_representation`, same 1.0×2.0 nominal size, default lining and casings) scores **0.69**. (a) `right_dimensions`=0: `get_shape_dims` measures the casing-inclusive extent 1.05×2.025. 1.05−1.0 = 0.0500000004 > `DIM_TOL=0.05` (test_01.py:60, 95-97). (b) integrity 0.75: the door clashes with **its own opening** (clash_utils.py:186-214 does not exclude IfcOpeningElement; test_01.py:107). Fault: **test**. A door filling its own opening is the intended IfcRelFillsElement topology, and nominal size is in OverallWidth/OverallHeight, not in the trim extents. The dataset's own Revit door shows the same thing (section 3). |
| test_02 | slab 10×5 m, 0.2 thick, bottom & centre at (−30,0) | IfcSlab FLOOR, x −35..−25, y −2.5..2.5, z 0..0.2, in L1 | 1 / 1 / 1 / 1.0 | **1.00** | yes | n/a |
| test_03 | 5×5 m opening at centre of slab 11kJ…CVP | IfcOpeningElement 5×5, centred on the slab bbox centre (5.0, 5.0125). It goes exactly through the slab, z 3.8..4.1, and IfcRelVoidsElement links it to the slab. | 1 / 1 / 1 / 1.0 | **1.00** | yes | **Variant B** has the same opening made 10 mm deeper on each side (z 3.79..4.11). This is the usual practice to avoid coplanar boolean faces. It scores **0.92**: integrity 0.67 because the opening "clashes" with **IfcSpace 274** below the slab (clash_utils.py:186-214 includes IfcSpace and IfcOpeningElement; test_03.py:116). Fault: **test**. Both elements are non-physical (a void and a room volume), so the overlap is not a clash. |
| test_04 | column 3 m high at (12, 8) | IfcColumn 300×300, centred (12, 8), z 0..3, L1 | 1 / 1 / 1 / 1.0 | **1.00** | yes | n/a |
| test_05 | 15 m wall beginning at (0,−10) | IfcWall from (0,−10) to (15,−10) (+X, since no direction is given), 200 mm, 3.6 m (storey height), L1 | 1 / 1 / 1 / 1.0 | **1.00** | yes | n/a. The test accepts any direction. |
| geometry_test_01 | 0.2 m slab on upper outer edges of 4 columns | IfcSlab 0..3 × 0..3 (outer faces of the corner columns), z 3.0..3.2. Variant A is in L2 (elev. 3.0), variant B in L1. | 1 / 1 / 1 / 1.0 | **1.00** | yes (both) | n/a. Touching the column tops does not count as a clash (`allow_touching=False` ignores face contact). |
| geometry_test_02 | column at centroid of the 4 walls | IfcColumn 300×300 at (2.5, 2.5), z 0..3.0, L1 | 1 / 1 / 1 / 1.0 | **1.00** | yes | n/a |
| geometry_test_03 | door in wall north (+Y) of wall 3YQ$…$hw | Wall north of $hw (y −1.0..−0.8) is $ig (y 1.5..1.7). IfcDoor 0.9×2.1 at its middle (x=0), sill 0, with opening, voids and fills; IFC2X3. | 1 / 1 / 1 / 1.0 | **1.00** | yes | Bonsai's parametric door could not be built in this IFC2X3 file: `add_door_representation` raises ValueError in shape_builder.mirror. This is an ifcopenshell.api limitation, not a test issue. |
| geometry_test_04 | IfcSpace in the area left of column 3A5G… | IfcSpace x 0.2..6.35, y 0.2..6.7, z 0..3.0 (the clear area bounded by the walls and the column/partition line). **Aggregated** to storey L1 (IfcRelAggregates), as the IFC rules require and as every existing IfcSpace in the dataset is. | 1 / 1 / 1 / **0.667** | **0.917** | **no** | `check_spatial_containment` (create_utils.py:149-161, called at geometry_test_04.py:104) only accepts IfcRelContainedInSpatialStructure. An IfcSpace is a spatial element and is placed in the storey via IfcRelAggregates. IFC2X3 has no `ContainedInStructure` inverse on IfcSpace, so `ifcopenshell.api spatial.assign_container` refuses with AttributeError. The source files' own spaces (e.g. 01_02_001, 01_02_003, basic_tasks) are all aggregated, not contained. Fault: **test**. Variant B adds a hand-made IfcRelContainedInSpatialStructure as well (against the schema's rule for that relationship) and gets 1.00, so the test rewards the non-standard model. |
| geometry_test_05 | 5 m wall from (10,5) in direction (1,0) | IfcWall with axis (10,5)→(15,5), 200 mm centred on the axis, 3.0 m, in "My Storey" (empty.ifc) | 1 / 1 / 1 / 1.0 | **1.00** | yes | n/a |
| topological_test_01 | wall to fully enclose room 3_DH…4s | Room is x 0.2..4.85, y 0.2..6.2. The W, S and N walls exist; the east side is open. New IfcWall on axis x=4.95 from y 0.2 to 6.2 (between the S and N walls, which already cover the corners), 200 mm, h 2.7, L1. This is the same as wall 1IMY… in 01_02_002. | 1 / 1 / 1 / 1.0 | **1.00** | yes | n/a |
| topological_test_02 | column in the inner space of the 4 walls | IfcColumn 300×300 at the inner-space centre (2.525, 3.2), z 0..2.7 (floor to soffit), L1 | 1 / 1 / 1 / 1.0 | **1.00** | yes | n/a |
| topological_test_03 | wall separating "rooms" 0rMM…RaK, 0rMM…Rcx | The two GUIDs are **walls** (stubs at y 3.1..3.3, x 0.2..1.7 and 3.35..4.85), not rooms. The real rooms are spaces 133/134 north and south of the stubs. Correct edit: fill the 1.65 m gap, IfcWall x 1.7..3.35, y 3.1..3.3, h 2.7, L1. | 1 / 1 / 1 / 1.0 | **1.00** | yes | No failure. **Prompt issue**: the IDs are walls, and the test uses their bbox centres as "room centres". The A answer still passes. Leniency: variant B, a full-length wall 0.2..4.85 that exactly duplicates both stubs, also gets 1.00. The surface-based collision check does not see coincident volumes. A probe wall shifted 50 mm is caught (0.92). |
| topological_test_04 | slab that closes the 4 walls | A ceiling slab (z 2.7..3.0) already exists and the floor slab is missing. New IfcSlab FLOOR 300 mm, 0..5.05 × 0..6.4 (the walls' outer outline), z −0.3..0, L1 | 1 / 1 / 1 / 1.0 | **1.00** | yes | n/a |
| topological_test_05 | door connecting inner space with outdoors | IfcDoor 0.9×2.1 in exterior south wall 3Vyq…AwAc at x 1.05..1.95, sill 0, with opening, voids and fills; L1 | 1 / 1 / 1 / 1.0 | **1.00** | yes | **Variant B** (Bonsai parametric door) scores **0.92**: integrity 0.67 from a clash with its own opening (clash_utils.py:186-214; topological_test_05.py:126). Fault: **test**, same cause as test_01 B. |

**Summary of the primary answers (pinned version): 14/15 get full marks, and geometry_test_04 gets 0.917.**
Equally correct alternatives lose points in 3 more tasks (test_01, test_03, topological_test_05) for the two test-side reasons below.

## 2. Under ifcopenshell 0.9.0 (installed in this container) every CREATE answer scores 0

- **14 of 15 tests raise an exception**, which `benchmark.py:264-272` turns into a score of 0. `clash_utils.py:256` `tree.add_element(iterator.get())` fails with `RuntimeError: Tree backend 'opencascade.brep' requires native brep elements`. Every CREATE test calls `check_clash_integrity`. The only one that does not raise is test_01, because it returns before reaching the clash call (next bullet).
- **test_01 returns all-zero metrics** before the clash check (test_01.py:66-70). `get_bbox(wall)` raises because 0.9.0's `create_shape(settings, product)` processes the first representation. On these Revit walls that is `'Axis'` (Curve2D), not `'Body'`. Every IfcWall in basic_tasks.ifc fails this way. Under 0.8.3 the same call returns the Body geometry.
- Cause: environment/version, not the answers. Anyone reproducing with ifcopenshell ≥ 0.9 gets 0 on all CREATE tasks. Any earlier audit run in this container with 0.9.0 that touched `get_bbox` or `check_clash_integrity` should be re-checked under the pin.

## 3. Distinct causes of correct answers losing points

1. **Spatial containment check is wrong for IfcSpace** (create_utils.py:149-161, used at geometry_test_04.py:104). It requires IfcRelContainedInSpatialStructure. The standard relation for a space is IfcRelAggregates, and in IFC2X3 the API cannot even create the containment. This is the only failure for a primary answer. Fault: test.
2. **The clash sub-check includes non-physical products and the element's own opening** (`_iter_clashable_products`, clash_utils.py:186-214, called with no `exclude_classes` from every CREATE test). Two consequences:
   - A door or window whose frame or casing extends past its own opening, as Bonsai's parametric door and Revit families do, "clashes" with its own IfcOpeningElement.
   - An opening made slightly deeper than its host "clashes" with the IfcSpace beside it.

   Evidence from the dataset itself: under this same check, the existing Revit door `11kJ…DY7` in basic_tasks.ifc clashes with its own opening and with IfcSpace 131. The existing window `11kJ…DbS` clashes with its own opening (`existing_door_check.py`). Fault: test.
3. **Door size measured from geometry extents with ±0.05 m** (test_01.py:60, 89-97). Doors with lining or casing exceed the nominal size: the Bonsai default door is +50 mm/+25 mm, and the dataset's own 750×2100 Revit door measures 0.85×2.2. Such doors fail even when OverallWidth/OverallHeight are exactly 1.0/2.0. Fault: mostly test (it ignores the nominal attributes). The bare-box door passes.
4. **Version dependency**: under ifcopenshell 0.9.0 every answer scores 0 (section 2). This is environment, not the answers or the test logic. The repo pins 0.8.3.post2.

Side observations (leniency, not rejections of correct answers):
- topological_test_03's prompt names two walls as "rooms".
- The collision check misses an exactly duplicated volume (the full-length wall over the stubs scores 1.0).
- topological_test_05 accepts a door in any wall, interior or exterior.
- touching contact is never counted as a clash. Doors sitting on floor slabs and slabs resting on column tops are fine.

## 4. Honesty notes
- I built a correct primary answer for every task.
- The only answer I could not build is the Bonsai-style door variant for geometry_test_03, because the ifcopenshell.api error happens before scoring.
- Validation: `ifcopenshell.validate` (schema, no express rules) finds no issues in any primary output beyond issues already in the source files: IfcMaterialProfileSetUsage without AssociatedTo in basic_tasks.ifc and 01_01_001.ifc. I set the two attributes the API leaves empty myself: IFC4X3 `IfcIndexedPolyCurve.SelfIntersect` and IFC2X3 OwnerHistory / `InteriorOrExteriorSpace`.
- Using the pinned version: I downloaded the official 0.8.3.post2 wheel (it went to /tmp/x, then I moved it to `create/`) and unzipped it into `create/ios083`. I used it only through `PYTHONPATH`, without installing it.
