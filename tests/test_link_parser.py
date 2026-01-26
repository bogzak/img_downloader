from pathlib import Path

from img_downloader.link_parser import LinkParser


def test_parse_file(tmp_path: Path) -> None:
    p = tmp_path / "links.txt"
    p.write_text(
        "# comment\n\n"
        "https://example.com/a.jpg\n"
        "https://example.com/b.png, meta\n"
        "https://example.com/c.webp; meta\n",
        encoding="utf-8",
    )
    urls = LinkParser().parse_file(p)
    assert urls == [
        "https://example.com/a.jpg",
        "https://example.com/b.png",
        "https://example.com/c.webp",
    ]
