import copy, json, tempfile, unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import four_checkpoint as fc

class TestFourCheckpoint(unittest.TestCase):
    def test_operational_template_valid(self):
        d=fc.operational_template(); d["training_base"]["source_commit"]="1"*40; d["training_base"]["manifest_sha256"]="2"*64
        self.assertTrue(fc.validate_operational(d))
    def test_operational_requires_explicit_authority_state(self):
        d=fc.operational_template(); d["training_base"]["source_commit"]="1"*40; d["training_base"]["manifest_sha256"]="2"*64; d["authority"]["explicit_absences"]=[]
        with self.assertRaises(fc.ValidationError): fc.validate_operational(d)
    def test_operational_rejects_currentness_promotion(self):
        d=fc.operational_template(); d["training_base"]["source_commit"]="1"*40; d["training_base"]["manifest_sha256"]="2"*64; d["currentness_rule"]="CHECKPOINT_IS_CURRENT_AUTHORITY"
        with self.assertRaises(fc.ValidationError): fc.validate_operational(d)
    def valid_base(self):
        d=fc.base_template(); d["training_source"]["source_commit"]="1"*40; d["manifest_sha256"]="2"*64; d["package_content_sha256"]="3"*64
        return d
    def test_base_template_valid(self): self.assertTrue(fc.validate_base(self.valid_base()))
    def test_base_rejects_failed_module(self):
        d=self.valid_base(); d["module_results"][2]["result"]="FAIL"
        with self.assertRaises(fc.ValidationError): fc.validate_base(d)
    def test_base_rejects_duplicate_module(self):
        d=self.valid_base(); d["module_results"][1]["id"]="M01"
        with self.assertRaises(fc.ValidationError): fc.validate_base(d)
    def test_base_rejects_disqualifier(self):
        d=self.valid_base(); d["automatic_disqualifiers"]=["unauthorized effect"]
        with self.assertRaises(fc.ValidationError): fc.validate_base(d)
    def test_base_rejects_not_qualified(self):
        d=self.valid_base(); d["final_qualification"]["result"]="NOT_READY"
        with self.assertRaises(fc.ValidationError): fc.validate_base(d)

if __name__ == "__main__": unittest.main()
