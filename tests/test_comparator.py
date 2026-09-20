import unittest
from services.llm_service import LLMService
from services.document_service import DocumentService
from agents.comparator_agent import ComparatorAgent

class TestComparator(unittest.TestCase):
    def test_comparator_execution(self):
        llm = LLMService(mode="DEMO")
        doc_service = DocumentService()
        agent = ComparatorAgent(llm, doc_service)
        
        # Test handling when docs don't exist
        res = agent.run("nonexistent1.pdf", "nonexistent2.pdf")
        self.assertEqual(res["status"], "Failed")

if __name__ == "__main__":
    unittest.main()
