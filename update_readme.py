"""
README 풀이 목록 자동 갱신 스크립트

사용법 (레포 최상위 폴더에서):
    python update_readme.py

동작:
- 하위 폴더의 모든 .py 파일을 훑어서 파일 맨 위 docstring 정보를 읽는다.
- README.md의 <!-- PROBLEMS:START --> ~ <!-- PROBLEMS:END --> 사이를 표로 다시 만든다.
  (마커 바깥의 내용은 절대 건드리지 않는다.)

docstring 형식 (template.py 참고):
    [BOJ 2206] 벽 부수고 이동하기
    문제 링크: https://www.acmicpc.net/problem/2206
    난이도: 골드 3 | 유형: BFS, 상태 추가 | 풀이일: 2026-09-29
"""

import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
README = ROOT / "README.md"
START = "<!-- PROBLEMS:START -->"
END = "<!-- PROBLEMS:END -->"

SKIP_DIRS = {".git", ".github", ".idea", ".vscode", "Study", "__pycache__", "venv", ".venv"}
SKIP_FILES = {"template.py", "update_readme.py"}
PLATFORM_ORDER = ["BOJ", "SWEA", "Programmers"]  # 나머지는 이름순

DOCSTRING = re.compile(r'("""|\'\'\')(.*?)\1', re.DOTALL)
HEADER = re.compile(
    r"^\s*\[\s*(?P<platform>[^\s\]]+)\s+(?P<num>[^\]]+?)\s*\]\s*(?P<title>\S.*)$",
    re.MULTILINE,
)
URL = re.compile(r"https?://\S+")


def field(text, name):
    m = re.search(rf"{name}\s*:\s*([^|\n]*)", text)
    return m.group(1).strip() if m else ""


def parse(path):
    """풀이 파일 하나에서 정보를 뽑는다. 형식이 맞지 않으면 None."""
    try:
        source = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None

    for m in DOCSTRING.finditer(source):
        doc = m.group(2)
        h = HEADER.search(doc)
        if not h:
            continue
        if h.group("num") == "문제번호":  # 채우지 않은 템플릿
            return None
        link = URL.search(doc)
        return {
            "platform": h.group("platform"),
            "num": h.group("num"),
            "title": h.group("title").strip(),
            "url": link.group(0).rstrip(").,") if link else "",
            "level": field(doc, "난이도"),
            "tags": field(doc, "유형"),
            "date": field(doc, "풀이일"),
            "path": path.relative_to(ROOT).as_posix(),
        }
    return None


def collect():
    items, skipped = [], []
    for path in sorted(ROOT.rglob("*.py")):
        rel = path.relative_to(ROOT)
        if path.name in SKIP_FILES or any(p in SKIP_DIRS for p in rel.parts[:-1]):
            continue
        info = parse(path)
        if info:
            items.append(info)
        else:
            skipped.append(rel.as_posix())
    return items, skipped


def sort_key_num(num):
    return (0, int(num), "") if num.isdigit() else (1, 0, num)


def platform_key(name):
    if name in PLATFORM_ORDER:
        return (PLATFORM_ORDER.index(name), name)
    return (len(PLATFORM_ORDER), name)


def build(items):
    if not items:
        return "아직 등록된 풀이가 없습니다."

    groups = defaultdict(list)
    for it in items:
        groups[it["platform"]].append(it)

    lines = [f"총 **{len(items)}문제**", ""]
    for platform in sorted(groups, key=platform_key):
        rows = sorted(groups[platform], key=lambda x: sort_key_num(x["num"]))
        lines += [
            f"### {platform} ({len(rows)})",
            "",
            "| 번호 | 제목 | 난이도 | 유형 | 풀이일 |",
            "| --- | --- | --- | --- | --- |",
        ]
        for r in rows:
            num = f"[{r['num']}]({r['url']})" if r["url"] else r["num"]
            title = f"[{r['title']}]({quote(r['path'])})"
            lines.append(f"| {num} | {title} | {r['level']} | {r['tags']} | {r['date']} |")
        lines.append("")
    return "\n".join(lines).rstrip()


def main():
    items, skipped = collect()
    block = f"{START}\n{build(items)}\n{END}"

    if README.exists():
        text = README.read_text(encoding="utf-8")
    else:
        text = "# Algorithm\n\n## 풀이 목록\n\n"

    if START in text and END in text:
        pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
        text = pattern.sub(lambda _: block, text)
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
        print("README에 마커가 없어서 맨 아래에 추가했습니다.")

    README.write_text(text, encoding="utf-8")
    print(f"README 갱신 완료: {len(items)}문제")
    if skipped:
        print("형식을 읽지 못해 건너뛴 파일 (docstring 첫 줄이 '[플랫폼 번호] 제목' 형식인지 확인):")
        for s in skipped:
            print(f"  - {s}")


if __name__ == "__main__":
    main()