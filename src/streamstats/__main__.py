import argparse
import sys
from itertools import chain
from pathlib import Path

from .analysis import analyze_events
from .errors import CLIConfigError, UnsupportedFormatError
from .parsers import get_parser
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
        sys.exit(2)

    try:
        run_analysis(args)
    except (CLIConfigError, UnsupportedFormatError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:  # noqa: BLE001
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(2)


def run_analysis(args):
    """Запускает анализ файлов."""
    all_events = []

    for input_path in args.inputs:
        path = Path(input_path)
        if not path.exists():
            raise CLIConfigError(f"File not found: {input_path}")

        parser_func = get_parser(args.format)
        events = parser_func(path, skip_invalid=args.skip_invalid)
        all_events.append(events)

    combined_events = chain.from_iterable(all_events)
    stats = analyze_events(combined_events)

    generate_report(stats, Path(args.output))
    print(f"Report saved to {args.output}")


if __name__ == "__main__":
    main()