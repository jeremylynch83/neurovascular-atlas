"""Exclusions must not survive an untracked change to validation code."""
from pathlib import Path
import hashlib,importlib.util,tempfile,unittest
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('deferred_guard',ROOT/'tools/arterial-review-v0.9.113/check_deferred.py')
guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)

class DeferredGuardTests(unittest.TestCase):
    def fixture(self,root):
        source=root/'public/anatomy/models/fixture.glb';source.parent.mkdir(parents=True);source.write_bytes(b'unchanged source')
        code=root/'tools/repair/geometry.py';code.parent.mkdir(parents=True);code.write_bytes(b'predicate v2')
        return {'requiredSourceAssetSha256':{'models/fixture.glb':hashlib.sha256(source.read_bytes()).hexdigest()},'requiredImplementationSha256':{'tools/repair/geometry.py':hashlib.sha256(code.read_bytes()).hexdigest()}}
    def test_matching_source_and_code_reuses_exclusions(self):
        with tempfile.TemporaryDirectory()as tmp:
            root=Path(tmp);registry=self.fixture(root);self.assertEqual(guard.check_assets(root,registry),[])
    def test_code_change_invalidates_unchanged_geometry(self):
        with tempfile.TemporaryDirectory()as tmp:
            root=Path(tmp);registry=self.fixture(root);(root/'tools/repair/geometry.py').write_bytes(b'predicate v3')
            self.assertEqual(guard.check_assets(root,registry),[{'asset':'tools/repair/geometry.py','reason':'implementation-bytes-changed'}])
    def test_legacy_geometry_only_exclusions_require_review(self):
        with tempfile.TemporaryDirectory()as tmp:
            root=Path(tmp);registry=self.fixture(root);del registry['requiredImplementationSha256']
            self.assertEqual(guard.check_assets(root,registry),[{'asset':'review-implementation','reason':'implementation-hashes-not-recorded'}])

if __name__=='__main__':unittest.main()
