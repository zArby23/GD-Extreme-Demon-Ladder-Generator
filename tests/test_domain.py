import unittest
from unittest.mock import Mock, patch

from gd_extreme_demon_ladder_generator.api.aredl_client import (
    AREDLClient,
    AREDLClientError,
)
from gd_extreme_demon_ladder_generator.core.ladder_builder import LadderBuilder
from gd_extreme_demon_ladder_generator.core.models import DemonLevel


class LadderBuilderTests(unittest.TestCase):
    def test_log_positions_include_both_endpoints(self):
        positions = LadderBuilder([]).generate_log_positions(1, 100, 2)

        self.assertEqual(positions[0], 1)
        self.assertEqual(positions[-1], 100)
        self.assertEqual(len(positions), 3)

    def test_log_positions_reject_invalid_steps(self):
        with self.assertRaises(ValueError):
            LadderBuilder([]).generate_log_positions(1, 100, 0)

    def test_build_only_adds_interior_steps(self):
        start = DemonLevel("start", "Start", 100, 1)
        target = DemonLevel("target", "Target", 1, 2)
        interior = DemonLevel("interior", "Interior", 10, 3)

        ladder = LadderBuilder([start, target, interior]).build(
            start, target, steps=2, window=100
        )

        self.assertEqual([level.level_id for level in ladder], [1, 3, 2])


class AREDLClientTests(unittest.TestCase):
    def test_rejects_a_non_list_levels_payload(self):
        response = Mock()
        response.json.return_value = {"level": "unexpected"}
        client = AREDLClient("https://example.test", timeout=1)

        with patch("requests.get", return_value=response):
            with self.assertRaises(AREDLClientError):
                client.fetch_levels()
