from pathlib import Path
from typing import List, Dict
import pandas as pd


def load_ground_truth(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    return pd.read_csv(path)


def list_input_files(input_dir: str | Path, extensions: tuple = (".png", ".jpg", ".pdf")) -> List[Path]:
    input_dir = Path(input_dir)
    files: List[Path] = []
    for ext in extensions:
        files.extend(input_dir.rglob(f"*{ext}"))
    return sorted(files)


def align_inputs_with_ground_truth(
    inputs: List[Path],
    ground_truth: pd.DataFrame,
    input_col: str = "filename",
) -> List[Dict]:
    gt_index = {row[input_col]: row for _, row in ground_truth.iterrows()}
    aligned: List[Dict] = []

    for p in inputs:
        key = p.name
        if key not in gt_index:
            continue
        row = gt_index[key]
        aligned.append(
            {
                "path": p,
                "ground_truth": row.to_dict(),
            }
        )
    return aligned
