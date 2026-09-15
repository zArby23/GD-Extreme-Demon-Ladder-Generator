import unittest

from gd_extreme_demon_ladder_generator.core.ladder_builder import LadderBuilder


class LadderBuilderTests(unittest.TestCase):
    def test_log_positions_include_both_endpoints(self):
        positions = LadderBuilder([]).generate_log_positions(1, 100, 2)

        self.assertEqual(positions[0], 1)
        self.assertEqual(positions[-1], 100)
        self.assertEqual(len(positions), 3)

    def test_log_positions_reject_invalid_steps(self):
        with self.assertRaises(ValueError):
            LadderBuilder([]).generate_log_positions(1, 100, 0)
