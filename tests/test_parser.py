import unittest
import os
from document_processing.parser import DocumentParser

class TestDocumentParser(unittest.TestCase):
    def test_txt_parser(self):
        test_file = "test_sample.txt"
        with open(test_file, "w") as f:
            f.write("This is a test document for DocShield AI parser verification.")
        
        parsed = DocumentParser.parse_document(test_file)
        self.assertEqual(parsed["file_type"], "TXT")
        self.assertIn("DocShield", parsed["full_text"])

        if os.path.exists(test_file):
            os.remove(test_file)

if __name__ == "__main__":
    unittest.main()
