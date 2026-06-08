#!/usr/bin/env python3
"""
Clean Reddit and Quora discussion text files by removing UI boilerplate.

Reddit boilerplate removed:
  - Vote buttons (Upvote/Downvote/Reply/Award/Share) and bare vote counts
  - Navigation text (Sort by, Search Comments, etc.)
  - Promoted ad blocks (avatar → username → • → Promoted → ad → Thumbnail image)
  - Avatar reference lines (u/username avatar), profile badge lines
  - Video player artifacts, mass-deleted comment filler, r/ASU title duplicates

Quora boilerplate removed:
  - "Profile photo for …" avatar lines
  - "Sort" navigation, answer counts ("3 Answers"), "· " separators
  - Bot timestamps ("BotJan 21"), year-only timestamps ("8y", "10y")
  - Credentials/bio lines (containing "Author has", "Upvoted by")
  - Upvoter name lines (the name that follows an "Upvoted by" line)
  - Upvoter credential lines (starting with ", " and containing degree info)
  - View/share counts ("6K viewsView upvotesView 1 share")
  - "Promoted by …" and "Sponsored by …" ad blocks and their content
  - "1 of 299 answers" style counters

Kept: question title, answer text, answerer names, timestamps, context.
"""

import re
import os


# ── exact-match lines to always discard ──────────────────────────────────────
EXACT_REMOVE = {
    # Reddit
    'Upvote', 'Downvote', 'Reply', 'Award', 'Share',
    'Go to comments', 'Sort by:', 'Best',
    'Search Comments', 'Expand comment search', 'Comments Section',
    '•',
    'Promoted', 'Learn More', 'Shop Now', 'Order Now', 'Sign Up',
    'Collapse video player', 'Remind Me',
    'Apostle of Steve Urkel',
    'This post was mass deleted and anonymized with Redact',
    # Quora
    'Sort',
    ' · ',
}

# ── regex patterns to discard ─────────────────────────────────────────────────
REGEX_REMOVE = [
    # Reddit
    r'^u/.+ avatar$',
    r'^Profile Badge for the Achievement',
    r'^Thumbnail image:',
    r'^Clickable image',
    r'^-?\d+$',
    r'^Coming Up ·',
    r'^\d+:\d+ / \d+:\d+$',
    r'^•\s*Edited \d+',
    r'^Edited \d+',
    r'^major \'year',
    r'^r/\w+ - .+',
    r'^([a-z]+ ){8,12}[a-z]+$',       # Redact random-word filler
    # Quora — avatars, nav, timestamps
    r'^Profile photo for .+',          # "Profile photo for Clint Potts"
    r'^\d+ Answers?$',                 # "3 Answers"
    r'^Bot[A-Za-z]+ \d+$',            # "BotJan 21"
    r'^\d+[y]$',                       # "8y", "10y"
    r'^\s*·\s*$',                      # bare " · " separator
    # Quora — view/vote/share counts
    r'^\d+(\.\d+)?[KkMm]? viewsView', # "6K viewsView upvotesView 1 share"
    r'^\d+ of \d+ answers?',           # "1 of 299 answers"
    # Quora — bio / credentials lines
    r'.+Author has .+ answer views',   # "researcher and writerAuthor has 28.2K…"
    r'.+Upvoted by\s*$',              # "Former Residence Hall Director…Upvoted by"
    r'^, .+(University|Institute|College|School).+',  # upvoter credential line
    r'.+Updated [A-Z][a-z]+ \d+',     # "Finance Writer…Updated May 27"
    # Quora — promoted / sponsored headers
    r'^Promoted by .+',
    r'^Sponsored by .+',
]


def is_timestamp(s: str) -> bool:
    """Reddit relative timestamp, e.g. '10mo ago', '7y ago'."""
    return bool(re.match(r'^\d+[a-z]+ ago$', s.strip()))


def is_reddit_avatar(s: str) -> bool:
    """Reddit avatar lines: 'u/username avatar'."""
    return bool(re.match(r'^u/.+ avatar$', s.strip()))


def is_quora_avatar(s: str) -> bool:
    """Quora avatar lines: 'Profile photo for …'."""
    return s.strip().startswith('Profile photo for ')


def should_remove(line: str) -> bool:
    stripped = line.strip()
    if stripped in EXACT_REMOVE:
        return True
    for pat in REGEX_REMOVE:
        if re.search(pat, stripped):
            return True
    return False


def clean_content(text: str) -> str:
    lines = text.split('\n')
    result: list[str] = []
    i = 0
    skip_next_name = False   # True after an "Upvoted by" line to drop the upvoter name

    while i < len(lines):
        stripped = lines[i].strip()

        # ── Reddit promoted ad block ──────────────────────────────────────────
        # Pattern: u/X avatar → username → • → Promoted → ad content → Thumbnail
        if is_reddit_avatar(stripped):
            j = i + 1
            if j < len(lines) and (
                lines[j].strip().startswith('u/')
                or re.match(r'^[A-Za-z0-9_\-\[\]\.]+$', lines[j].strip())
            ):
                j += 1
            if j < len(lines) and lines[j].strip() == '•':
                j += 1
            if j < len(lines) and lines[j].strip() == 'Promoted':
                i = j + 1
                while i < len(lines):
                    cur = lines[i].strip()
                    if cur.startswith('Thumbnail image:') or cur.startswith('Clickable image'):
                        i += 1
                        while i < len(lines):
                            t = lines[i].strip()
                            if (t in ('Collapse video player', 'Remind Me', '')
                                    or re.match(r'^\d+:\d+', t)
                                    or re.match(r'^Coming Up', t)):
                                i += 1
                            else:
                                break
                        break
                    elif is_reddit_avatar(cur):
                        break
                    elif i + 1 < len(lines) and lines[i + 1].strip() == '•':
                        k = i + 2
                        if k < len(lines) and lines[k].strip() == 'OP':
                            k += 1
                        if k < len(lines) and is_timestamp(lines[k].strip()):
                            break
                        else:
                            i += 1
                    else:
                        i += 1
                continue

            else:
                i += 1   # just a regular avatar line — skip it
                continue

        # ── Quora avatar lines — skip (name on next line is kept) ────────────
        if is_quora_avatar(stripped):
            i += 1
            continue

        # ── Quora Promoted/Sponsored ad block ────────────────────────────────
        # "Promoted by …" blocks contain an embedded answer with its own avatar
        # and end with a view-count line — skip everything until that line.
        # "Sponsored by …" blocks have no embedded avatar and end at the next
        # real answer's avatar line (which we leave for the main loop).
        if re.match(r'^Promoted by .+', stripped):
            i += 1
            while i < len(lines):
                cur = lines[i].strip()
                if re.match(r'^\d+(\.\d+)?[KkMm]? viewsView', cur):
                    i += 1   # skip the view-count line too
                    break
                i += 1
            continue

        if re.match(r'^Sponsored by .+', stripped):
            i += 1
            while i < len(lines):
                cur = lines[i].strip()
                if is_quora_avatar(cur):
                    break    # don't advance i; main loop handles it
                i += 1
            continue

        # ── Drop upvoter name line (line immediately after "Upvoted by") ─────
        if skip_next_name and stripped:
            skip_next_name = False
            i += 1
            continue

        # ── Regular boilerplate removal ───────────────────────────────────────
        if should_remove(lines[i]):
            # If this line contains "Upvoted by", the NEXT name line is also junk
            if 'Upvoted by' in stripped:
                skip_next_name = True
            i += 1
            continue

        result.append(lines[i])
        i += 1

    # ── Collapse runs of blank lines into a single blank ──────────────────────
    final: list[str] = []
    prev_blank = False
    for line in result:
        blank = line.strip() == ''
        if blank:
            if not prev_blank:
                final.append('')
            prev_blank = True
        else:
            final.append(line)
            prev_blank = False

    return '\n'.join(final).strip() + '\n'


def main():
    src_dir = os.path.join(
        os.path.dirname(__file__), 'documents', 'textFiles'
    )
    dst_dir = os.path.join(
        os.path.dirname(__file__), 'documents', 'cleanedTextFiles'
    )
    os.makedirs(dst_dir, exist_ok=True)

    for filename in sorted(os.listdir(src_dir)):
        if not filename.endswith('.txt'):
            continue
        src_path = os.path.join(src_dir, filename)
        dst_path = os.path.join(dst_dir, filename)

        with open(src_path, encoding='utf-8') as f:
            raw = f.read()

        cleaned = clean_content(raw)

        with open(dst_path, 'w', encoding='utf-8') as f:
            f.write(cleaned)

        raw_lines   = len(raw.splitlines())
        clean_lines = len(cleaned.splitlines())
        print(f'{filename:30s}  {raw_lines:4d} → {clean_lines:4d} lines '
              f'({100*(1 - clean_lines/raw_lines):.0f}% reduction)')


if __name__ == '__main__':
    main()
