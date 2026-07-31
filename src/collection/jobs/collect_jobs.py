from dataclasses import asdict, dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

from tqdm import tqdm
from pathlib import Path
import json

from src.collection.jobs.greenhouse import GreenhouseCollector
from src.collection.jobs.source_registry import JobSource, load_job_sources
from src.collection.preprocessing.html_processing import process_html_content


@dataclass
class JobPosting:
    provider: str
    source_identifier: str
    id: str
    updated_at: str
    title: str
    company: str
    location: str
    description: str
    url: str


PROVIDERS = {
    "greenhouse": GreenhouseCollector(),
}


def collect_source(source: JobSource) -> tuple[JobSource, list[dict]]:
    collector = PROVIDERS.get(source.provider)

    if collector is None:
        return source, []

    return source, collector.collect(source.identifier)

# def append_job_posting(job_posting: JobPosting, output_path: Path,) -> None:
#     with output_path.open("a", encoding="utf-8") as file:
#         if is_dataclass(job_posting):
#             job_posting = asdict(job_posting)

#         file.write(
#             json.dumps(job_posting, ensure_ascii=False)
#             + "\n"
#         )

def collect_jobs(output_path: Path):
    sources = load_job_sources()
    
    greenhouse_sources = [source for source in sources if source.provider == "greenhouse"]
    output_path.parent.mkdir(parents=True, exist_ok=True)

    sources_with_jobs = 0
    sources_without_jobs = 0

    print(f"\n{'=' * 20} Job Collection {'=' * 20}")
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [
            executor.submit(collect_source, source)
            for source in greenhouse_sources
        ]

        with output_path.open("w", encoding="utf-8") as file:
            for future in tqdm(
                as_completed(futures),
                total=len(futures),
            ):
                source, jobs = future.result()

                if jobs:
                    sources_with_jobs += 1
                else:
                    sources_without_jobs += 1
                    
                for job in jobs:
                    job_posting = JobPosting(
                                    provider=source.provider,
                                    source_identifier=source.identifier,
                                    id=str(job.get("id", "")),
                                    updated_at=job.get("updated_at", ""),
                                    title=(job.get("title") or "").strip(),
                                    company=(job.get("company") or "").strip(),
                                    location=((job.get("location") or {}).get("name") or "").strip(),
                                    description=(process_html_content(job.get("content")) or "").strip(),
                                    url=(job.get("absolute_url") or "").strip(),
                                )
                    file.write(
                        json.dumps(asdict(job_posting), ensure_ascii=False)
                        + "\n"
                    )

    print(f"Total sources: {len(greenhouse_sources)}")
    print(f"Sources with jobs: {sources_with_jobs}")
    print(f"Sources without jobs: {sources_without_jobs}")