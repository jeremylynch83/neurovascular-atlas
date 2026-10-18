"""Verify immutable production-coordinate crossing regressions."""
from pathlib import Path
import sys,json,argparse
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'tools/repair'))
from geometry import triangle_crosses,triangle_crosses_exact
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path);args=p.parse_args()
E=A/'anatomy/source/intersection-predicate-v0.9.114';rows=json.load(open(E/'predicate-fixtures.json'))+[json.load(open(E/'a5-distal-contact-fixture.json'))];results=[]
for row in rows:
 expected=row['expected'];exact=triangle_crosses_exact(row['a'],row['b']);actual=triangle_crosses(row['a'],row['b']);results.append({'node':row['node'],'faces':row['faces'],'expected':expected,'exact':exact,'actual':actual,'passed':exact==expected and actual==expected})
report={'passed':all(r['passed']for r in results),'fixtureCases':len(results),'genuineCrossingsRetained':sum(r['expected']for r in results),'falseReportsRejected':sum(not r['expected']for r in results),'results':results}
if args.output:args.output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items()if k!='results'},indent=2));raise SystemExit(0 if report['passed']else 1)
