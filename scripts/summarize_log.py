import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG = ROOT / "build.log"
DEFAULT_PROMPT = ROOT / "build_prompt.md"
DEFAULT_SUMMARY = ROOT / "build_summary.md"


def read_build_log(log_path):
    try:
        data = log_path.read_bytes()
    except FileNotFoundError as exc:
        raise SystemExit(f"Build log not found: {log_path}") from exc
    except OSError as exc:
        raise SystemExit(f"Could not read build log: {log_path}: {exc}") from exc

    if data.startswith((b"\xff\xfe", b"\xfe\xff")):
        return data.decode("utf-16", errors="replace")
    return data.decode("utf-8-sig", errors="replace")


def extract_important_lines(build_log):
    lines = build_log.splitlines()
    relevant = []
    failure_marker = re.compile(
        r"(?:^FAILED\s|^ERROR\s|^E\s+|short test summary|traceback|"
        r"[A-Za-z_][\w.-]*Error:|AssertionError|"
        r"\b[A-Za-z_./-]+\.py:\d+:)"
    )
    result_marker = re.compile(
        r"\b\d+\s+(?:failed|passed|errors?|skipped)(?:,|\s|$)"
    )

    for line in lines:
        if failure_marker.search(line, re.IGNORECASE):
            cleaned = line.rstrip()
            if cleaned not in relevant:
                relevant.append(cleaned)

    if not relevant:
        relevant = [
            line.rstrip()
            for line in lines[-80:]
            if result_marker.search(line.strip())
        ]

    return "\n".join(relevant[-120:])


def build_prompt(build_log, important_log):
    return f"""# Python pytest build failure analysis

Analyze the pytest build log below and give a beginner-friendly diagnosis.

Return exactly these three sections:

## Root cause
Explain why the build failed and identify the relevant exception or assertion mismatch.

## Failing test or file
Name the failing pytest test and source or test file when they are present in the log.

## Suggested solution
Give concrete code or test changes that would fix or diagnose the failure. Keep suggestions consistent with the repository code.

Do not claim that you ran tests. Do not invent log details that are not present.

## Repository
- Project: Python pricing service
- Source module: `src/pricing.py`
- Tests: `tests/test_pricing.py`

## Extracted build information
```text
{important_log}
```

## Full build log
```text
{build_log[-12000:].strip()}
```
"""


def save_copilot_summary(summary_output, summary_file):
    if summary_file is None:
        return

    try:
        summary = summary_file.read_text(encoding="utf-8", errors="replace")
        summary_output.write_text(summary.strip() + "\n", encoding="utf-8")
    except OSError as exc:
        raise SystemExit(f"Could not save summary: {exc}") from exc


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract pytest errors and prepare an LLM build-failure prompt."
    )
    parser.add_argument(
        "log",
        nargs="?",
        type=Path,
        default=DEFAULT_LOG,
        help="pytest build log (default: build.log)",
    )
    parser.add_argument(
        "--prompt-output",
        type=Path,
        default=DEFAULT_PROMPT,
        help="Markdown file that receives the Copilot prompt",
    )
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=DEFAULT_SUMMARY,
        help="Markdown file that receives the Copilot summary",
    )
    parser.add_argument(
        "--summary-file",
        type=Path,
        help="Optional file containing pasted Copilot Chat output",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    log_path = args.log if args.log.is_absolute() else ROOT / args.log
    prompt_output = (
        args.prompt_output
        if args.prompt_output.is_absolute()
        else ROOT / args.prompt_output
    )
    summary_output = (
        args.summary_output
        if args.summary_output.is_absolute()
        else ROOT / args.summary_output
    )
    summary_file = (
        args.summary_file
        if args.summary_file is None or args.summary_file.is_absolute()
        else ROOT / args.summary_file
    )

    build_log = read_build_log(log_path)
    important_log = extract_important_lines(build_log)
    prompt = build_prompt(build_log, important_log)

    try:
        prompt_output.write_text(prompt, encoding="utf-8")
        save_copilot_summary(summary_output, summary_file)
    except OSError as exc:
        raise SystemExit(f"Could not write output file: {exc}") from exc

    print(prompt_output)
    if summary_file is not None:
        print(summary_output)


if __name__ == "__main__":
    main()