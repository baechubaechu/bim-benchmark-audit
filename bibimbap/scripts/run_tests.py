import sys, json, importlib, csv
sys.path.insert(0, '/tmp/bib/bibimbap')
D = '/tmp/bib/olddata/data/ifc/'
rows = {r['test']: r for r in csv.DictReader(open('/tmp/bib/olddata/data/prompts/all_questions.csv'))}
R = ''
# task -> (schema key, primary answer, {label: alternative values})
A = {
 'test_06': ('area', 150.0, {'space Body extrusion 10x15': 150.0}),
 'test_07': ('length', 10.2, {'axis/extrusion length': 10.2}),
 'test_08': ('volume', 457.2, {'space Body vol (h=3.048)': 457.2, 'floor area x wall height 3.6': 540.0}),
 'test_09': ('distance', 10.0, {}),
 'test_10': ('global_id', '22hyxvAPr65PFt9WZfHSP3', {}),
 'geometry_test_06': ('length', 7.2, {'inner clear 7.0': 7.0, 'outer 7.4': 7.4}),
 'geometry_test_07': ('global_id', '1pkLoAx5P7Lwxnk7MMv3Lz', {}),
 'geometry_test_08': ('distance_m', 4.0, {'centre-line 4.2': 4.2, 'outer faces 4.4': 4.4}),
 'geometry_test_09': ('wall_ids', ['2I2XyofMDDYhKncvMedHww', '2I2XyofMDDYhKncvMedHX0', '2I2XyofMDDYhKncvMedH$i'], {}),
 'geometry_test_10': ('value', 5.9, {'axis 6.1': 6.1, 'outer 6.3': 6.3}),
 'topological_test_06': ('global_id', '3Vyqk8cSj8TOuAk6zHUw89', {}),
 'topological_test_07': ('global_ids', ['1NO2FmQyX8Dx48Vy4bqK11', '1NO2FmQyX8Dx48Vy4bqK9m'], {}),
 'topological_test_08': ('global_ids', ['3wugWiepr7zgNK68VeZIat', '3wugWiepr7zgNK68VeZIH7'], {}),
 'topological_test_09': ('global_id', '3Vyqk8cSj8TOuAk6zHUwKx', {}),
 'topological_test_10': ('global_id', '0rTWnvc$TEcxPkiz6YVMaY', {}),
 'numeric_test_01': ('value', 17.11, {}),
 'numeric_test_02': ('value', 42.70, {}),
 'numeric_test_03': ('value', 51.83, {'L2 slab footprint 86.265': 86.265, 'L2 space NFA 44.83': 44.83}),
 'numeric_test_04': ('value', 138.095, {'slab footprints 2x86.265': 172.53}),
 'numeric_test_05': ('value', 33.6, {'exposed excl. nB end face': 33.0, 'axis length x h': 34.8}),
 'numeric_test_06': ('value', 36.0, {'axis length x h': 34.8}),
 'numeric_test_07': ('value', 20.22, {'room-side clear incl. nB end face (key)': 20.82, 'both sides of partition': 25.14, 'axis/untrimmed one side': 21.42}),
 'numeric_test_08': ('value', 27.3, {}),
 'numeric_test_09': ('value', 36.0, {}),
 'numeric_test_10': ('value', 25.2, {'exposed own faces 24.0': 24.0, 'room-side clear incl. nB end face (key)': 24.6, 'untrimmed + nB end': 25.8, 'both sides of nG': 32.7}),
 'numeric_test_11': ('value', 11.25, {'>= 2 m2': 13.25}),
 'numeric_test_12': ('value', 3.4, {}),
 'numeric_test_13': ('value', 24.3, {}),
 'numeric_test_14': ('value', 3.625, {}),
 'numeric_test_15': ('value', 3, {'>= 2 m2': 4}),
 'numeric_test_16': ('value', 1.7325, {'opening AREA sum (key)': 5.775}),
 'numeric_test_17': ('value', 12.932, {'gross volume (no opening deduction)': 14.58, 'net one-side wall AREA (key)': 64.66}),
 'numeric_test_18': ('value', 51.06, {'without column deduction': 51.33}),
 'numeric_test_19': ('value', 15.53625, {'upper slab only net vol': 6.79125, 'upper slab net AREA (key)': 22.6375}),
 'numeric_test_20': ('value', 44.6, {'incl. column-void perimeter': 45.8}),
}
out = {}
for t, (k, ans, alts) in A.items():
    mod = importlib.import_module('data.tests.' + t)
    ifc = D + rows[t]['ifc-file']
    res = {'primary': ans, 'primary_result': mod.execute_test(ifc, ifc, {k: ans, 'raw_model_response': R}), 'alternatives': {}}
    for lab, v in alts.items():
        res['alternatives'][lab] = {'value': v, 'result': mod.execute_test(ifc, ifc, {k: v, 'raw_model_response': R})}
    out[t] = res
    print(t, ans, res['primary_result'], {l: (a['value'], a['result']['right_answer']) for l, a in res['alternatives'].items()})
json.dump(out, open('test_runs.json', 'w'), indent=1)
