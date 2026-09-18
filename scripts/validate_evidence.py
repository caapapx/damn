#!/usr/bin/env python3
"""Validate a DAMN EvidencePacket without network access."""

import json
import sys
from pathlib import Path
from urllib.parse import urlparse, urlunparse


def canonical_url(value: str) -> str:
    parsed = urlparse(value)
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), parsed.path.rstrip("/"), "", parsed.query, ""))


def validate(packet: dict) -> list[str]:
    errors = []
    required = ("packet_id", "task_id", "completion_status", "claims", "sources", "gaps", "budget_used")
    for key in required:
        if key not in packet:
            errors.append(f"missing packet field: {key}")
    source_ids = set()
    for source in packet.get("sources", []):
        for key in ("source_id", "provider", "canonical_url", "retrieved_at", "locator"):
            if not source.get(key):
                errors.append(f"source missing {key}: {source.get('source_id', '<unknown>')}")
        source_id = source.get("source_id")
        if source_id in source_ids:
            errors.append(f"duplicate source_id: {source_id}")
        source_ids.add(source_id)
        url = source.get("canonical_url", "")
        if url and canonical_url(url) != url:
            errors.append(f"non-canonical URL: {url}")
    for claim in packet.get("claims", []):
        for key in ("claim_id", "text", "source_ids", "verification_status"):
            if key not in claim:
                errors.append(f"claim missing {key}: {claim.get('claim_id', '<unknown>')}")
        for source_id in claim.get("source_ids", []):
            if source_id not in source_ids:
                errors.append(f"claim references unknown source: {source_id}")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_evidence.py PACKET.json", file=sys.stderr)
        return 2
    packet = json.loads(Path(sys.argv[1]).read_text())
    errors = validate(packet)
    if errors:
        print(json.dumps({"valid": False, "errors": errors}, ensure_ascii=False))
        return 1
    print(json.dumps({"valid": True, "packet_id": packet["packet_id"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
