import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ICONS = ROOT / "icons"
MANIFEST = ICONS / "manifest.json"
HTML = ROOT / "index.html"
SKILL = ROOT.parent / "SKILL.md"

# Distilled from ccrsxx/twitter-clone@62a9588 (HeroIcon + CustomIcon).
REQUIRED = (
    "AppleIcon",
    "ArchiveBoxXMarkIcon",
    "ArrowLeftIcon",
    "ArrowPathIcon",
    "ArrowPathRoundedSquareIcon",
    "ArrowRightIcon",
    "ArrowRightOnRectangleIcon",
    "ArrowUpRightIcon",
    "ArrowUpTrayIcon",
    "Bars3BottomLeftIcon",
    "BellIcon",
    "BookmarkIcon",
    "BookmarkSlashIcon",
    "CalendarDaysIcon",
    "CameraIcon",
    "ChartBarIcon",
    "ChartPieIcon",
    "ChatBubbleBottomCenterTextIcon",
    "ChatBubbleOvalLeftIcon",
    "CheckBadgeIcon",
    "CheckIcon",
    "ChevronDownIcon",
    "ChevronRightIcon",
    "Cog8ToothIcon",
    "EllipsisHorizontalCircleIcon",
    "EllipsisHorizontalIcon",
    "EnvelopeIcon",
    "ExclamationTriangleIcon",
    "FaceSmileIcon",
    "FeatherIcon",
    "GifIcon",
    "GlobeAmericasIcon",
    "GoogleIcon",
    "HashtagIcon",
    "HeartIcon",
    "HomeIcon",
    "LinkIcon",
    "MagnifyingGlassIcon",
    "MapPinIcon",
    "PaintBrushIcon",
    "PhotoIcon",
    "PinIcon",
    "PinOffIcon",
    "PlusIcon",
    "QuestionMarkCircleIcon",
    "SparklesIcon",
    "SpinnerIcon",
    "TrashIcon",
    "TriangleIcon",
    "TwitterIcon",
    "UserGroupIcon",
    "UserIcon",
    "UserMinusIcon",
    "UserPlusIcon",
    "XMarkIcon",
)

TWEET_ACTIONS = (
    "ChatBubbleOvalLeftIcon",
    "ArrowPathRoundedSquareIcon",
    "HeartIcon",
    "ArrowUpTrayIcon",
)


class DistilledIconsTest(unittest.TestCase):
    def test_manifest_lists_every_required_icon(self):
        self.assertTrue(MANIFEST.is_file(), "showcase/icons/manifest.json missing")
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(data.get("commit"), "62a9588")
        ids = [item["id"] for item in data["icons"]]
        self.assertEqual(sorted(ids), sorted(REQUIRED))

    def test_each_icon_svg_exists_and_has_a_path(self):
        missing = []
        empty = []
        for name in REQUIRED:
            path = ICONS / f"{name}.svg"
            if not path.is_file():
                missing.append(name)
                continue
            text = path.read_text(encoding="utf-8")
            if "<svg" not in text or "<path" not in text:
                empty.append(name)
        self.assertEqual(missing, [], f"missing svg: {missing}")
        self.assertEqual(empty, [], f"svg without path: {empty}")

    def test_tweet_actions_use_distilled_paths(self):
        html = HTML.read_text(encoding="utf-8")
        for name in TWEET_ACTIONS:
            svg = (ICONS / f"{name}.svg").read_text(encoding="utf-8")
            d_start = svg.split('d="', 1)[1][:24]
            self.assertIn(d_start, html, name)

    def test_skill_points_at_icon_snapshot(self):
        skill = SKILL.read_text(encoding="utf-8")
        self.assertIn("showcase/icons", skill)
        self.assertIn("62a9588", skill)


if __name__ == "__main__":
    unittest.main()
