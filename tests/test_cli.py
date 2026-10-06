import argparse

import pytest

from ascii_3d_cube.cli import build_parser, positive_float, positive_int


def test_parser_accepts_render_options():
    args = build_parser().parse_args(
        ["--width", "100", "--height", "36", "--fps", "60", "--no-color"]
    )

    assert args.width == 100
    assert args.height == 36
    assert args.fps == 60
    assert args.no_color is True


@pytest.mark.parametrize("value", ["0", "-1"])
def test_positive_int_rejects_non_positive_values(value):
    with pytest.raises(argparse.ArgumentTypeError):
        positive_int(value)


@pytest.mark.parametrize("value", ["0", "-0.1"])
def test_positive_float_rejects_non_positive_values(value):
    with pytest.raises(argparse.ArgumentTypeError):
        positive_float(value)
