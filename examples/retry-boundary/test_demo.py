"""Assertions about the public fixture, not about any customer or private runtime."""
import importlib.util
import json
from pathlib import Path
import socket
import sys
import unittest
from unittest.mock import patch

path = Path(__file__).with_name('demo.py')
spec = importlib.util.spec_from_file_location('public_retry_demo', path)
demo = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = demo
spec.loader.exec_module(demo)


class DemoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = demo.run_demo()
        cls.rows = {row['case']: row for row in cls.report['cases']}

    def test_normal(self):
        r = self.rows['normal']
        self.assertEqual(r['client_states'], ['NEW_BOOKING_CONFIRMED'])
        self.assertEqual(r['observed_booking_rows'], 1)

    def test_unsafe_retry_reproduces_duplicate(self):
        r = self.rows['unsafe_retry']
        self.assertEqual(r['effects_after_first_attempt'], 1)
        self.assertEqual(r['client_states'], ['OUTCOME_UNKNOWN', 'NEW_BOOKING_CONFIRMED'])
        self.assertEqual((r['service_calls'], r['observed_booking_rows']), (2, 2))
        self.assertEqual(r['workflow_result'], 'FAIL_DUPLICATE_EFFECT')

    def test_guarded_retry_does_not_duplicate_fixture_effect(self):
        r = self.rows['guarded_retry']
        self.assertEqual(r['client_states'], ['OUTCOME_UNKNOWN', 'EXISTING_BOOKING_CONFIRMED'])
        self.assertEqual((r['service_calls'], r['observed_booking_rows']), (2, 1))

    def test_lost_response_is_not_called_success(self):
        r = self.rows['unknown_without_retry']
        self.assertEqual(r['client_states'], ['OUTCOME_UNKNOWN'])
        self.assertEqual((r['service_calls'], r['observed_booking_rows']), (1, 1))

    def test_changed_payload_stops_before_service(self):
        r = self.rows['changed_payload']
        self.assertEqual(r['client_states'], ['APPROVAL_DENIED'])
        self.assertEqual((r['service_calls'], r['observed_booking_rows']), (0, 0))

    def test_expiry_boundary_stops_before_service(self):
        r = self.rows['expired_approval']
        self.assertEqual(r['client_states'], ['APPROVAL_DENIED'])
        self.assertEqual((r['service_calls'], r['observed_booking_rows']), (0, 0))

    def test_revocation_stops_before_service(self):
        r = self.rows['revoked_approval']
        self.assertEqual(r['client_states'], ['APPROVAL_DENIED'])
        self.assertEqual((r['service_calls'], r['observed_booking_rows']), (0, 0))

    def test_key_reuse_with_new_payload_rejected(self):
        r = self.rows['key_payload_conflict']
        self.assertEqual(r['client_states'], ['NEW_BOOKING_CONFIRMED', 'IDEMPOTENCY_KEY_CONFLICT'])
        self.assertEqual((r['service_calls'], r['observed_booking_rows']), (2, 1))

    def test_dedupe_survives_connection_reopen(self):
        r = self.rows['database_reopen']
        self.assertEqual(r['client_states'], ['OUTCOME_UNKNOWN', 'EXISTING_BOOKING_CONFIRMED'])
        self.assertEqual((r['service_calls'], r['observed_booking_rows']), (2, 1))
        self.assertFalse(self.report['process_restart_tested'])

    def test_repeated_runs_have_identical_results(self):
        self.assertEqual(self.report, demo.run_demo())

    def test_all_cases_run_with_network_functions_blocked(self):
        with patch.object(socket, 'socket', side_effect=AssertionError('network forbidden')), \
             patch.object(socket, 'create_connection', side_effect=AssertionError('network forbidden')), \
             patch.object(socket, 'getaddrinfo', side_effect=AssertionError('DNS forbidden')):
            self.assertEqual(self.report, demo.run_demo())

    def test_json_output_is_finite_and_explicitly_synthetic(self):
        self.assertEqual(len(self.rows), 9)
        self.assertTrue(self.report['synthetic_only'])
        self.assertFalse(self.report['customer_system_tested'])
        self.assertEqual(self.report['network_requests'], 0)
        json.dumps(self.report, allow_nan=False)


if __name__ == '__main__':
    unittest.main(verbosity=2)
