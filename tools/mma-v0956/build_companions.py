"""Build companion teaching channels around the corrected arterial course."""
from clear_neural import *
import smooth_fields
original_field=smooth_fields.arterial_field
data=np.load(WORK/('outward-flow.npz' if '--outward' in sys.argv else 'neural-flow.npz'))
steps=[Step(p,d) for p,d in zip(data['points'],data['vectors'])]
def corrected_field():
    baseline=original_field()
    def transform(v):
        q=baseline(v)
        for step in steps:q=step(q)
        return q
    return transform
smooth_fields.arterial_field=corrected_field
exec(compile((Path(__file__).parents[1]/'mma-v0952/build_paired_veins.py').read_text(),'build_paired_veins.py','exec'))
