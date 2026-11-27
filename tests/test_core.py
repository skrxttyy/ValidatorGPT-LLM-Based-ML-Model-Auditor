import unittest
from validatorgpt.core import *

class AuditTests(unittest.TestCase):
    def test_confusion(self):
        value = audit([0, 0, 1, 1], [.1, .8, .9, .2])
        self.assertEqual([value[k] for k in ['tn','fp','fn','tp']], [1,1,1,1])
        self.assertEqual(value['recall'], .5)

    def test_invalid_probability(self):
        with self.assertRaises(ValueError):
            audit([0, 1], [.2, float('nan')])
