import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = (ROOT / "tokens.css").read_text(encoding="utf-8")


def decl(name: str) -> str:
    match = re.search(rf"{re.escape(name)}:\s*([^;]+);", CSS)
    if not match:
        raise AssertionError(f"missing {name}")
    return re.sub(r"\s+", " ", match.group(1).strip())


class TokenContractTest(unittest.TestCase):
    def test_raw_background_triplets(self):
        self.assertEqual(decl("--dark-background"), "0 0 0")
        self.assertEqual(decl("--dim-background"), "22 33 44")
        self.assertEqual(decl("--light-background"), "255 255 255")
        self.assertEqual(decl("--dark-search-background"), "32 35 39")
        self.assertEqual(decl("--dim-search-background"), "39 51 64")
        self.assertEqual(decl("--light-search-background"), "239 243 244")
        self.assertEqual(decl("--dark-sidebar-background"), "22 24 28")
        self.assertEqual(decl("--dim-sidebar-background"), "30 39 50")
        self.assertEqual(decl("--light-sidebar-background"), "247 249 249")

    def test_fixed_accent_triplets(self):
        self.assertEqual(decl("--accent-blue"), "29 155 240")
        self.assertEqual(decl("--accent-yellow"), "255 213 0")
        self.assertEqual(decl("--accent-pink"), "249 26 130")
        self.assertEqual(decl("--accent-purple"), "120 87 255")
        self.assertEqual(decl("--accent-orange"), "255 122 0")
        self.assertEqual(decl("--accent-green"), "0 184 122")
        self.assertEqual(decl("--accent-red"), "244 33 46")

    def test_hex_only_tokens(self):
        self.assertEqual(decl("--twitter-icon"), "#D6D9DB")
        self.assertEqual(decl("--image-preview-hover"), "#272C30")

    def test_radius_tokens(self):
        self.assertEqual(decl("--radius-full"), "9999px")
        self.assertEqual(decl("--radius-2xl"), "16px")
        self.assertEqual(decl("--radius-md"), "6px")

    def test_default_semantic_on_root(self):
        self.assertIn('data-theme="lights-out"', CSS)
        self.assertEqual(decl("--main-accent"), "var(--accent-blue)")


if __name__ == "__main__":
    unittest.main()
