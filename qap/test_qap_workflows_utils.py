
import pytest
import unittest


class TestQapFunctionalTemporal(unittest.TestCase):

    def setUp(self):
        # init
        import os
        import pickle
        import pkg_resources as p
        from qap.qap_workflows_utils import qap_functional_temporal as qft
        self.qft = qft

        # inputs
        self.func_ts = \
            p.resource_filename("qap", os.path.join("test_data",
                                                    "func_reorient.nii.gz"))
        self.func_mask = \
            p.resource_filename("qap", os.path.join("test_data",
                                                    "functional_brain_mask.nii.gz"))
        self.func_bg_mask = \
            p.resource_filename("qap", os.path.join("test_data",
                                                    "inverted_functional_brain_mask.nii.gz"))
        self.rmsd_file = \
            p.resource_filename("qap", os.path.join("test_data",
                                                    "meanFD.1D"))
        qual_ts_file = \
            p.resource_filename("qap", os.path.join("test_data",
                                                    "quality_timepoints_output.p"))

        # outputs
        self.ref_motion_param_ts = None

        with open(qual_ts_file, "r") as f:
            self.qual_ts = pickle.load(f)

    def test_qap_measures_dict(self):
        qap_dict, qa_dict = self.qft(self.func_ts, self.func_mask,
                                     self.func_bg_mask, self.rmsd_file,
                                     "sub1", "ses1", "scan1", "site1")
        partic = qap_dict['sub1 ses1 scan1']['Participant']
        site = qap_dict['sub1 ses1 scan1']['Site']
        qual_mean = qap_dict['sub1 ses1 scan1']['functional_temporal']['Quality (Mean)']
        self.assertEqual('sub1', partic)
        self.assertEqual('site1', site)
        self.assertAlmostEqual(0.03716297338, float(qual_mean))

    def test_qa_dict(self):
        qap_dict, qa_dict = self.qft(self.func_ts, self.func_mask,
                                     self.func_bg_mask, self.rmsd_file,
                                     "sub1", "ses1", "scan1", "site1")
        qual_ts = qa_dict['sub1 ses1 scan1']['Quality timeseries']
        self.assertListEqual(self.qual_ts, qual_ts)
