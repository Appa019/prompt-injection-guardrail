"""What before.py and after.py share on the command line: the run count and readable API errors."""

import argparse
from contextlib import contextmanager

import openai


def _positive_int(text):
    try:
        value = int(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"expected a whole number, got {text!r}")
    if value < 1:
        raise argparse.ArgumentTypeError("must be 1 or more")
    return value


def parse_runs(description, default=5):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("runs", nargs="?", type=_positive_int, default=default,
                        help=f"how many times to run (default: {default})")
    return parser.parse_args().runs


@contextmanager
def api_errors():
    """Turns the usual OpenAI failures into one-line messages instead of tracebacks."""
    try:
        yield
    except openai.AuthenticationError:
        raise SystemExit("OpenAI rejected the key. Check OPENAI_API_KEY in .env.")
    except openai.PermissionDeniedError as e:
        raise SystemExit(f"This key can't use the model: {e.message}")
    except openai.NotFoundError as e:
        raise SystemExit(f"{e.message}\nSet another model with OPENAI_MODEL in .env.")
    except openai.RateLimitError:
        raise SystemExit("Rate limit or no credit on the OpenAI account. Check billing or try again in a minute.")
    except openai.APIConnectionError:
        raise SystemExit("Could not reach the OpenAI API. Check your internet connection.")
