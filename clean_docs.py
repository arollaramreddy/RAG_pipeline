#!/usr/bin/env python3
"""
Clean Reddit discussion text files by removing UI boilerplate:
  - Vote buttons (Upvote/Downvote/Reply/Award/Share)
  - Standalone vote counts (bare numbers)
  - Navigation text (Sort by, Search Comments, etc.)
  - Promoted ad blocks (avatar → username → • → Promoted → ad content → Thumbnail image)
  - Avatar reference lines (u/username avatar)
  - Profile badge lines
  - Video player artifacts
  - Mass-deleted comment filler
  - r/ASU title duplicates

Kept: post title, post body, usernames, timestamps, degree info, OP marker, comment text.
"""

import re
import os


# ── exact-match lines to always discard ──────────────────────────────────────
EXACT_REMOVE = {
    'Upvote', 'Downvote', 'Reply', 'Award', 'Share',
    'Go to comments', 'Sort by:', 'Best',
    'Search Comments', 'Expand comment search', 'Comments Section',
    '•',
    'Promoted', 'Learn More', 'Shop Now', 'Order Now', 'Sign Up',
    'Collapse video player', 'Remind Me',
    # Known ASU subreddit joke flairs
    'Apostle of Steve Urkel',
    # Mass-deleted filler
    'This post was mass deleted and anonymized with Redact',
}

# ── regex patterns to discard ─────────────────────────────────────────────────
REGEX_REMOVE = [
    r'^u/.+ avatar$',               # avatar reference lines
    r'^Profile Badge for the Achievement',
    r'^Thumbnail image:',
    r'^Clickable image',
    r'^-?\d+$',                      # bare vote / comment counts (incl. negative)
    r'^Coming Up ·',                # scheduled AMA promos
    r'^\d+:\d+ / \d+:\d+$',        # video time counter (0:00 / 0:00)
    r'^•\s*Edited \d+',            # edit timestamps with leading bullet
    r'^Edited \d+',                # edit timestamps without bullet
    r'^major \'year',              # flair placeholder text
    r'^r/\w+ - .+',               # subreddit-prefixed duplicate titles
    # Redact random-word strings: 9-13 all-lowercase words, no punctuation
    r'^([a-z]+ ){8,12}[a-z]+$',
]


def is_timestamp(s: str) -> bool:
    """Reddit relative timestamp, e.g. '10mo ago', '7y ago', '4mo ago'."""
    return bool(re.match(r'^\d+[a-z]+ ago$', s.strip()))


def is_avatar_line(s: str) -> bool:
    """Lines like 'u/username avatar'."""
    return bool(re.match(r'^u/.+ avatar$', s.strip()))


def should_remove(line: str) -> bool:
    stripped = line.strip()
    if stripped in EXACT_REMOVE:
        return True
    for pat in REGEX_REMOVE:
        if re.match(pat, stripped):
            return True
    return False


def clean_content(text: str) -> str:
    lines = text.split('\n')
    result: list[str] = []
    i = 0

    while i < len(lines):
        stripped = lines[i].strip()

        # ── Detect promoted ad block ──────────────────────────────────────────
        # Pattern: avatar line → (u/name or name) → • → Promoted
        if is_avatar_line(stripped):
            j = i + 1
            # Advance past the username line (u/name or plain name)
            if j < len(lines) and (
                lines[j].strip().startswith('u/')
                or re.match(r'^[A-Za-z0-9_\-\[\]\.]+$', lines[j].strip())
            ):
                j += 1
            # Advance past the bullet
            if j < len(lines) and lines[j].strip() == '•':
                j += 1
            # If next non-empty line is "Promoted" → this is an ad block
            if j < len(lines) and lines[j].strip() == 'Promoted':
                # Skip past "Promoted"
                i = j + 1
                # Consume ad content until a reliable end marker
                while i < len(lines):
                    cur = lines[i].strip()
                    # End: thumbnail / clickable image line
                    if cur.startswith('Thumbnail image:') or cur.startswith('Clickable image'):
                        i += 1
                        # Also consume any trailing video-player artifacts
                        while i < len(lines):
                            t = lines[i].strip()
                            if (t in ('Collapse video player', 'Remind Me', '')
                                    or re.match(r'^\d+:\d+', t)
                                    or re.match(r'^Coming Up', t)):
                                i += 1
                            else:
                                break
                        break
                    # End: next comment's avatar line (real comment, not another ad)
                    elif is_avatar_line(cur):
                        break  # don't advance i; main loop handles it
                    # End: username line followed by • and then a timestamp
                    # (handles ads that end without a Thumbnail line)
                    elif (i + 1 < len(lines) and lines[i + 1].strip() == '•'):
                        k = i + 2
                        if k < len(lines) and lines[k].strip() == 'OP':
                            k += 1
                        if k < len(lines) and is_timestamp(lines[k].strip()):
                            break  # don't advance i; main loop handles it
                        else:
                            i += 1
                    else:
                        i += 1
                continue  # back to main while

            else:
                # Not an ad block — just a regular user avatar line; skip it
                i += 1
                continue

        # ── Regular boilerplate removal ───────────────────────────────────────
        if should_remove(lines[i]):
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
