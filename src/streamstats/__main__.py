import argparse
import logging
import sys
from pathlib import Path

from .analysis import analyze_events
from .errors import CLIConfigError, UnsupportedFormatError
from .parsers import parse_csv, parse_jsonl
from .report import generate_report


def main():
    parser = argparse.ArgumentParser(description="Потоковый анализатор файлов")
    subparsers = parser.add_subparsers(dest="command")

    analyze_parser = subparsers.add_parser("analyze")
    analyze_parser.add_argument("inputs", nargs="+", help="Входные файлы")
    analyze_parser.add_argument("--format", required=True, choices=["csv", "jsonl"])
    analyze_parser.add_argument("--output", required=True)
    analyze_parser.add_argument("--skip-invalid", action="store_true")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "analyze":
        run_analysis(args)


def run_analysis(args):
    """Запускает анализ файлов."""
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")

    all_events = []

    for input_path in args.inputs:
        path = Path(input_path)
        if not path.exists():
            raise CLIConfigError(f"File not found: {input_path}")

        if args.format == "csv":
            events = parse_csv(path, skip_invalid=args.skip_invalid)
        elif args.format == "jsonl":
            events = parse_jsonl(path, skip_invalid=args.skip_invalid)
        else:
            raise UnsupportedFormatError(f"Unsupported format: {args.format}")

        all_events.append(events)

    from itertools import chain
    combined_events = chain.from_iterable(all_events)

    stats = analyze_events(combined_events)

    generate_report(stats, Path(args.output))
    print(f"Report saved to {args.output}")


if __name__ == "__main__":
    main()