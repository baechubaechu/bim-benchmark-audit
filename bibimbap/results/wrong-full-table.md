
| task | variant | why | metrics | score |
|---|---|---|---|---|
| test_01 | *correct_A* (reference) | correct answer from the create C1 check | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| test_01 | noop | unchanged file, model_output claims success | OE=0 RL=0 RD=0 IC=0 | 0.000 |
| test_01 | two_new_elements | correct element plus a coincident second copy (two created instead of one) | OE=1 RL=0 RD=0 IC=0 | 0.250 |
| test_01 | junk_duplicate_of_unrelated **⚑** | correct + coincident duplicate of unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| test_01 | collateral_move_unrelated **⚑** | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved +1 m in x | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| test_01 | collateral_delete_unrelated **⚑** | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj deleted | OE=1 RL=1 RD=1 IC=0.75 | 0.938 |
| test_01 | door_without_opening **⚑** | door block placed in the wall with no opening/void/fill, so the wall is not cut | OE=1 RL=1 RD=1 IC=0.75 | 0.938 |
| test_01 | door_in_other_wall | 2x1 door in wall 22hy..SKC instead of 2UsX..Hvf | OE=1 RL=0 RD=1 IC=0.75 | 0.688 |
| test_01 | door_2m_wide_1m_high **⚑** | door 2.0 m wide x 1.0 m high (prompt: 2 by 1 m door; a 1 m high door; test accepts both orders) | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| test_01 | door_0.9x2.1 | standard 0.9x2.1 door instead of 1x2 | OE=1 RL=1 RD=0 IC=1 | 0.750 |
| test_02 | *correct_A* (reference) | correct answer from the create C1 check | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| test_02 | noop | unchanged file, model_output claims success | OE=0 RL=0 RD=0 IC=0 | 0.000 |
| test_02 | two_new_elements | correct element plus a coincident second copy (two created instead of one) | OE=1 RL=0 RD=0 IC=0 | 0.250 |
| test_02 | junk_duplicate_of_unrelated **⚑** | correct + coincident duplicate of unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| test_02 | collateral_move_unrelated **⚑** | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved +1 m in x | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| test_02 | collateral_delete_unrelated **⚑** | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj deleted | OE=1 RL=1 RD=1 IC=0.6667 | 0.917 |
| test_02 | slab_floating_0.75m **⚑** | slab bottom at z=+0.75 m instead of 0 (prompt: bottom at (-30,0)) | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| test_02 | slab_0.4_thick | slab 0.4 m thick instead of 0.2 | OE=1 RL=1 RD=0 IC=1 | 0.750 |
| test_02 | slab_centre_off_0.4m **⚑** | slab centre at (-29.6, 0.4) instead of (-30, 0) | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| test_03 | *correct_A* (reference) | correct answer from the create C1 check | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| test_03 | noop | unchanged file, model_output claims success | OE=0 RL=0 RD=0 IC=0 | 0.000 |
| test_03 | two_new_elements | correct element plus a coincident second copy (two created instead of one) | OE=1 RL=0 RD=0 IC=0 | 0.250 |
| test_03 | junk_duplicate_of_unrelated **⚑** | correct + coincident duplicate of unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| test_03 | collateral_move_unrelated **⚑** | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved +1 m in x | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| test_03 | collateral_delete_unrelated **⚑** | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj deleted | OE=1 RL=1 RD=1 IC=0.6667 | 0.917 |
| test_03 | opening_without_void_rel **⚑** | 5x5 opening box at the slab centre but not linked by IfcRelVoidsElement (slab is not cut) | OE=1 RL=1 RD=1 IC=0.6667 | 0.917 |
| test_03 | opening_off_centre_2m | opening 2 m off centre | OE=1 RL=0 RD=1 IC=1 | 0.750 |
| test_03 | opening_off_centre_0.2m **⚑** | opening 0.2 m off centre | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| test_04 | *correct_A* (reference) | correct answer from the create C1 check | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| test_04 | noop | unchanged file, model_output claims success | OE=0 RL=0 RD=0 IC=0 | 0.000 |
| test_04 | two_new_elements | correct element plus a coincident second copy (two created instead of one) | OE=1 RL=0 RD=0 IC=0 | 0.250 |
| test_04 | junk_duplicate_of_unrelated | correct + coincident duplicate of unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj | OE=1 RL=0 RD=0 IC=0 | 0.250 |
| test_04 | collateral_move_unrelated **⚑** | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved +1 m in x | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| test_04 | collateral_delete_unrelated **⚑** | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj deleted | OE=1 RL=1 RD=1 IC=0.6667 | 0.917 |
| test_04 | column_floating_z10 **⚑** | 3 m column at (12,8) but base at z=10 m (floating 10 m above the floor) | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| test_04 | column_at_8_12 **⚑** | column at (8,12) instead of (12,8) | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| test_04 | column_6m | 6 m column instead of 3 m | OE=1 RL=1 RD=0 IC=1 | 0.750 |
| test_05 | *correct_A* (reference) | correct answer from the create C1 check | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| test_05 | noop | unchanged file, model_output claims success | OE=0 RL=0 RD=0 IC=0 | 0.000 |
| test_05 | two_new_elements | correct element plus a coincident second copy (two created instead of one) | OE=1 RL=0 RD=0 IC=0 | 0.250 |
| test_05 | junk_duplicate_of_unrelated **⚑** | correct + coincident duplicate of unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| test_05 | collateral_move_unrelated **⚑** | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved +1 m in x | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| test_05 | collateral_delete_unrelated **⚑** | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj deleted | OE=1 RL=1 RD=1 IC=0.6667 | 0.917 |
| test_05 | wall_centred_on_point **⚑** | 15 m wall centred on (0,-10) (runs -7.5..7.5) instead of beginning there | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| test_05 | wall_10m | 10 m wall instead of 15 m | OE=1 RL=1 RD=0 IC=1 | 0.750 |
| geometry_test_01 | *correct_A* (reference) | correct answer from the create C1 check | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| geometry_test_01 | noop | unchanged file, model_output claims success | OE=0 RL=0 RD=0 IC=0 | 0.000 |
| geometry_test_01 | two_new_elements | correct element plus a coincident second copy (two created instead of one) | OE=1 RL=0 RD=0 IC=0 | 0.250 |
| geometry_test_01 | slab_overhang_0.45 **⚑** | slab overhangs the outer column edges by 0.45 m on every side | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| geometry_test_01 | slab_floating_0.5 | slab 0.5 m above the column tops | OE=1 RL=0 RD=1 IC=1 | 0.750 |
| geometry_test_02 | *correct_A* (reference) | correct answer from the create C1 check | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| geometry_test_02 | noop | unchanged file, model_output claims success | OE=0 RL=0 RD=0 IC=0 | 0.000 |
| geometry_test_02 | two_new_elements | correct element plus a coincident second copy (two created instead of one) | OE=1 RL=0 RD=0 IC=0 | 0.250 |
| geometry_test_02 | column_floating_z10 **⚑** | column at the centroid in plan but base at z=10 m (floating) | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| geometry_test_02 | column_1.2m_stub **⚑** | 1.2 m stub column in a 3 m storey | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| geometry_test_03 | *correct_A* (reference) | correct answer from the create C1 check | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| geometry_test_03 | noop | unchanged file, model_output claims success | OE=0 RL=0 RD=0 IC=0 | 0.000 |
| geometry_test_03 | two_new_elements | correct element plus a coincident second copy (two created instead of one) | OE=1 RL=0 RD=0 IC=0 | 0.250 |
| geometry_test_03 | door_without_opening **⚑** | door block in the north wall with no opening/void/fill | OE=1 RL=1 RD=1 IC=0.6667 | 0.917 |
| geometry_test_03 | door_in_reference_wall | door in the reference wall $hw itself instead of the wall north of it | OE=1 RL=0 RD=1 IC=0.6667 | 0.667 |
| geometry_test_03 | door_in_far_north_wall | door in the second wall north ($iC), not the adjacent one ($ig) | OE=1 RL=0 RD=1 IC=0.6667 | 0.667 |
| geometry_test_04 | *correct_A* (reference) | correct answer from the create C1 check | OE=1 RL=1 RD=1 IC=0.6667 | 0.917 |
| geometry_test_04 | noop | unchanged file, model_output claims success | OE=0 RL=0 RD=0 IC=0 | 0.000 |
| geometry_test_04 | two_new_elements | correct element plus a coincident second copy (two created instead of one) | OE=1 RL=0 RD=0 IC=0 | 0.250 |
| geometry_test_04 | junk_duplicate_of_unrelated **⚑** | correct + coincident duplicate of unrelated IfcWallStandardCase 3A5GfH23DBvBYpavCfWhSk | OE=1 RL=1 RD=1 IC=0.6667 | 0.917 |
| geometry_test_04 | collateral_move_unrelated | correct + unrelated IfcWallStandardCase 3A5GfH23DBvBYpavCfWhSk moved +1 m in x | OE=1 RL=1 RD=1 IC=0.3333 | 0.833 |
| geometry_test_04 | collateral_delete_unrelated | correct + unrelated IfcWallStandardCase 3A5GfH23DBvBYpavCfWhSk deleted | OE=1 RL=1 RD=1 IC=0.3333 | 0.833 |
| geometry_test_04 | space_whole_floor | space covers the whole floor including the area right of the column | OE=1 RL=1 RD=0 IC=0.6667 | 0.667 |
| geometry_test_04 | space_right_of_column | space in the area RIGHT of the column | OE=1 RL=0 RD=0 IC=0.6667 | 0.417 |
| geometry_test_05 | *correct_A* (reference) | correct answer from the create C1 check | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| geometry_test_05 | noop | unchanged file, model_output claims success | OE=0 RL=0 RD=0 IC=0 | 0.000 |
| geometry_test_05 | two_new_elements | correct element plus a coincident second copy (two created instead of one) | OE=1 RL=0 RD=0 IC=0 | 0.250 |
| geometry_test_05 | wall_direction_+y **⚑** | 5 m wall from (10,5) pointing (0,1) instead of (1,0) | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| geometry_test_05 | wall_4.6m **⚑** | 4.6 m wall instead of 5 m | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| geometry_test_05 | wall_5.45m **⚑** | 5.45 m wall instead of 5 m | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| geometry_test_05 | wall_direction_-x | wall pointing (-1,0) | OE=1 RL=0 RD=1 IC=1 | 0.750 |
| topological_test_01 | *correct_A* (reference) | correct answer from the create C1 check | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| topological_test_01 | noop | unchanged file, model_output claims success | OE=0 RL=0 RD=0 IC=0 | 0.000 |
| topological_test_01 | two_new_elements | correct element plus a coincident second copy (two created instead of one) | OE=1 RL=0 RD=0 IC=0 | 0.250 |
| topological_test_01 | junk_duplicate_of_unrelated | correct + coincident duplicate of unrelated IfcWall 3_DHXxtdb3wRKlXgyMiHOP | OE=1 RL=0 RD=0 IC=0 | 0.250 |
| topological_test_01 | collateral_move_unrelated **⚑** | correct + unrelated IfcWall 3_DHXxtdb3wRKlXgyMiHOP moved +1 m in x | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| topological_test_01 | collateral_delete_unrelated **⚑** | correct + unrelated IfcWall 3_DHXxtdb3wRKlXgyMiHOP deleted | OE=1 RL=1 RD=1 IC=0.6667 | 0.917 |
| topological_test_01 | wall_outside_west_wall **⚑** | new wall parallel to and outside the existing west wall (x -0.3..-0.1); east side of the room stays open | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| topological_test_01 | wall_across_room **⚑** | wall across the middle of the room; east side stays open | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| topological_test_02 | *correct_A* (reference) | correct answer from the create C1 check | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| topological_test_02 | noop | unchanged file, model_output claims success | OE=0 RL=0 RD=0 IC=0 | 0.000 |
| topological_test_02 | two_new_elements | correct element plus a coincident second copy (two created instead of one) | OE=1 RL=0 RD=0 IC=0 | 0.250 |
| topological_test_02 | junk_duplicate_of_unrelated **⚑** | correct + coincident duplicate of unrelated IfcSlab 3_DHXxtdb3wRKlXgyMiHD0 | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| topological_test_02 | collateral_move_unrelated **⚑** | correct + unrelated IfcSlab 3_DHXxtdb3wRKlXgyMiHD0 moved +1 m in x | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| topological_test_02 | collateral_delete_unrelated **⚑** | correct + unrelated IfcSlab 3_DHXxtdb3wRKlXgyMiHD0 deleted | OE=1 RL=1 RD=1 IC=0.6667 | 0.917 |
| topological_test_02 | column_outside_east_wall **⚑** | column 0.25 m outside the east wall (x 5.3..5.6), i.e. not in the inner space | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| topological_test_03 | *correct_A* (reference) | correct answer from the create C1 check | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| topological_test_03 | noop | unchanged file, model_output claims success | OE=0 RL=0 RD=0 IC=0 | 0.000 |
| topological_test_03 | two_new_elements | correct element plus a coincident second copy (two created instead of one) | OE=1 RL=0 RD=0 IC=0 | 0.250 |
| topological_test_03 | junk_duplicate_of_unrelated | correct + coincident duplicate of unrelated IfcWall 3_DHXxtdb3wRKlXgyMiHOP | OE=1 RL=0 RD=0 IC=0 | 0.250 |
| topological_test_03 | collateral_move_unrelated **⚑** | correct + unrelated IfcWall 3_DHXxtdb3wRKlXgyMiHOP moved +1 m in x | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| topological_test_03 | collateral_delete_unrelated **⚑** | correct + unrelated IfcWall 3_DHXxtdb3wRKlXgyMiHOP deleted | OE=1 RL=1 RD=1 IC=0.6667 | 0.917 |
| topological_test_03 | wall_0.65m_in_gap **⚑** | 0.65 m wall in the middle of the 1.65 m gap, leaving 0.5 m gaps on both sides (rooms not separated) | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| topological_test_03 | full_length_duplicate_stubs **⚑** | full-length wall that coincides with both existing wall stubs (from create C1) | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| topological_test_04 | *correct_A* (reference) | correct answer from the create C1 check | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| topological_test_04 | noop | unchanged file, model_output claims success | OE=0 RL=0 RD=0 IC=0 | 0.000 |
| topological_test_04 | two_new_elements | correct element plus a coincident second copy (two created instead of one) | OE=1 RL=0 RD=0 IC=0 | 0.250 |
| topological_test_04 | junk_duplicate_of_unrelated **⚑** | correct + coincident duplicate of unrelated IfcWall 006bnjuTb7gwla5uiF7YAR | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| topological_test_04 | collateral_move_unrelated **⚑** | correct + unrelated IfcWall 006bnjuTb7gwla5uiF7YAR moved +1 m in x | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| topological_test_04 | collateral_delete_unrelated **⚑** | correct + unrelated IfcWall 006bnjuTb7gwla5uiF7YAR deleted | OE=1 RL=1 RD=1 IC=0.6667 | 0.917 |
| topological_test_04 | slab_0.8m_below_walls **⚑** | floor slab 0.8 m below the wall bases (gap; does not close the walls) | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| topological_test_04 | slab_duplicate_of_ceiling **⚑** | new slab coincident with the existing ceiling slab (floor stays open) | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| topological_test_05 | *correct_A* (reference) | correct answer from the create C1 check | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| topological_test_05 | noop | unchanged file, model_output claims success | OE=0 RL=0 RD=0 IC=0 | 0.000 |
| topological_test_05 | two_new_elements | correct element plus a coincident second copy (two created instead of one) | OE=1 RL=0 RD=0 IC=0 | 0.250 |
| topological_test_05 | junk_duplicate_of_unrelated **⚑** | correct + coincident duplicate of unrelated IfcWall 3Vyqk8cSj8TOuAk6zHUwAt | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| topological_test_05 | collateral_move_unrelated **⚑** | correct + unrelated IfcWall 3Vyqk8cSj8TOuAk6zHUwAt moved +1 m in x | OE=1 RL=1 RD=1 IC=0.6667 | 0.917 |
| topological_test_05 | collateral_delete_unrelated **⚑** | correct + unrelated IfcWall 3Vyqk8cSj8TOuAk6zHUwAt deleted | OE=1 RL=1 RD=1 IC=0.6667 | 0.917 |
| topological_test_05 | door_in_interior_wall **⚑** | door in interior wall 3Vyq..wBs (connects two inner rooms, not to outdoors) | OE=1 RL=1 RD=1 IC=1 | 1.000 |
| topological_test_05 | door_without_opening **⚑** | door block in the exterior wall with no opening/void/fill | OE=1 RL=1 RD=1 IC=0.6667 | 0.917 |
| test_11 | *correct_test_11_center* (reference) | correct answer from the update C1 check (best-scoring accepted reading) | RL=1 RD=1 IC=1 | 1.000 |
| test_11 | noop | unchanged file, model_output claims success | RL=0 RD=0 IC=1 | 0.333 |
| test_11 | collateral_move_unrelated_placement | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved +1 m x via its ObjectPlacement | RL=1 RD=1 IC=0 | 0.667 |
| test_11 | collateral_move_unrelated_geometry **⚑** | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved +1 m x via its Body geometry (placement untouched) | RL=1 RD=1 IC=1 | 1.000 |
| test_11 | collateral_halve_unrelated_height **⚑** | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj squashed to half its local-z size (geometry only) | RL=1 RD=1 IC=1 | 1.000 |
| test_11 | collateral_delete_unrelated | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj deleted | RL=1 RD=1 IC=0 | 0.667 |
| test_11 | junk_duplicate_of_unrelated **⚑** | correct + coincident duplicate of unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj | RL=1 RD=1 IC=1 | 1.000 |
| test_11 | rotate_+45 | rotated +45 instead of +90 | RL=0 RD=0 IC=1 | 0.333 |
| test_11 | rotate_-90 **⚑** | rotated -90 instead of +90 about the centre (same occupied volume for a symmetric box wall; only the axis direction flips) | RL=1 RD=1 IC=1 | 1.000 |
| test_11 | rotate_other_wall | wall 22hy..SKC rotated instead | RL=0 RD=0 IC=0 | 0.000 |
| test_12 | *correct_test_12_minusx* (reference) | correct answer from the update C1 check (best-scoring accepted reading) | RL=1 RD=1 IC=1 | 1.000 |
| test_12 | noop | unchanged file, model_output claims success | RL=0 RD=1 IC=1 | 0.667 |
| test_12 | collateral_move_unrelated_placement | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved +1 m x via its ObjectPlacement | RL=1 RD=1 IC=0 | 0.667 |
| test_12 | collateral_move_unrelated_geometry **⚑** | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved +1 m x via its Body geometry (placement untouched) | RL=1 RD=1 IC=1 | 1.000 |
| test_12 | collateral_halve_unrelated_height **⚑** | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj squashed to half its local-z size (geometry only) | RL=1 RD=1 IC=1 | 1.000 |
| test_12 | collateral_delete_unrelated | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj deleted | RL=1 RD=1 IC=0 | 0.667 |
| test_12 | junk_duplicate_of_unrelated **⚑** | correct + coincident duplicate of unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj | RL=1 RD=1 IC=1 | 1.000 |
| test_12 | move_-2m | door+opening moved 2 m instead of 1 m | RL=0 RD=1 IC=1 | 0.667 |
| test_12 | placement_only_move **⚑** | placements say -1 m but geometry shifted back: door and opening do not move in space | RL=1 RD=1 IC=1 | 1.000 |
| test_12 | door_moved_opening_left | door moved -1 m but its opening left behind (door now sits in solid wall) | RL=1 RD=1 IC=0 | 0.667 |
| test_13 | *correct_test_13_resize* (reference) | correct answer from the update C1 check (best-scoring accepted reading) | RL=1 RD=1 IC=1 | 1.000 |
| test_13 | noop | unchanged file, model_output claims success | RL=0 RD=1 IC=1 | 0.667 |
| test_13 | collateral_move_unrelated_placement | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved +1 m x via its ObjectPlacement | RL=1 RD=1 IC=0 | 0.667 |
| test_13 | collateral_move_unrelated_geometry **⚑** | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved +1 m x via its Body geometry (placement untouched) | RL=1 RD=1 IC=1 | 1.000 |
| test_13 | collateral_halve_unrelated_height **⚑** | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj squashed to half its local-z size (geometry only) | RL=1 RD=1 IC=1 | 1.000 |
| test_13 | collateral_delete_unrelated | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj deleted | RL=1 RD=1 IC=0 | 0.667 |
| test_13 | junk_duplicate_of_unrelated **⚑** | correct + coincident duplicate of unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj | RL=1 RD=1 IC=1 | 1.000 |
| test_13 | placement_only_move_up **⚑** | window assembly placements raised 0.5 m, geometry shifted back: nothing moves or grows in space | RL=1 RD=1 IC=1 | 1.000 |
| test_13 | move_up_1m | assembly moved up 1.0 m | RL=0 RD=1 IC=1 | 0.667 |
| test_13 | window_only_up | only the window raised, opening/trims left | RL=0 RD=1 IC=0 | 0.333 |
| test_14 | *correct_test_14_down* (reference) | correct answer from the update C1 check (best-scoring accepted reading) | RL=1 RD=1 IC=1 | 1.000 |
| test_14 | noop | unchanged file, model_output claims success | RL=0 RD=1 IC=1 | 0.667 |
| test_14 | collateral_move_unrelated_placement | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved +1 m x via its ObjectPlacement | RL=1 RD=1 IC=0 | 0.667 |
| test_14 | collateral_move_unrelated_geometry **⚑** | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved +1 m x via its Body geometry (placement untouched) | RL=1 RD=1 IC=1 | 1.000 |
| test_14 | collateral_halve_unrelated_height **⚑** | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj squashed to half its local-z size (geometry only) | RL=1 RD=1 IC=1 | 1.000 |
| test_14 | collateral_delete_unrelated | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj deleted | RL=1 RD=1 IC=0 | 0.667 |
| test_14 | junk_duplicate_of_unrelated **⚑** | correct + coincident duplicate of unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj | RL=1 RD=1 IC=1 | 1.000 |
| test_14 | placement_only_move_down **⚑** | slab placement lowered 0.5 m, geometry shifted back: slab stays where it was | RL=1 RD=1 IC=1 | 1.000 |
| test_14 | move_up_0.5 | slab moved UP 0.5 m | RL=0 RD=1 IC=1 | 0.667 |
| test_15 | *correct_test_15* (reference) | correct answer from the update C1 check (best-scoring accepted reading) | RL=1 RD=1 IC=1 | 1.000 |
| test_15 | noop | unchanged file, model_output claims success | RL=0 RD=1 IC=1 | 0.667 |
| test_15 | collateral_move_unrelated_placement | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved +1 m x via its ObjectPlacement | RL=1 RD=1 IC=0 | 0.667 |
| test_15 | collateral_move_unrelated_geometry **⚑** | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved +1 m x via its Body geometry (placement untouched) | RL=1 RD=1 IC=1 | 1.000 |
| test_15 | collateral_halve_unrelated_height **⚑** | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj squashed to half its local-z size (geometry only) | RL=1 RD=1 IC=1 | 1.000 |
| test_15 | collateral_delete_unrelated | correct + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj deleted | RL=1 RD=1 IC=0 | 0.667 |
| test_15 | junk_duplicate_of_unrelated **⚑** | correct + coincident duplicate of unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj | RL=1 RD=1 IC=1 | 1.000 |
| test_15 | placement_only_move **⚑** | column placement moved -3 m y, geometry shifted back: column stays | RL=1 RD=1 IC=1 | 1.000 |
| test_15 | move_+3 | moved +3 m | RL=0 RD=1 IC=1 | 0.667 |
| test_15 | move_other_column | column 22hy..SMv moved instead | RL=0 RD=1 IC=0 | 0.333 |
| geometry_test_11 | *correct_geometry_test_11* (reference) | correct answer from the update C1 check (best-scoring accepted reading) | RL=1 RD=1 IC=1 | 1.000 |
| geometry_test_11 | noop | unchanged file, model_output claims success | RL=1 RD=0 IC=1 | 0.667 |
| geometry_test_11 | collateral_move_unrelated_placement | correct + unrelated IfcWall 3PQZwOmmD1hgPWgX4XFLB1 moved +1 m x via its ObjectPlacement | RL=1 RD=1 IC=0 | 0.667 |
| geometry_test_11 | collateral_move_unrelated_geometry **⚑** | correct + unrelated IfcWall 3PQZwOmmD1hgPWgX4XFLB1 moved +1 m x via its Body geometry (placement untouched) | RL=1 RD=1 IC=1 | 1.000 |
| geometry_test_11 | collateral_halve_unrelated_height **⚑** | correct + unrelated IfcWall 3PQZwOmmD1hgPWgX4XFLB1 squashed to half its local-z size (geometry only) | RL=1 RD=1 IC=1 | 1.000 |
| geometry_test_11 | collateral_delete_unrelated | correct + unrelated IfcWall 3PQZwOmmD1hgPWgX4XFLB1 deleted | RL=1 RD=1 IC=0 | 0.667 |
| geometry_test_11 | junk_duplicate_of_unrelated **⚑** | correct + coincident duplicate of unrelated IfcWall 3PQZwOmmD1hgPWgX4XFLB1 | RL=1 RD=1 IC=1 | 1.000 |
| geometry_test_11 | lower_by_1m | L2 walls lowered by 1.0 m | RL=1 RD=0 IC=1 | 0.667 |
| geometry_test_11 | lower_storey1_walls | the six ground-floor walls lowered 0.5 m instead | RL=1 RD=0 IC=1 | 0.667 |
| geometry_test_11 | raise_base_0.5 | L2 walls shortened from the bottom (base raised 0.5 m, gap above slab) | RL=0 RD=1 IC=1 | 0.667 |
| geometry_test_12 | *correct_geometry_test_12* (reference) | correct answer from the update C1 check (best-scoring accepted reading) | RL=0 RD=1 IC=1 | 0.667 |
| geometry_test_12 | noop **⚑** | unchanged file, model_output claims success | RL=0 RD=1 IC=1 | 0.667 |
| geometry_test_12 | collateral_move_unrelated_placement **⚑** | correct + unrelated IfcWall 1$zxNs50z3OeFBpABtoN54 moved +1 m x via its ObjectPlacement | RL=1 RD=1 IC=0 | 0.667 |
| geometry_test_12 | collateral_move_unrelated_geometry **⚑** | correct + unrelated IfcWall 1$zxNs50z3OeFBpABtoN54 moved +1 m x via its Body geometry (placement untouched) | RL=1 RD=1 IC=1 | 1.000 |
| geometry_test_12 | collateral_halve_unrelated_height **⚑** | correct + unrelated IfcWall 1$zxNs50z3OeFBpABtoN54 squashed to half its local-z size (geometry only) | RL=1 RD=1 IC=1 | 1.000 |
| geometry_test_12 | collateral_delete_unrelated **⚑** | correct + unrelated IfcWall 1$zxNs50z3OeFBpABtoN54 deleted | RL=1 RD=1 IC=0 | 0.667 |
| geometry_test_12 | junk_duplicate_of_unrelated **⚑** | correct + coincident duplicate of unrelated IfcWall 1$zxNs50z3OeFBpABtoN54 | RL=1 RD=1 IC=1 | 1.000 |
| geometry_test_12 | *control_resave_correct* (control) | correct answer re-opened and re-written unchanged (control, not wrong) | RL=1 RD=1 IC=1 | 1.000 |
| geometry_test_12 | rotate_-45 **⚑** | rotated -45 instead of +45 | RL=0 RD=1 IC=1 | 0.667 |
| geometry_test_12 | rotate_+50.8 **⚑** | rotated +50.8 instead of +45 | RL=0 RD=1 IC=1 | 0.667 |
| geometry_test_12 | rotate_+51 **⚑** | rotated +51 instead of +45 | RL=1 RD=1 IC=1 | 1.000 |
| geometry_test_12 | rotate_+90 **⚑** | rotated +90 | RL=0 RD=1 IC=1 | 0.667 |
| geometry_test_12 | rotate_other_wall | wall N54 (perpendicular) rotated +45 instead | RL=0 RD=1 IC=0 | 0.333 |
| geometry_test_13 | *correct_geometry_test_13* (reference) | correct answer from the update C1 check (best-scoring accepted reading) | RL=1 RD=1 IC=1 | 1.000 |
| geometry_test_13 | noop | unchanged file, model_output claims success | RL=0 RD=1 IC=1 | 0.667 |
| geometry_test_13 | collateral_move_unrelated_placement | correct + unrelated IfcBuildingElementProxy 2KbOAL4v52mv2YJ6fTqlO_ moved +1 m x via its ObjectPlacement | RL=1 RD=1 IC=0 | 0.667 |
| geometry_test_13 | collateral_move_unrelated_geometry **⚑** | correct + unrelated IfcBuildingElementProxy 2KbOAL4v52mv2YJ6fTqlO_ moved +1 m x via its Body geometry (placement untouched) | RL=1 RD=1 IC=1 | 1.000 |
| geometry_test_13 | collateral_halve_unrelated_height **⚑** | correct + unrelated IfcBuildingElementProxy 2KbOAL4v52mv2YJ6fTqlO_ squashed to half its local-z size (geometry only) | RL=1 RD=1 IC=1 | 1.000 |
| geometry_test_13 | collateral_delete_unrelated | correct + unrelated IfcBuildingElementProxy 2KbOAL4v52mv2YJ6fTqlO_ deleted | RL=1 RD=1 IC=0 | 0.667 |
| geometry_test_13 | junk_duplicate_of_unrelated **⚑** | correct + coincident duplicate of unrelated IfcBuildingElementProxy 2KbOAL4v52mv2YJ6fTqlO_ | RL=1 RD=1 IC=1 | 1.000 |
| geometry_test_13 | move_narrow_window | the 0.6 m window moved instead | RL=0 RD=1 IC=0 | 0.333 |
| geometry_test_13 | move_-3 | moved -3 m | RL=0 RD=1 IC=1 | 0.667 |
| geometry_test_13 | move_3_and_up | moved +3 m x and also +0.5 m z | RL=0 RD=1 IC=1 | 0.667 |
| geometry_test_14 | *correct_geometry_test_14_symmetric* (reference) | correct answer from the update C1 check (best-scoring accepted reading) | RL=1 RD=1 IC=1 | 1.000 |
| geometry_test_14 | noop | unchanged file, model_output claims success | RL=1 RD=0 IC=1 | 0.667 |
| geometry_test_14 | junk_duplicate_of_target_class **⚑** | correct + coincident duplicate (new GUID) of 11kJIqz$n2Jf_DfJV1SCVP | RL=1 RD=1 IC=1 | 1.000 |
| geometry_test_14 | square_by_shrinking | made square by SHORTENING the long side (prompt: increase) | RL=1 RD=0 IC=1 | 0.667 |
| geometry_test_14 | extend_short_side_3m | short side increased 3 m (not a square) | RL=1 RD=0 IC=1 | 0.667 |
| geometry_test_15 | *correct_geometry_test_15_tl* (reference) | correct answer from the update C1 check (best-scoring accepted reading) | RL=1 RD=1 IC=1 | 1.000 |
| geometry_test_15 | noop | unchanged file, model_output claims success | RL=0 RD=1 IC=1 | 0.667 |
| geometry_test_15 | junk_duplicate_of_target_class **⚑** | correct + coincident duplicate (new GUID) of 3lOEkLxYb9$uRd50gnIDpA | RL=1 RD=1 IC=1 | 1.000 |
| topological_test_11 | *correct_topological_test_11* (reference) | correct answer from the update C1 check (best-scoring accepted reading) | RL=1 RD=1 IC=1 | 1.000 |
| topological_test_11 | noop | unchanged file, model_output claims success | RL=1 RD=0 IC=1 | 0.667 |
| topological_test_11 | collateral_move_unrelated_placement | correct + unrelated IfcWall 3Vyqk8cSj8TOuAk6zHUwAt moved +1 m x via its ObjectPlacement | RL=1 RD=1 IC=0 | 0.667 |
| topological_test_11 | collateral_move_unrelated_geometry **⚑** | correct + unrelated IfcWall 3Vyqk8cSj8TOuAk6zHUwAt moved +1 m x via its Body geometry (placement untouched) | RL=1 RD=1 IC=1 | 1.000 |
| topological_test_11 | collateral_halve_unrelated_height **⚑** | correct + unrelated IfcWall 3Vyqk8cSj8TOuAk6zHUwAt squashed to half its local-z size (geometry only) | RL=1 RD=1 IC=1 | 1.000 |
| topological_test_11 | collateral_delete_unrelated | correct + unrelated IfcWall 3Vyqk8cSj8TOuAk6zHUwAt deleted | RL=1 RD=1 IC=0 | 0.667 |
| topological_test_11 | junk_duplicate_of_unrelated **⚑** | correct + coincident duplicate of unrelated IfcWall 3Vyqk8cSj8TOuAk6zHUwAt | RL=1 RD=1 IC=1 | 1.000 |
| topological_test_11 | slab_geometry_lowered_to_columns **⚑** | columns unchanged; instead the slab's geometry is lowered 1.195 m so its underside meets the 1.5 m columns | RL=1 RD=1 IC=1 | 1.000 |
| topological_test_11 | only_one_column | only one of the two columns extended | RL=1 RD=0 IC=1 | 0.667 |
| topological_test_11 | columns_through_slab | columns extended to 3.5 m, piercing through the slab | RL=1 RD=0 IC=0 | 0.333 |
| topological_test_12 | *correct_topological_test_12_symmetric* (reference) | correct answer from the update C1 check (best-scoring accepted reading) | RL=1 RD=1 IC=1 | 1.000 |
| topological_test_12 | noop | unchanged file, model_output claims success | RL=1 RD=0 IC=1 | 0.667 |
| topological_test_12 | collateral_move_unrelated_placement | correct + unrelated IfcColumn 0n4qMSuxfEFA0BeEfapSQB moved +1 m x via its ObjectPlacement | RL=1 RD=1 IC=0 | 0.667 |
| topological_test_12 | collateral_move_unrelated_geometry **⚑** | correct + unrelated IfcColumn 0n4qMSuxfEFA0BeEfapSQB moved +1 m x via its Body geometry (placement untouched) | RL=1 RD=1 IC=1 | 1.000 |
| topological_test_12 | collateral_halve_unrelated_height **⚑** | correct + unrelated IfcColumn 0n4qMSuxfEFA0BeEfapSQB squashed to half its local-z size (geometry only) | RL=1 RD=1 IC=1 | 1.000 |
| topological_test_12 | collateral_delete_unrelated | correct + unrelated IfcColumn 0n4qMSuxfEFA0BeEfapSQB deleted | RL=1 RD=1 IC=0 | 0.667 |
| topological_test_12 | junk_duplicate_of_unrelated **⚑** | correct + coincident duplicate of unrelated IfcColumn 0n4qMSuxfEFA0BeEfapSQB | RL=1 RD=1 IC=1 | 1.000 |
| topological_test_12 | shorten_other_wall | wall 3Vyqk8cSj8TOuAk6zHUwIV shortened 1 m instead of CZr | RL=1 RD=0 IC=1 | 0.667 |
| topological_test_13 | *correct_topological_test_13* (reference) | correct answer from the update C1 check (best-scoring accepted reading) | RL=1 RD=1 IC=1 | 1.000 |
| topological_test_13 | noop | unchanged file, model_output claims success | RL=0 RD=1 IC=0 | 0.333 |
| topological_test_13 | collateral_move_unrelated_placement | correct + unrelated IfcWall 0HbU4cYqD2SBtSJYoQ_eZD moved +1 m x via its ObjectPlacement | RL=1 RD=1 IC=0 | 0.667 |
| topological_test_13 | collateral_move_unrelated_geometry **⚑** | correct + unrelated IfcWall 0HbU4cYqD2SBtSJYoQ_eZD moved +1 m x via its Body geometry (placement untouched) | RL=1 RD=1 IC=1 | 1.000 |
| topological_test_13 | collateral_halve_unrelated_height **⚑** | correct + unrelated IfcWall 0HbU4cYqD2SBtSJYoQ_eZD squashed to half its local-z size (geometry only) | RL=1 RD=1 IC=1 | 1.000 |
| topological_test_13 | collateral_delete_unrelated | correct + unrelated IfcWall 0HbU4cYqD2SBtSJYoQ_eZD deleted | RL=1 RD=1 IC=0 | 0.667 |
| topological_test_13 | junk_duplicate_of_unrelated **⚑** | correct + coincident duplicate of unrelated IfcWall 0HbU4cYqD2SBtSJYoQ_eZD | RL=1 RD=1 IC=1 | 1.000 |
| topological_test_13 | placement_only_move **⚑** | window+opening placements moved to y=900 mm, geometry shifted back: window stays | RL=1 RD=1 IC=1 | 1.000 |
| topological_test_13 | correct_move_window_shrunk **⚑** | correct move, but the window body is shrunk to half size (OverallWidth/Height attributes left unchanged) | RL=1 RD=1 IC=1 | 1.000 |
| topological_test_13 | *move_by_window_only_or_assembly* (control) | real move of the assembly root by dy | RL=1 RD=1 IC=1 | 1.000 |
| topological_test_14 | *correct_topological_test_14* (reference) | correct answer from the update C1 check (best-scoring accepted reading) | RL=1 RD=1 IC=1 | 1.000 |
| topological_test_14 | noop | unchanged file, model_output claims success | RL=1 RD=0 IC=1 | 0.667 |
| topological_test_14 | collateral_move_unrelated_placement | correct + unrelated IfcColumn 1A1LNnHqHFQwR1jv6PQkVI moved +1 m x via its ObjectPlacement | RL=1 RD=1 IC=0 | 0.667 |
| topological_test_14 | collateral_move_unrelated_geometry **⚑** | correct + unrelated IfcColumn 1A1LNnHqHFQwR1jv6PQkVI moved +1 m x via its Body geometry (placement untouched) | RL=1 RD=1 IC=1 | 1.000 |
| topological_test_14 | collateral_halve_unrelated_height **⚑** | correct + unrelated IfcColumn 1A1LNnHqHFQwR1jv6PQkVI squashed to half its local-z size (geometry only) | RL=1 RD=1 IC=1 | 1.000 |
| topological_test_14 | collateral_delete_unrelated | correct + unrelated IfcColumn 1A1LNnHqHFQwR1jv6PQkVI deleted | RL=1 RD=1 IC=0 | 0.667 |
| topological_test_14 | junk_duplicate_of_unrelated **⚑** | correct + coincident duplicate of unrelated IfcColumn 1A1LNnHqHFQwR1jv6PQkVI | RL=1 RD=1 IC=1 | 1.000 |
| topological_test_14 | wall_geometry_moved_to_beam_ends **⚑** | beams untouched; the reference wall's geometry is moved 1.46 m so its face meets the beam ends | RL=1 RD=1 IC=1 | 1.000 |
| topological_test_15 | *correct_topological_test_15* (reference) | correct answer from the update C1 check (best-scoring accepted reading) | RL=1 RD=1 IC=1 | 1.000 |
| topological_test_15 | noop | unchanged file, model_output claims success | RL=0 RD=1 IC=1 | 0.667 |
| topological_test_15 | collateral_move_unrelated_placement | correct + unrelated IfcWall 0CJwXarnHAeA7eFXxxI_tZ moved +1 m x via its ObjectPlacement | RL=1 RD=1 IC=0 | 0.667 |
| topological_test_15 | collateral_move_unrelated_geometry **⚑** | correct + unrelated IfcWall 0CJwXarnHAeA7eFXxxI_tZ moved +1 m x via its Body geometry (placement untouched) | RL=1 RD=1 IC=1 | 1.000 |
| topological_test_15 | collateral_halve_unrelated_height **⚑** | correct + unrelated IfcWall 0CJwXarnHAeA7eFXxxI_tZ squashed to half its local-z size (geometry only) | RL=1 RD=1 IC=1 | 1.000 |
| topological_test_15 | collateral_delete_unrelated | correct + unrelated IfcWall 0CJwXarnHAeA7eFXxxI_tZ deleted | RL=1 RD=1 IC=0 | 0.667 |
| topological_test_15 | junk_duplicate_of_unrelated **⚑** | correct + coincident duplicate of unrelated IfcWall 0CJwXarnHAeA7eFXxxI_tZ | RL=1 RD=1 IC=1 | 1.000 |
| topological_test_15 | placement_only_move **⚑** | slab placement lowered 50 mm, geometry shifted back: slab still floats 50 mm above | RL=1 RD=1 IC=1 | 1.000 |
| topological_test_15 | move_down_0.35 | slab lowered 0.35 m: penetrates slab hO | RL=0 RD=1 IC=0 | 0.333 |
| topological_test_15 | lower_and_shift_y | lowered 50 mm but also shifted 0.2 m in y | RL=0 RD=1 IC=1 | 0.667 |
| test_16 | *correct_A_clean_delete* (reference) | clean delete via root.remove_product (del C1 variant A) | ONE=1 IC=0 | 0.500 |
| test_16 | *ref_C_dirty_delete* (reference) | entity-only delete leaving its psets/relations (del C1 variant C) | ONE=1 IC=1 | 1.000 |
| test_16 | noop | unchanged file, model_output claims success | ONE=0 IC=0 | 0.000 |
| test_16 | delete_wrong_element | clean delete of IfcColumn 22hyxvAPr65PFt9WZfHSrj instead of the target | ONE=0 IC=0 | 0.000 |
| test_16 | delete_target_plus_same_class **⚑** | targets plus another IfcColumn 22hyxvAPr65PFt9WZfHSrj deleted | ONE=1 IC=0 | 0.500 |
| test_16 | A_plus_delete_unrelated **⚑** | clean delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj deleted | ONE=1 IC=0 | 0.500 |
| test_16 | A_plus_junk_duplicate **⚑** | A-delete + coincident duplicate of unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj | ONE=1 IC=0 | 0.500 |
| test_16 | A_plus_unrelated_geometry_moved **⚑** | A-delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved 1 m via geometry | ONE=1 IC=0 | 0.500 |
| test_16 | A_plus_unrelated_height_halved **⚑** | A-delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj squashed to half height (geometry only) | ONE=1 IC=0 | 0.500 |
| test_16 | C_plus_junk_duplicate **⚑** | C-delete + coincident duplicate of unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj | ONE=1 IC=1 | 1.000 |
| test_16 | C_plus_unrelated_geometry_moved **⚑** | C-delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved 1 m via geometry | ONE=1 IC=1 | 1.000 |
| test_16 | C_plus_unrelated_height_halved **⚑** | C-delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj squashed to half height (geometry only) | ONE=1 IC=1 | 1.000 |
| test_16 | C_plus_unrelated_placement_moved **⚑** | C-delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved 1 m via placement | ONE=1 IC=0 | 0.500 |
| test_16 | target_kept_guid_renamed **⚑** | target NOT deleted: element kept in place, only its GlobalId replaced by a new one | ONE=1 IC=1 | 1.000 |
| test_17 | *correct_A_clean_delete* (reference) | clean delete via root.remove_product (del C1 variant A) | ONE=1 IC=0 | 0.500 |
| test_17 | *ref_C_dirty_delete* (reference) | entity-only delete leaving its psets/relations (del C1 variant C) | ONE=1 IC=0 | 0.500 |
| test_17 | noop | unchanged file, model_output claims success | ONE=0 IC=0 | 0.000 |
| test_17 | A_plus_delete_unrelated **⚑** | clean delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj deleted | ONE=1 IC=0 | 0.500 |
| test_17 | A_plus_junk_duplicate **⚑** | A-delete + coincident duplicate of unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj | ONE=1 IC=0 | 0.500 |
| test_17 | A_plus_unrelated_geometry_moved **⚑** | A-delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved 1 m via geometry | ONE=1 IC=0 | 0.500 |
| test_17 | A_plus_unrelated_height_halved **⚑** | A-delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj squashed to half height (geometry only) | ONE=1 IC=0 | 0.500 |
| test_17 | C_plus_junk_duplicate **⚑** | C-delete + coincident duplicate of unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj | ONE=1 IC=0 | 0.500 |
| test_17 | C_plus_unrelated_geometry_moved **⚑** | C-delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved 1 m via geometry | ONE=1 IC=0 | 0.500 |
| test_17 | C_plus_unrelated_height_halved **⚑** | C-delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj squashed to half height (geometry only) | ONE=1 IC=0 | 0.500 |
| test_17 | C_plus_unrelated_placement_moved **⚑** | C-delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved 1 m via placement | ONE=1 IC=0 | 0.500 |
| test_17 | target_kept_guid_renamed **⚑** | target NOT deleted: element kept in place, only its GlobalId replaced by a new one | ONE=1 IC=0 | 0.500 |
| test_18 | *correct_A_clean_delete* (reference) | clean delete via root.remove_product (del C1 variant A) | ONE=1 IC=0 | 0.500 |
| test_18 | *ref_C_dirty_delete* (reference) | entity-only delete leaving its psets/relations (del C1 variant C) | ONE=1 IC=1 | 1.000 |
| test_18 | noop | unchanged file, model_output claims success | ONE=0 IC=0 | 0.000 |
| test_18 | delete_wrong_element | clean delete of IfcOpeningElement 2v_dq1kqXwgUORGuwQrNAz instead of the target | ONE=0 IC=0 | 0.000 |
| test_18 | delete_target_plus_same_class **⚑** | targets plus another IfcOpeningElement 2v_dq1kqXwgUORGuwQrNAz deleted | ONE=1 IC=0 | 0.500 |
| test_18 | A_plus_delete_unrelated **⚑** | clean delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj deleted | ONE=1 IC=0 | 0.500 |
| test_18 | A_plus_junk_duplicate **⚑** | A-delete + coincident duplicate of unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj | ONE=1 IC=0 | 0.500 |
| test_18 | A_plus_unrelated_geometry_moved **⚑** | A-delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved 1 m via geometry | ONE=1 IC=0 | 0.500 |
| test_18 | A_plus_unrelated_height_halved **⚑** | A-delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj squashed to half height (geometry only) | ONE=1 IC=0 | 0.500 |
| test_18 | C_plus_junk_duplicate **⚑** | C-delete + coincident duplicate of unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj | ONE=1 IC=1 | 1.000 |
| test_18 | C_plus_unrelated_geometry_moved **⚑** | C-delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved 1 m via geometry | ONE=1 IC=1 | 1.000 |
| test_18 | C_plus_unrelated_height_halved **⚑** | C-delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj squashed to half height (geometry only) | ONE=1 IC=1 | 1.000 |
| test_18 | C_plus_unrelated_placement_moved **⚑** | C-delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved 1 m via placement | ONE=1 IC=0 | 0.500 |
| test_18 | target_kept_guid_renamed **⚑** | target NOT deleted: element kept in place, only its GlobalId replaced by a new one | ONE=1 IC=1 | 1.000 |
| test_19 | *correct_A_clean_delete* (reference) | clean delete via root.remove_product (del C1 variant A) | ONE=1 IC=0 | 0.500 |
| test_19 | *ref_C_dirty_delete* (reference) | entity-only delete leaving its psets/relations (del C1 variant C) | ONE=1 IC=0 | 0.500 |
| test_19 | noop | unchanged file, model_output claims success | ONE=0 IC=0 | 0.000 |
| test_19 | delete_wrong_element | clean delete of IfcWall 2UsXAbj6n0fwEWqdkVuHup instead of the target | ONE=0 IC=0 | 0.000 |
| test_19 | delete_target_plus_same_class **⚑** | targets plus another IfcWall 2UsXAbj6n0fwEWqdkVuHup deleted | ONE=1 IC=0 | 0.500 |
| test_19 | A_plus_delete_unrelated **⚑** | clean delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj deleted | ONE=1 IC=0 | 0.500 |
| test_19 | A_plus_junk_duplicate **⚑** | A-delete + coincident duplicate of unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj | ONE=1 IC=0 | 0.500 |
| test_19 | A_plus_unrelated_geometry_moved **⚑** | A-delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved 1 m via geometry | ONE=1 IC=0 | 0.500 |
| test_19 | A_plus_unrelated_height_halved **⚑** | A-delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj squashed to half height (geometry only) | ONE=1 IC=0 | 0.500 |
| test_19 | C_plus_junk_duplicate **⚑** | C-delete + coincident duplicate of unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj | ONE=1 IC=0 | 0.500 |
| test_19 | C_plus_unrelated_geometry_moved **⚑** | C-delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved 1 m via geometry | ONE=1 IC=0 | 0.500 |
| test_19 | C_plus_unrelated_height_halved **⚑** | C-delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj squashed to half height (geometry only) | ONE=1 IC=0 | 0.500 |
| test_19 | C_plus_unrelated_placement_moved **⚑** | C-delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved 1 m via placement | ONE=1 IC=0 | 0.500 |
| test_19 | target_kept_guid_renamed **⚑** | target NOT deleted: element kept in place, only its GlobalId replaced by a new one | ONE=1 IC=0 | 0.500 |
| test_20 | *correct_A_clean_delete* (reference) | clean delete via root.remove_product (del C1 variant A) | ONE=1 IC=0 | 0.500 |
| test_20 | *ref_C_dirty_delete* (reference) | entity-only delete leaving its psets/relations (del C1 variant C) | ONE=1 IC=1 | 1.000 |
| test_20 | noop | unchanged file, model_output claims success | ONE=0 IC=0 | 0.000 |
| test_20 | delete_wrong_element | clean delete of IfcSpace 2UsXAbj6n0fwEWqdkVuHuP instead of the target | ONE=0 IC=0 | 0.000 |
| test_20 | delete_target_plus_same_class **⚑** | targets plus another IfcSpace 2UsXAbj6n0fwEWqdkVuHuP deleted | ONE=1 IC=0 | 0.500 |
| test_20 | A_plus_delete_unrelated **⚑** | clean delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj deleted | ONE=1 IC=0 | 0.500 |
| test_20 | A_plus_junk_duplicate **⚑** | A-delete + coincident duplicate of unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj | ONE=1 IC=0 | 0.500 |
| test_20 | A_plus_unrelated_geometry_moved **⚑** | A-delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved 1 m via geometry | ONE=1 IC=0 | 0.500 |
| test_20 | A_plus_unrelated_height_halved **⚑** | A-delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj squashed to half height (geometry only) | ONE=1 IC=0 | 0.500 |
| test_20 | C_plus_junk_duplicate **⚑** | C-delete + coincident duplicate of unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj | ONE=1 IC=1 | 1.000 |
| test_20 | C_plus_unrelated_geometry_moved **⚑** | C-delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved 1 m via geometry | ONE=1 IC=1 | 1.000 |
| test_20 | C_plus_unrelated_height_halved **⚑** | C-delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj squashed to half height (geometry only) | ONE=1 IC=1 | 1.000 |
| test_20 | C_plus_unrelated_placement_moved **⚑** | C-delete + unrelated IfcColumn 22hyxvAPr65PFt9WZfHSrj moved 1 m via placement | ONE=1 IC=0 | 0.500 |
| test_20 | target_kept_guid_renamed **⚑** | target NOT deleted: element kept in place, only its GlobalId replaced by a new one | ONE=1 IC=1 | 1.000 |
| geometry_test_16 | *correct_A_clean_delete* (reference) | clean delete via root.remove_product (del C1 variant A) | ONE=1 IC=0 | 0.500 |
| geometry_test_16 | *ref_C_dirty_delete* (reference) | entity-only delete leaving its psets/relations (del C1 variant C) | ONE=1 IC=0 | 0.500 |
| geometry_test_16 | noop | unchanged file, model_output claims success | ONE=0 IC=0 | 0.000 |
| geometry_test_16 | A_plus_delete_unrelated **⚑** | clean delete + unrelated IfcWall 1g0NIEjcH1lfGqbYWRqtLa deleted | ONE=1 IC=0 | 0.500 |
| geometry_test_16 | A_plus_junk_duplicate **⚑** | A-delete + coincident duplicate of unrelated IfcWall 1g0NIEjcH1lfGqbYWRqtLa | ONE=1 IC=0 | 0.500 |
| geometry_test_16 | A_plus_unrelated_geometry_moved **⚑** | A-delete + unrelated IfcWall 1g0NIEjcH1lfGqbYWRqtLa moved 1 m via geometry | ONE=1 IC=0 | 0.500 |
| geometry_test_16 | A_plus_unrelated_height_halved **⚑** | A-delete + unrelated IfcWall 1g0NIEjcH1lfGqbYWRqtLa squashed to half height (geometry only) | ONE=1 IC=0 | 0.500 |
| geometry_test_16 | C_plus_junk_duplicate **⚑** | C-delete + coincident duplicate of unrelated IfcWall 1g0NIEjcH1lfGqbYWRqtLa | ONE=1 IC=0 | 0.500 |
| geometry_test_16 | C_plus_unrelated_geometry_moved **⚑** | C-delete + unrelated IfcWall 1g0NIEjcH1lfGqbYWRqtLa moved 1 m via geometry | ONE=1 IC=0 | 0.500 |
| geometry_test_16 | C_plus_unrelated_height_halved **⚑** | C-delete + unrelated IfcWall 1g0NIEjcH1lfGqbYWRqtLa squashed to half height (geometry only) | ONE=1 IC=0 | 0.500 |
| geometry_test_16 | C_plus_unrelated_placement_moved **⚑** | C-delete + unrelated IfcWall 1g0NIEjcH1lfGqbYWRqtLa moved 1 m via placement | ONE=1 IC=0 | 0.500 |
| geometry_test_16 | target_kept_guid_renamed **⚑** | target NOT deleted: element kept in place, only its GlobalId replaced by a new one | ONE=1 IC=0 | 0.500 |
| geometry_test_17 | *correct_A_clean_delete* (reference) | clean delete via root.remove_product (del C1 variant A) | ONE=1 IC=0 | 0.500 |
| geometry_test_17 | *ref_C_dirty_delete* (reference) | entity-only delete leaving its psets/relations (del C1 variant C) | ONE=1 IC=0 | 0.500 |
| geometry_test_17 | noop | unchanged file, model_output claims success | ONE=0 IC=0 | 0.000 |
| geometry_test_17 | delete_wrong_element | clean delete of IfcWall 1u4oG4Ltr15fMWjwJ4pN3B instead of the target | ONE=0 IC=0 | 0.000 |
| geometry_test_17 | delete_target_plus_same_class **⚑** | targets plus another IfcWall 1u4oG4Ltr15fMWjwJ4pN3B deleted | ONE=1 IC=0 | 0.500 |
| geometry_test_17 | A_plus_delete_unrelated **⚑** | clean delete + unrelated IfcWall 1u4oG4Ltr15fMWjwJ4pN3B deleted | ONE=1 IC=0 | 0.500 |
| geometry_test_17 | A_plus_junk_duplicate **⚑** | A-delete + coincident duplicate of unrelated IfcWall 1u4oG4Ltr15fMWjwJ4pN3B | ONE=1 IC=0 | 0.500 |
| geometry_test_17 | A_plus_unrelated_geometry_moved **⚑** | A-delete + unrelated IfcWall 1u4oG4Ltr15fMWjwJ4pN3B moved 1 m via geometry | ONE=1 IC=0 | 0.500 |
| geometry_test_17 | A_plus_unrelated_height_halved **⚑** | A-delete + unrelated IfcWall 1u4oG4Ltr15fMWjwJ4pN3B squashed to half height (geometry only) | ONE=1 IC=0 | 0.500 |
| geometry_test_17 | C_plus_junk_duplicate **⚑** | C-delete + coincident duplicate of unrelated IfcWall 1u4oG4Ltr15fMWjwJ4pN3B | ONE=1 IC=0 | 0.500 |
| geometry_test_17 | C_plus_unrelated_geometry_moved **⚑** | C-delete + unrelated IfcWall 1u4oG4Ltr15fMWjwJ4pN3B moved 1 m via geometry | ONE=1 IC=0 | 0.500 |
| geometry_test_17 | C_plus_unrelated_height_halved **⚑** | C-delete + unrelated IfcWall 1u4oG4Ltr15fMWjwJ4pN3B squashed to half height (geometry only) | ONE=1 IC=0 | 0.500 |
| geometry_test_17 | C_plus_unrelated_placement_moved **⚑** | C-delete + unrelated IfcWall 1u4oG4Ltr15fMWjwJ4pN3B moved 1 m via placement | ONE=1 IC=0 | 0.500 |
| geometry_test_17 | target_kept_guid_renamed **⚑** | target NOT deleted: element kept in place, only its GlobalId replaced by a new one | ONE=1 IC=0 | 0.500 |
| geometry_test_17 | partial_delete | only 9 of 10 present targets deleted | ONE=0 IC=0 | 0.000 |
| geometry_test_17 | partial_dirty_delete | only 9 of 10 present targets deleted (entity-only) | ONE=0 IC=0 | 0.000 |
| geometry_test_18 | *correct_A_clean_delete* (reference) | clean delete via root.remove_product (del C1 variant A) | exception → 0 (RuntimeError: Instance with GlobalId '1xzI3PuNvF1RRUjZb8YIP1) | 0.000 |
| geometry_test_18 | *ref_C_dirty_delete* (reference) | entity-only delete leaving its psets/relations (del C1 variant C) | exception → 0 (RuntimeError: Instance with GlobalId '1xzI3PuNvF1RRUjZb8YIP1) | 0.000 |
| geometry_test_18 | noop | unchanged file, model_output claims success | ONE=0 IC=0 | 0.000 |
| geometry_test_18 | delete_wrong_element | clean delete of IfcWindow 1xzI3PuNvF1RRUjZb8YIE6 instead of the target | exception → 0 (RuntimeError: Instance with GlobalId '1xzI3PuNvF1RRUjZb8YIP1) | 0.000 |
| geometry_test_18 | delete_target_plus_same_class | targets plus another IfcWindow 1xzI3PuNvF1RRUjZb8YIE6 deleted | exception → 0 (RuntimeError: Instance with GlobalId '1xzI3PuNvF1RRUjZb8YIP1) | 0.000 |
| geometry_test_18 | A_plus_delete_unrelated | clean delete + unrelated IfcWall 1u4oG4Ltr15fMWjwJ4pN5R deleted | exception → 0 (RuntimeError: Instance with GlobalId '1xzI3PuNvF1RRUjZb8YIP1) | 0.000 |
| geometry_test_18 | A_plus_junk_duplicate | A-delete + coincident duplicate of unrelated IfcWall 1u4oG4Ltr15fMWjwJ4pN5R | exception → 0 (RuntimeError: Instance with GlobalId '1xzI3PuNvF1RRUjZb8YIP1) | 0.000 |
| geometry_test_18 | A_plus_unrelated_geometry_moved | A-delete + unrelated IfcWall 1u4oG4Ltr15fMWjwJ4pN5R moved 1 m via geometry | exception → 0 (RuntimeError: Instance with GlobalId '1xzI3PuNvF1RRUjZb8YIP1) | 0.000 |
| geometry_test_18 | A_plus_unrelated_height_halved | A-delete + unrelated IfcWall 1u4oG4Ltr15fMWjwJ4pN5R squashed to half height (geometry only) | exception → 0 (RuntimeError: Instance with GlobalId '1xzI3PuNvF1RRUjZb8YIP1) | 0.000 |
| geometry_test_18 | C_plus_junk_duplicate | C-delete + coincident duplicate of unrelated IfcWall 1u4oG4Ltr15fMWjwJ4pN5R | exception → 0 (RuntimeError: Instance with GlobalId '1xzI3PuNvF1RRUjZb8YIP1) | 0.000 |
| geometry_test_18 | C_plus_unrelated_geometry_moved | C-delete + unrelated IfcWall 1u4oG4Ltr15fMWjwJ4pN5R moved 1 m via geometry | exception → 0 (RuntimeError: Instance with GlobalId '1xzI3PuNvF1RRUjZb8YIP1) | 0.000 |
| geometry_test_18 | C_plus_unrelated_height_halved | C-delete + unrelated IfcWall 1u4oG4Ltr15fMWjwJ4pN5R squashed to half height (geometry only) | exception → 0 (RuntimeError: Instance with GlobalId '1xzI3PuNvF1RRUjZb8YIP1) | 0.000 |
| geometry_test_18 | C_plus_unrelated_placement_moved | C-delete + unrelated IfcWall 1u4oG4Ltr15fMWjwJ4pN5R moved 1 m via placement | exception → 0 (RuntimeError: Instance with GlobalId '1xzI3PuNvF1RRUjZb8YIP1) | 0.000 |
| geometry_test_18 | target_kept_guid_renamed | target NOT deleted: element kept in place, only its GlobalId replaced by a new one | exception → 0 (RuntimeError: Instance with GlobalId '1xzI3PuNvF1RRUjZb8YIP1) | 0.000 |
| geometry_test_18 | partial_delete | only 1 of 2 present targets deleted | exception → 0 (RuntimeError: Instance with GlobalId '1xzI3PuNvF1RRUjZb8YIP1) | 0.000 |
| geometry_test_18 | partial_dirty_delete | only 1 of 2 present targets deleted (entity-only) | exception → 0 (RuntimeError: Instance with GlobalId '1xzI3PuNvF1RRUjZb8YIP1) | 0.000 |
| geometry_test_19 | *correct_A_clean_delete* (reference) | clean delete via root.remove_product (del C1 variant A) | exception → 0 (RuntimeError: Instance with GlobalId '1mRYVM4YfFFBRkcbz1hH$F) | 0.000 |
| geometry_test_19 | *ref_C_dirty_delete* (reference) | entity-only delete leaving its psets/relations (del C1 variant C) | exception → 0 (RuntimeError: Instance with GlobalId '1mRYVM4YfFFBRkcbz1hH$F) | 0.000 |
| geometry_test_19 | noop | unchanged file, model_output claims success | ONE=0 IC=0 | 0.000 |
| geometry_test_19 | delete_wrong_element | clean delete of IfcWindow 1mRYVM4YfFFBRkcbz1hHvq instead of the target | exception → 0 (RuntimeError: Instance with GlobalId '1mRYVM4YfFFBRkcbz1hH$F) | 0.000 |
| geometry_test_19 | delete_target_plus_same_class | targets plus another IfcWindow 1mRYVM4YfFFBRkcbz1hHvq deleted | exception → 0 (RuntimeError: Instance with GlobalId '1mRYVM4YfFFBRkcbz1hH$F) | 0.000 |
| geometry_test_19 | A_plus_delete_unrelated | clean delete + unrelated IfcWall 1mRYVM4YfFFBRkcbz1hHbp deleted | exception → 0 (RuntimeError: Instance with GlobalId '1mRYVM4YfFFBRkcbz1hH$F) | 0.000 |
| geometry_test_19 | A_plus_junk_duplicate | A-delete + coincident duplicate of unrelated IfcWall 1mRYVM4YfFFBRkcbz1hHbp | exception → 0 (RuntimeError: Instance with GlobalId '1mRYVM4YfFFBRkcbz1hH$F) | 0.000 |
| geometry_test_19 | A_plus_unrelated_geometry_moved | A-delete + unrelated IfcWall 1mRYVM4YfFFBRkcbz1hHbp moved 1 m via geometry | exception → 0 (RuntimeError: Instance with GlobalId '1mRYVM4YfFFBRkcbz1hH$F) | 0.000 |
| geometry_test_19 | A_plus_unrelated_height_halved | A-delete + unrelated IfcWall 1mRYVM4YfFFBRkcbz1hHbp squashed to half height (geometry only) | exception → 0 (RuntimeError: Instance with GlobalId '1mRYVM4YfFFBRkcbz1hH$F) | 0.000 |
| geometry_test_19 | C_plus_junk_duplicate | C-delete + coincident duplicate of unrelated IfcWall 1mRYVM4YfFFBRkcbz1hHbp | exception → 0 (RuntimeError: Instance with GlobalId '1mRYVM4YfFFBRkcbz1hH$F) | 0.000 |
| geometry_test_19 | C_plus_unrelated_geometry_moved | C-delete + unrelated IfcWall 1mRYVM4YfFFBRkcbz1hHbp moved 1 m via geometry | exception → 0 (RuntimeError: Instance with GlobalId '1mRYVM4YfFFBRkcbz1hH$F) | 0.000 |
| geometry_test_19 | C_plus_unrelated_height_halved | C-delete + unrelated IfcWall 1mRYVM4YfFFBRkcbz1hHbp squashed to half height (geometry only) | exception → 0 (RuntimeError: Instance with GlobalId '1mRYVM4YfFFBRkcbz1hH$F) | 0.000 |
| geometry_test_19 | C_plus_unrelated_placement_moved | C-delete + unrelated IfcWall 1mRYVM4YfFFBRkcbz1hHbp moved 1 m via placement | exception → 0 (RuntimeError: Instance with GlobalId '1mRYVM4YfFFBRkcbz1hH$F) | 0.000 |
| geometry_test_19 | target_kept_guid_renamed | target NOT deleted: element kept in place, only its GlobalId replaced by a new one | exception → 0 (RuntimeError: Instance with GlobalId '1mRYVM4YfFFBRkcbz1hH$F) | 0.000 |
| geometry_test_20 | *correct_A_clean_delete* (reference) | clean delete via root.remove_product (del C1 variant A) | ONE=1 IC=0 | 0.500 |
| geometry_test_20 | *ref_C_dirty_delete* (reference) | entity-only delete leaving its psets/relations (del C1 variant C) | ONE=1 IC=0 | 0.500 |
| geometry_test_20 | noop | unchanged file, model_output claims success | ONE=0 IC=0 | 0.000 |
| geometry_test_20 | delete_wrong_element | clean delete of IfcWall 0lwZAgQMb7yAIJTmmcGlc6 instead of the target | ONE=0 IC=0 | 0.000 |
| geometry_test_20 | delete_target_plus_same_class **⚑** | targets plus another IfcWall 0lwZAgQMb7yAIJTmmcGlc6 deleted | ONE=1 IC=0 | 0.500 |
| geometry_test_20 | A_plus_delete_unrelated **⚑** | clean delete + unrelated IfcWall 0lwZAgQMb7yAIJTmmcGlc6 deleted | ONE=1 IC=0 | 0.500 |
| geometry_test_20 | A_plus_junk_duplicate **⚑** | A-delete + coincident duplicate of unrelated IfcWall 0lwZAgQMb7yAIJTmmcGlc6 | ONE=1 IC=0 | 0.500 |
| geometry_test_20 | A_plus_unrelated_geometry_moved **⚑** | A-delete + unrelated IfcWall 0lwZAgQMb7yAIJTmmcGlc6 moved 1 m via geometry | ONE=1 IC=0 | 0.500 |
| geometry_test_20 | A_plus_unrelated_height_halved **⚑** | A-delete + unrelated IfcWall 0lwZAgQMb7yAIJTmmcGlc6 squashed to half height (geometry only) | ONE=1 IC=0 | 0.500 |
| geometry_test_20 | C_plus_junk_duplicate **⚑** | C-delete + coincident duplicate of unrelated IfcWall 0lwZAgQMb7yAIJTmmcGlc6 | ONE=1 IC=0 | 0.500 |
| geometry_test_20 | C_plus_unrelated_geometry_moved **⚑** | C-delete + unrelated IfcWall 0lwZAgQMb7yAIJTmmcGlc6 moved 1 m via geometry | ONE=1 IC=0 | 0.500 |
| geometry_test_20 | C_plus_unrelated_height_halved **⚑** | C-delete + unrelated IfcWall 0lwZAgQMb7yAIJTmmcGlc6 squashed to half height (geometry only) | ONE=1 IC=0 | 0.500 |
| geometry_test_20 | C_plus_unrelated_placement_moved **⚑** | C-delete + unrelated IfcWall 0lwZAgQMb7yAIJTmmcGlc6 moved 1 m via placement | ONE=1 IC=0 | 0.500 |
| geometry_test_20 | target_kept_guid_renamed **⚑** | target NOT deleted: element kept in place, only its GlobalId replaced by a new one | ONE=1 IC=0 | 0.500 |
| topological_test_16 | *correct_A_clean_delete* (reference) | clean delete via root.remove_product (del C1 variant A) | ONE=1 IC=0 | 0.500 |
| topological_test_16 | *ref_C_dirty_delete* (reference) | entity-only delete leaving its psets/relations (del C1 variant C) | ONE=1 IC=0 | 0.500 |
| topological_test_16 | noop | unchanged file, model_output claims success | ONE=0 IC=0 | 0.000 |
| topological_test_16 | delete_wrong_element | clean delete of IfcWall 3cmsjRvPb4wf9t15K203_D instead of the target | ONE=0 IC=0 | 0.000 |
| topological_test_16 | delete_target_plus_same_class **⚑** | targets plus another IfcWall 3cmsjRvPb4wf9t15K203_D deleted | ONE=1 IC=0 | 0.500 |
| topological_test_16 | A_plus_delete_unrelated **⚑** | clean delete + unrelated IfcWall 3cmsjRvPb4wf9t15K203_D deleted | ONE=1 IC=0 | 0.500 |
| topological_test_16 | A_plus_junk_duplicate **⚑** | A-delete + coincident duplicate of unrelated IfcWall 3cmsjRvPb4wf9t15K203_D | ONE=1 IC=0 | 0.500 |
| topological_test_16 | A_plus_unrelated_geometry_moved **⚑** | A-delete + unrelated IfcWall 3cmsjRvPb4wf9t15K203_D moved 1 m via geometry | ONE=1 IC=0 | 0.500 |
| topological_test_16 | A_plus_unrelated_height_halved **⚑** | A-delete + unrelated IfcWall 3cmsjRvPb4wf9t15K203_D squashed to half height (geometry only) | ONE=1 IC=0 | 0.500 |
| topological_test_16 | C_plus_junk_duplicate **⚑** | C-delete + coincident duplicate of unrelated IfcWall 3cmsjRvPb4wf9t15K203_D | ONE=1 IC=0 | 0.500 |
| topological_test_16 | C_plus_unrelated_geometry_moved **⚑** | C-delete + unrelated IfcWall 3cmsjRvPb4wf9t15K203_D moved 1 m via geometry | ONE=1 IC=0 | 0.500 |
| topological_test_16 | C_plus_unrelated_height_halved **⚑** | C-delete + unrelated IfcWall 3cmsjRvPb4wf9t15K203_D squashed to half height (geometry only) | ONE=1 IC=0 | 0.500 |
| topological_test_16 | C_plus_unrelated_placement_moved **⚑** | C-delete + unrelated IfcWall 3cmsjRvPb4wf9t15K203_D moved 1 m via placement | ONE=1 IC=0 | 0.500 |
| topological_test_16 | target_kept_guid_renamed **⚑** | target NOT deleted: element kept in place, only its GlobalId replaced by a new one | ONE=1 IC=0 | 0.500 |
| topological_test_17 | *correct_A_clean_delete* (reference) | clean delete via root.remove_product (del C1 variant A) | ONE=1 IC=0 | 0.500 |
| topological_test_17 | *ref_C_dirty_delete* (reference) | entity-only delete leaving its psets/relations (del C1 variant C) | ONE=1 IC=1 | 1.000 |
| topological_test_17 | noop | unchanged file, model_output claims success | ONE=0 IC=0 | 0.000 |
| topological_test_17 | delete_wrong_element | clean delete of IfcColumn 2IIWDJ6bzEPxU4iXeUX9cP instead of the target | ONE=0 IC=0 | 0.000 |
| topological_test_17 | delete_target_plus_same_class **⚑** | targets plus another IfcColumn 2IIWDJ6bzEPxU4iXeUX9cP deleted | ONE=1 IC=0 | 0.500 |
| topological_test_17 | A_plus_delete_unrelated **⚑** | clean delete + unrelated IfcColumn 2IIWDJ6bzEPxU4iXeUX9cP deleted | ONE=1 IC=0 | 0.500 |
| topological_test_17 | A_plus_junk_duplicate **⚑** | A-delete + coincident duplicate of unrelated IfcColumn 2IIWDJ6bzEPxU4iXeUX9cP | ONE=1 IC=0 | 0.500 |
| topological_test_17 | A_plus_unrelated_geometry_moved **⚑** | A-delete + unrelated IfcColumn 2IIWDJ6bzEPxU4iXeUX9cP moved 1 m via geometry | ONE=1 IC=0 | 0.500 |
| topological_test_17 | A_plus_unrelated_height_halved **⚑** | A-delete + unrelated IfcColumn 2IIWDJ6bzEPxU4iXeUX9cP squashed to half height (geometry only) | ONE=1 IC=0 | 0.500 |
| topological_test_17 | C_plus_junk_duplicate **⚑** | C-delete + coincident duplicate of unrelated IfcColumn 2IIWDJ6bzEPxU4iXeUX9cP | ONE=1 IC=1 | 1.000 |
| topological_test_17 | C_plus_unrelated_geometry_moved **⚑** | C-delete + unrelated IfcColumn 2IIWDJ6bzEPxU4iXeUX9cP moved 1 m via geometry | ONE=1 IC=1 | 1.000 |
| topological_test_17 | C_plus_unrelated_height_halved **⚑** | C-delete + unrelated IfcColumn 2IIWDJ6bzEPxU4iXeUX9cP squashed to half height (geometry only) | ONE=1 IC=1 | 1.000 |
| topological_test_17 | C_plus_unrelated_placement_moved **⚑** | C-delete + unrelated IfcColumn 2IIWDJ6bzEPxU4iXeUX9cP moved 1 m via placement | ONE=1 IC=0 | 0.500 |
| topological_test_17 | target_kept_guid_renamed **⚑** | target NOT deleted: element kept in place, only its GlobalId replaced by a new one | ONE=1 IC=1 | 1.000 |
| topological_test_17 | partial_delete | only 4 of 5 present targets deleted | ONE=0 IC=0 | 0.000 |
| topological_test_17 | partial_dirty_delete **⚑** | only 4 of 5 present targets deleted (entity-only) | ONE=0 IC=1 | 0.500 |
| topological_test_18 | *correct_A_clean_delete* (reference) | clean delete via root.remove_product (del C1 variant A) | ONE=1 IC=0 | 0.500 |
| topological_test_18 | *ref_C_dirty_delete* (reference) | entity-only delete leaving its psets/relations (del C1 variant C) | ONE=1 IC=1 | 1.000 |
| topological_test_18 | noop | unchanged file, model_output claims success | ONE=0 IC=0 | 0.000 |
| topological_test_18 | delete_wrong_element | clean delete of IfcSpace 3Vyqk8cSj8TOuAk6zHUwKx instead of the target | ONE=0 IC=0 | 0.000 |
| topological_test_18 | delete_target_plus_same_class **⚑** | targets plus another IfcSpace 3Vyqk8cSj8TOuAk6zHUwKx deleted | ONE=1 IC=0 | 0.500 |
| topological_test_18 | A_plus_delete_unrelated **⚑** | clean delete + unrelated IfcWall 3Vyqk8cSj8TOuAk6zHUwMJ deleted | ONE=1 IC=0 | 0.500 |
| topological_test_18 | A_plus_junk_duplicate **⚑** | A-delete + coincident duplicate of unrelated IfcWall 3Vyqk8cSj8TOuAk6zHUwMJ | ONE=1 IC=0 | 0.500 |
| topological_test_18 | A_plus_unrelated_geometry_moved **⚑** | A-delete + unrelated IfcWall 3Vyqk8cSj8TOuAk6zHUwMJ moved 1 m via geometry | ONE=1 IC=0 | 0.500 |
| topological_test_18 | A_plus_unrelated_height_halved **⚑** | A-delete + unrelated IfcWall 3Vyqk8cSj8TOuAk6zHUwMJ squashed to half height (geometry only) | ONE=1 IC=0 | 0.500 |
| topological_test_18 | C_plus_junk_duplicate **⚑** | C-delete + coincident duplicate of unrelated IfcWall 3Vyqk8cSj8TOuAk6zHUwMJ | ONE=1 IC=1 | 1.000 |
| topological_test_18 | C_plus_unrelated_geometry_moved **⚑** | C-delete + unrelated IfcWall 3Vyqk8cSj8TOuAk6zHUwMJ moved 1 m via geometry | ONE=1 IC=1 | 1.000 |
| topological_test_18 | C_plus_unrelated_height_halved **⚑** | C-delete + unrelated IfcWall 3Vyqk8cSj8TOuAk6zHUwMJ squashed to half height (geometry only) | ONE=1 IC=1 | 1.000 |
| topological_test_18 | C_plus_unrelated_placement_moved **⚑** | C-delete + unrelated IfcWall 3Vyqk8cSj8TOuAk6zHUwMJ moved 1 m via placement | ONE=1 IC=0 | 0.500 |
| topological_test_18 | target_kept_guid_renamed **⚑** | target NOT deleted: element kept in place, only its GlobalId replaced by a new one | ONE=1 IC=1 | 1.000 |
| topological_test_19 | *correct_A_clean_delete* (reference) | clean delete via root.remove_product (del C1 variant A) | ONE=1 IC=0 | 0.500 |
| topological_test_19 | *ref_C_dirty_delete* (reference) | entity-only delete leaving its psets/relations (del C1 variant C) | ONE=1 IC=1 | 1.000 |
| topological_test_19 | noop | unchanged file, model_output claims success | ONE=0 IC=0 | 0.000 |
| topological_test_19 | A_plus_delete_unrelated **⚑** | clean delete + unrelated IfcWall 3Vyqk8cSj8TOuAk6zHUwAt deleted | ONE=1 IC=0 | 0.500 |
| topological_test_19 | A_plus_junk_duplicate **⚑** | A-delete + coincident duplicate of unrelated IfcWall 3Vyqk8cSj8TOuAk6zHUwAt | ONE=1 IC=0 | 0.500 |
| topological_test_19 | A_plus_unrelated_geometry_moved **⚑** | A-delete + unrelated IfcWall 3Vyqk8cSj8TOuAk6zHUwAt moved 1 m via geometry | ONE=1 IC=0 | 0.500 |
| topological_test_19 | A_plus_unrelated_height_halved **⚑** | A-delete + unrelated IfcWall 3Vyqk8cSj8TOuAk6zHUwAt squashed to half height (geometry only) | ONE=1 IC=0 | 0.500 |
| topological_test_19 | C_plus_junk_duplicate **⚑** | C-delete + coincident duplicate of unrelated IfcWall 3Vyqk8cSj8TOuAk6zHUwAt | ONE=1 IC=1 | 1.000 |
| topological_test_19 | C_plus_unrelated_geometry_moved **⚑** | C-delete + unrelated IfcWall 3Vyqk8cSj8TOuAk6zHUwAt moved 1 m via geometry | ONE=1 IC=1 | 1.000 |
| topological_test_19 | C_plus_unrelated_height_halved **⚑** | C-delete + unrelated IfcWall 3Vyqk8cSj8TOuAk6zHUwAt squashed to half height (geometry only) | ONE=1 IC=1 | 1.000 |
| topological_test_19 | C_plus_unrelated_placement_moved **⚑** | C-delete + unrelated IfcWall 3Vyqk8cSj8TOuAk6zHUwAt moved 1 m via placement | ONE=1 IC=0 | 0.500 |
| topological_test_19 | target_kept_guid_renamed **⚑** | target NOT deleted: element kept in place, only its GlobalId replaced by a new one | ONE=1 IC=1 | 1.000 |
| topological_test_20 | *correct_A_clean_delete* (reference) | clean delete via root.remove_product (del C1 variant A) | ONE=0 IC=0 | 0.000 |
| topological_test_20 | *ref_C_dirty_delete* (reference) | entity-only delete leaving its psets/relations (del C1 variant C) | ONE=0 IC=1 | 0.500 |
| topological_test_20 | noop | unchanged file, model_output claims success | ONE=0 IC=0 | 0.000 |
| topological_test_20 | delete_wrong_element | clean delete of IfcColumn 0CGowky6PBXuUPvpf59ezk instead of the target | ONE=0 IC=0 | 0.000 |
| topological_test_20 | delete_target_plus_same_class | targets plus another IfcColumn 0CGowky6PBXuUPvpf59ezk deleted | ONE=0 IC=0 | 0.000 |
| topological_test_20 | A_plus_delete_unrelated | clean delete + unrelated IfcColumn 0CGowky6PBXuUPvpf59ezk deleted | ONE=0 IC=0 | 0.000 |
| topological_test_20 | A_plus_junk_duplicate | A-delete + coincident duplicate of unrelated IfcColumn 0CGowky6PBXuUPvpf59ezk | ONE=0 IC=0 | 0.000 |
| topological_test_20 | A_plus_unrelated_geometry_moved | A-delete + unrelated IfcColumn 0CGowky6PBXuUPvpf59ezk moved 1 m via geometry | ONE=0 IC=0 | 0.000 |
| topological_test_20 | A_plus_unrelated_height_halved | A-delete + unrelated IfcColumn 0CGowky6PBXuUPvpf59ezk squashed to half height (geometry only) | ONE=0 IC=0 | 0.000 |
| topological_test_20 | C_plus_junk_duplicate **⚑** | C-delete + coincident duplicate of unrelated IfcColumn 0CGowky6PBXuUPvpf59ezk | ONE=0 IC=1 | 0.500 |
| topological_test_20 | C_plus_unrelated_geometry_moved **⚑** | C-delete + unrelated IfcColumn 0CGowky6PBXuUPvpf59ezk moved 1 m via geometry | ONE=0 IC=1 | 0.500 |
| topological_test_20 | C_plus_unrelated_height_halved **⚑** | C-delete + unrelated IfcColumn 0CGowky6PBXuUPvpf59ezk squashed to half height (geometry only) | ONE=0 IC=1 | 0.500 |
| topological_test_20 | C_plus_unrelated_placement_moved | C-delete + unrelated IfcColumn 0CGowky6PBXuUPvpf59ezk moved 1 m via placement | ONE=0 IC=0 | 0.000 |
| topological_test_20 | target_kept_guid_renamed **⚑** | target NOT deleted: element kept in place, only its GlobalId replaced by a new one | ONE=0 IC=1 | 0.500 |
| topological_test_20 | partial_delete | only 3 of 4 present targets deleted | ONE=0 IC=0 | 0.000 |
| topological_test_20 | partial_dirty_delete **⚑** | only 3 of 4 present targets deleted (entity-only) | ONE=0 IC=1 | 0.500 |

