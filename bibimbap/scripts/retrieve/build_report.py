import json
runs = json.load(open('test_runs.json'))
# task: (prompt short, key, tol, class, method/answer text, note)
T = [
('test_06','Area of room 2UsX..Hyo (m2)','150.0','abs<0.1','MATCH','150.0 (IfcSpace Body: 10.0x15.0 rectangle; = clear area between walls 38.9-48.9 / 0-15.0)','No Qto/BaseQuantities in file.'),
('test_07','Length of wall 22hy..SKC (m)','10.2','abs<0.1','MATCH','10.2 (Axis polyline 10200 mm = extrusion XDim; free-standing wall, no junctions)',''),
('test_08','Volume of room 2UsX..Hyo (m3)','457.2','abs<0.1','MATCH','457.2 (space Body 150 m2 x 3.048 m)','Space is 3.048 m high while surrounding walls are 3.6 m and no slab is modelled; 150 x 3.6 = 540 would fail. Key follows the modelled space.'),
('test_09','Centre distance of columns ..SMr / ..SMu (m)','10.0','abs<0.1','MATCH','10.0 (bbox centres x=-20.0 and x=-10.0, same y)','Column names say 300x450 but geometry is 200x200; irrelevant to centre distance.'),
('test_10','GlobalId of the 5 m wall','22hyxvAPr65PFt9WZfHSP3','exact','MATCH','22hyxvAPr65PFt9WZfHSP3 (axis 5000 mm; only wall of 5 m among 16)',''),
('geometry_test_06','Longest side of the non-square room (m)','7.2 (accepts 6.9-7.4)','range [6.9,7.4]','MATCH','7.2 centre-line (partition axis x=6.4 to wall axis x=13.6); inner clear 7.0; outer 7.4','No IfcSpace in file: rooms inferred from walls (left room 6.1x6.1 clear = square; right room 7.0x6.1). Range accepts all three readings. Docstring mentions half score but the code returns a plain True for anything in range.'),
('geometry_test_07','Id of the shortest wall','1pkLoAx5P7Lwxnk7MMv3Lz','exact','MATCH','1pkLoAx5P7Lwxnk7MMv3Lz (axis 2.1 m; next shortest 2.7 m)',''),
('geometry_test_08','Distance between the longest walls (m)','4.0','abs<=0.01','AMBIGUOUS','4.0 clear distance between inner faces of the two longest walls (6.1 m at y=-4.4..-4.2, 5.9 m at y=-0.2..0)','Centre-line distance 4.2 and outer-face distance 4.4 are both reasonable readings of "distance between walls" and fail with the 0.01 tolerance.'),
('geometry_test_09','Ids of the walls that form a triangle','{..Hww, ..HX0, ..H$i}','exact set of 3','MATCH','same 3 walls (the only non-orthogonal walls; profiles mitred, meeting at apex (0,-1) and base y=-5.6)',''),
('geometry_test_10','Total inner length of walls ..YtE + ..Yr0 (m)','5.9','abs<=0.01','MATCH','5.9 = 3.5 (tE inner face x=0.2, y 0.2..3.7) + 2.4 (r0 inner face y=0.2, x 0.2..2.6)','Axis sum 6.1 and outer 6.3 fail, but the prompt says "inner", so the key is the right reading.'),
('topological_test_06','Wall separating rooms ..UwKx and ..UwJB','3Vyqk8cSj8TOuAk6zHUw89','exact','MATCH','..Uw89 (y 4.5..4.7; Kx below at y<=4.5, JB above at y>=4.7, x-overlap 5.1..7.5)','No IfcRelSpaceBoundary in file; derived from geometry.'),
('topological_test_07','Slabs that close room ..UwKx','{..K11, ..K9m}','exact set','MATCH','{K11 (floor, full 7.7x8.1), K9m (ceiling, covers x 5.1..7.7, y 0..4.7)}','Ceiling slab ..K2W only touches the room footprint along the edge x=5.1 (no area overlap).'),
('topological_test_08','Columns touching room ..ZIPn','{..ZIat, ..ZIH7}','exact set','MATCH','{at (face x=3.6 on room edge), H7 (face y=2.9 on room edge)}','Other columns IIS (x 5.45..5.65) and GO (y<1.14) do not touch room x 0.2..3.6, y 2.9..6.3.'),
('topological_test_09','Room not adjacent to ..xNU','3Vyqk8cSj8TOuAk6zHUwKx','exact','MATCH','..UwKx (x 5.1..7.5, y 0.2..4.5; NU is x 0.2..2.8, y 4.7..7.9; no shared wall or corner)','K5 shares wall ..89, JB shares wall ..IV.'),
('topological_test_10','Room open to the exterior','0rTWnvc$TEcxPkiz6YVMaY','exact','MATCH','..VMaY (east wall ..MJ only spans y 4.5..8.1, so the room edge x=7.7, y 0.2..4.5 has no wall)',''),
('numeric_test_01','Net floor area of room ..nvVA (m2)','17.11','max(0.1, 0.1%)','MATCH','17.11 (space profile; check from walls: 12.92 + 3.99 + 0.20 strip under partial wall sD)',''),
('numeric_test_02','Net floor area of all rooms (m2)','42.7','max(0.1, 0.1%)','MATCH','42.70 = 17.11 + 21.18 + 4.41 (spaces); check: 7.8x5.8 clear minus interior walls 2.54 = 42.70',''),
('numeric_test_03','GFA of the second floor (m2)','51.83','max(0.1, 0.1%)','MATCH','51.83 = L2 outer wall outline (7.7x4.7 + 4.6x3.4)','"Second floor" read as L2 (only 2 storeys; in UK/EU usage it would be a 3rd storey that does not exist). The L2 slab is 10.65x8.1 = 86.265 m2 (extends beyond the L2 walls) and L2 spaces sum 44.83 m2; both fail.'),
('numeric_test_04','GFA of all storeys (m2)','138.095','max(0.1, 0.1%)','MATCH','138.095 = L1 outline 10.65x8.1 (86.265) + L2 outline 51.83','Using slab footprints instead gives 172.53.'),
('numeric_test_05','Inner net wall area, 4 walls (m2)','33.6','max(0.1, 0.1%)','MATCH','33.6 = room-facing exposed faces (2.9+3.0+0.2 nB end+2.0+3.1) x 3.0; no openings so net = gross','Face-sampling script. Leaving out nB end face gives 33.0; axis length x h gives 34.8; both fail.'),
('numeric_test_06','Outer net wall area, 4 walls (m2)','36.0','max(0.1, 0.1%)','MATCH','36.0 = exterior exposed faces incl. end faces (3.3+2.8+2.2+3.7) x 3.0; no openings','Same file content as 005 apart from the header.'),
('numeric_test_07','Inner net wall area, walls pI9 + m0 + gT (m2)','20.82','max(0.1, 0.1%)','AMBIGUOUS','20.22 = south-room faces of listed walls (2.9+2.0+3.1) x 3 - door 1.8x2.1','Key = 20.22 + 0.6, which is the 0.2 m end face of wall nB (not in the list), i.e. a room-boundary clear length of 5.1+3.1. The partition pI9 has two interior sides (both = 25.14). Untrimmed/axis = 21.42. No reading that uses only the three listed walls gives 20.82. Under a strict reading this is a MISMATCH.'),
('numeric_test_08','Outer net wall area, 4 walls (m2)','27.3','max(0.1, 0.1%)','MATCH','27.3 = 36.0 gross - openings (2x1.6 + 2.5 + 3.0 = 8.7)',''),
('numeric_test_09','Outer gross wall area, 4 walls (m2)','36.0','max(0.1, 0.1%)','MATCH','36.0 (same outer faces as 006; openings ignored for gross)',''),
('numeric_test_10','Inner gross wall area, nG + m0 + gT, "do not trim, include intersecting areas" (m2)','24.6','max(0.1, 0.1%)','AMBIGUOUS','25.2 = untrimmed own inner faces (2.9+2.0+3.5) x 3','Key 24.6 = (5.1+3.1) x 3: it adds the nB junction (0.2) but trims gT to 3.1, which partly contradicts "do not trim". Other readings: exposed 24.0, untrimmed + nB 25.8, both sides of nG 32.7. The extra sentence in the prompt does not pin down a single value.'),
('numeric_test_11','Area of openings > 2 m2 (m2)','11.25','max(0.1, 0.1%)','MATCH','11.25 = 3.84 (2.4x1.6) + 3.0 (1.2x2.5) + 4.41 (2.1x2.1)','One opening is exactly 2.0 m2 (1.0x2.0); strict ">" excludes it, ">=" gives 13.25.'),
('numeric_test_12','Combined width of openings with a sill (m)','3.4','max(0.1, 0.1%)','MATCH','3.4 = 2.4 (sill 0.9) + 1.0 (sill 0.5); the other two openings start at z=0','Geometry same as 011.'),
('numeric_test_13','Length of all walls (m)','24.3','max(0.1, 0.1%)','MATCH','24.3 = sum of axis lengths 6.5+3.1+3.5+5.1+3.0+2.0+1.1 (walls butt, no overlaps)',''),
('numeric_test_14','Area of the opening in slab ..PbrE (m2)','3.625','max(0.1, 0.1%)','MATCH','3.625 = 2.9 x 1.25 (single IfcOpeningElement)',''),
('numeric_test_15','Number of openings > 2 m2','3','max(0.1, 0.1%)','MATCH','3 (wall 3.84, wall 2.4, slab 3.6; excluded: 2.0 exactly, 1.8)','">=" would give 4. Counts the slab opening too.'),
('numeric_test_16','Volume of openings in slab ..PbrE (m3)','5.775','max(0.1, 0.1%)','MISMATCH','1.7325 = 2.4x1.5x0.3 + 2.9x0.75x0.3 (opening solids 1.08 + 0.6525)','Key 5.775 = 3.6 + 2.175, the opening AREAS in m2, not volumes.'),
('numeric_test_17','Net wall volume of all walls (m3)','64.66','max(0.1, 0.1%)','MISMATCH','12.932 (sum of wall solids with openings cut; gross 14.58 - openings 1.648)','Key 64.66 = 24.3 x 3.0 - opening areas 8.24, the net one-side wall AREA in m2, not a volume (= 12.932 / 0.2).'),
('numeric_test_18','Net volume of the non-rectangular room (m3)','51.06','max(0.1, 0.1%)','MATCH','51.06 = 17.02 m2 (space profile incl. 0.3x0.3 column void) x 3.0','Without the column deduction it would be 51.33.'),
('numeric_test_19','Net volume of all slabs (m3)','22.6375','max(0.1, 0.1%)','MISMATCH','15.536 = upper slab 6.791 (29.15x0.3 - openings 0.866 - 1.0875) + lower slab 8.745','Key 22.6375 = 29.15 - 2.8875 - 3.625, the net AREA of the upper slab in m2.'),
('numeric_test_20','"Perimeter in cubic meters" of all rooms','44.6','max(0.1, 0.1%)','TEXT ISSUE','44.6 m = 20.8 + 15.4 + 8.4 (outer boundaries of the 3 spaces)','Prompt asks for perimeter in cubic meters. The value matches the outer perimeter. If the inner boundary around the free-standing column (1.2) is included: 45.8.'),
]
vals = {}
lines = ['# BIBIMBAP RETRIEVE tasks: answer-key check', '',
 'Data: /tmp/bib/olddata/data (ifc + all_questions.csv); tests: /tmp/bib/bibimbap/data/tests. Geometry: ifcopenshell 0.9.0 (Body representations, world coordinates, SI metres); wall faces classified by sampling the face grid (wallfaces.py). "test passes" = execute_test with my primary answer under the schema key.', '',
 '| task | prompt (short) | key in test | your answer (method) | tolerance | class | test passes with my answer | note |', '|---|---|---|---|---|---|---|---|']
for t, p, key, tol, cls, ans, note in T:
    r = runs[t]
    ok = r['primary_result']['right_answer']
    alt_pass = [f"{l}={a['value']}" for l, a in r['alternatives'].items() if a['result']['right_answer'] and a['value'] != r['primary']]
    passtxt = ('yes' if ok else 'no') + ((' (key reading passes: ' + '; '.join(alt_pass) + ')') if (not ok and alt_pass) else '')
    lines.append(f'| {t} | {p} | {key} | {ans} | {tol} | {cls} | {passtxt} | {note} |')
    vals[t] = dict(prompt=p, key=key, tolerance=tol, cls=cls, my_answer=r['primary'], method=ans, note=note,
                   test_with_my_answer=r['primary_result'], alternatives=r['alternatives'])
from collections import Counter
c = Counter(x[4] for x in T)
lines += ['', 'Counts: ' + ', '.join(f'{k} {v}' for k, v in sorted(c.items())) + f' (total {len(T)})']
open('retrieve-check.md', 'w').write('\n'.join(lines) + '\n')
json.dump(vals, open('retrieve-values.json', 'w'), indent=1, default=str)
print(c)
