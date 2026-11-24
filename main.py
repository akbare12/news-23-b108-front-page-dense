#!/usr/bin/env python3
"""news-23 b108 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import hashlib
import os
import struct
import sys
import zlib

SRC_NAME = "entry.png"
MIN_BYTES = 10_000
MAX_BYTES = 1_048_576


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    return 1


def parse_png(data):
    """Validate a PNG byte string; return (width, height) or raise ValueError."""
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("bad PNG signature")
    # first chunk: length at offset 8, type at 12, IHDR data at 16..29, CRC at 29..33.
    # Offsets are +8 from the file start because the 8-byte PNG signature comes first.
    if len(data) < 33:
        raise ValueError("file too short for IHDR")
    length = struct.unpack(">I", data[8:12])[0]
    ctype = data[12:16]
    if ctype != b"IHDR" or length != 13:
        raise ValueError("first chunk is not a 13-byte IHDR")
    ihdr = data[16:29]
    crc_stored = struct.unpack(">I", data[29:33])[0]
    if zlib.crc32(b"IHDR" + ihdr) & 0xFFFFFFFF != crc_stored:
        raise ValueError("IHDR CRC mismatch")
    width, height, depth, ctype_b, comp, filt, inter = struct.unpack(">IIBBBBB", ihdr)
    if (width, height) != (1024, 1024):
        raise ValueError("expected 1024x1024, got %dx%d" % (width, height))
    if depth != 8 or ctype_b not in (2, 6):
        raise ValueError("expected 8-bit RGB/RGBA")
    if comp != 0 or filt != 0 or inter != 0:
        raise ValueError("unexpected compression/filter/interlace")
    # chunk walk: verify CRC of every chunk, require non-empty IDAT payload,
    # require IEND (0-byte) as the final chunk with no trailing data.
    off = 33
    idat_total = 0
    seen_iend = False
    while off + 8 <= len(data):
        ln = struct.unpack(">I", data[off:off + 4])[0]
        typ = data[off + 4:off + 8]
        end = off + 8 + ln + 4
        if end > len(data):
            raise ValueError("truncated chunk %r" % typ)
        crc_stored = struct.unpack(">I", data[off + 8 + ln:off + 8 + ln + 4])[0]
        if zlib.crc32(typ + data[off + 8:off + 8 + ln]) & 0xFFFFFFFF != crc_stored:
            raise ValueError("CRC mismatch in chunk %r" % typ)
        if typ == b"IDAT":
            if ln == 0:
                raise ValueError("empty IDAT chunk")
            idat_total += ln
        if typ == b"IEND":
            if ln != 0:
                raise ValueError("IEND must be 0 bytes")
            if end != len(data):
                raise ValueError("trailing data after IEND")
            seen_iend = True
            break
        off = end
    if not seen_iend:
        raise ValueError("missing IEND")
    if idat_total < 1000:
        raise ValueError("IDAT payload too small")
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SRC_NAME)
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not outdir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    outdir_abs = os.path.abspath(outdir)
    if os.path.isfile(outdir_abs):
        return fail("MAKEFUN_OUTPUT_DIR is a file: %s" % outdir)
    # refuse to write inside the repo (grader runs from a read-only copy)
    if outdir_abs == here or outdir_abs.startswith(here + os.sep):
        return fail("MAKEFUN_OUTPUT_DIR must be outside the repo: %s" % outdir)
    if not os.path.isfile(src):
        return fail("source not found: %s" % src)
    with open(src, "rb") as f:
        data = f.read()
    if len(data) < MIN_BYTES:
        return fail("source too small: %d bytes" % len(data))
    if len(data) > MAX_BYTES:
        return fail("source over 1 MiB: %d bytes" % len(data))
    try:
        w, h = parse_png(data)
    except ValueError as e:
        return fail("invalid PNG: %s" % e)
    os.makedirs(outdir_abs, exist_ok=True)
    dst = os.path.join(outdir_abs, SRC_NAME)
    if os.path.abspath(dst) == os.path.abspath(src):
        return fail("output would overwrite the source")
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        back = f.read()
    if back != data:
        return fail("output differs from source after write")
    print("wrote %s (%dx%d, %d bytes, sha256 %s)"
          % (dst, w, h, len(data), hashlib.sha256(data).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
