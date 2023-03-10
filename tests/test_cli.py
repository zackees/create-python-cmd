"""
Unit test file.
"""
import unittest
import os


class MainTester(unittest.TestCase):
    """Main tester class."""

    def test_imports(self) -> None:
        """Test command line interface (CLI)."""
        rtn = os.system("createpythoncmd --help")
        self.assertEqual(0, rtn)


if __name__ == "__main__":
    unittest.main()
