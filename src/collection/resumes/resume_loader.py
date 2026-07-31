from dataclasses import asdict, dataclass
from pathlib import Path
import pandas as pd
import json
from tqdm import tqdm

@dataclass(frozen=True)
class Resume:
    id: str
    description: str
    html: str
    category: str

def process_resume_str(text: str):
    return ' '.join(text.split())

def load_resumes(input_path: Path, output_path: Path):
    df = pd.read_csv(input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"\n{'=' * 20} Job Collection {'=' * 20}")

    with output_path.open("w", encoding="utf-8") as file:
        for row in tqdm(df.iterrows()):
            row = row[1]

            resume = Resume(
                    id=str(row.iloc[0]) or "",
                    description=process_resume_str(row.iloc[1] or ""),
                    html=row.iloc[2] or "",
                    category=row.iloc[3] or "",
                )

            file.write(
                json.dumps(asdict(resume), ensure_ascii=False)
                + "\n"
            )
    print(f"Number of resumes: {len(df)}")