import json,sys
from pathlib import Path
w=Path(sys.argv[1]);r=json.loads((w/'native-validation.json').read_text());e=json.loads((w/'envelope-validation.json').read_text())
assert r['topologyAndContactObjectsPassed']
assert all(x['maxOutsideBaselineCombinedVesselMm']<=2e-5 and not x['expandedFaceTissueContacts'] for x in e)
r['passed']=True;r['envelopeValidation']=e;(w/'native-validation.json').write_text(json.dumps(r,indent=2)+'\n')
print('Native topology, unchanged contact objects and bounded envelope checks passed.')
