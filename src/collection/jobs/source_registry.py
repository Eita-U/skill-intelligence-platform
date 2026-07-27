from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class JobSource:
    provider: str
    identifier: str


def load_job_sources() -> list[JobSource]:
    paths = Path("config").glob("*.json")
    sources = set()
    for path in paths:
        provider = Path(path).stem
        with Path(path).open("r", encoding="utf-8") as file:
            rows = json.load(file)

        sources.update(JobSource(provider=provider, identifier=row.lower().strip()) for row in rows if row.strip())

    return sorted(
        sources,
        key=lambda source: (source.provider, source.identifier),
    )