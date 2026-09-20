import unittest
from agents.orchestrator import OrchestratorAgent

class TestOrchestrator(unittest.TestCase):
    def setUp(self):
        self.orchestrator = OrchestratorAgent()

    def test_summarize_routing(self):
        route = self.orchestrator.route_request("Please summarize the security policy document.")
        self.assertEqual(route["agent"], "SUMMARIZER")

    def test_comparator_routing(self):
        route = self.orchestrator.route_request("What changed between V1 and V2 policy files?")
        self.assertEqual(route["agent"], "COMPARATOR")

    def test_qa_routing(self):
        route = self.orchestrator.route_request("What is the maximum allowed leave count?")
        self.assertEqual(route["agent"], "QA")

if __name__ == "__main__":
    unittest.main()
