from copy import deepcopy

import pytest

from ggshield.output import TextOutputHandler
from ggshield.scan import Result
from ggshield.scan.scannable import ScanCollection
from ggshield.utils import Filemode
from tests.conftest import (
    _MULTI_SECRET_ONE_LINE_PATCH,
    _MULTI_SECRET_ONE_LINE_PATCH_OVERLAY,
    _MULTI_SECRET_ONE_LINE_PATCH_OVERLAY_SCAN_RESULT,
    _MULTI_SECRET_ONE_LINE_PATCH_SCAN_RESULT,
    _MULTI_SECRET_TWO_LINES_PATCH,
    _MULTI_SECRET_TWO_LINES_PATCH_SCAN_RESULT,
    _ONE_LINE_AND_MULTILINE_PATCH_CONTENT,
    _ONE_LINE_AND_MULTILINE_PATCH_SCAN_RESULT,
    _SIMPLE_SECRET_MULTILINE_PATCH,
    _SIMPLE_SECRET_MULTILINE_PATCH_SCAN_RESULT,
    _SIMPLE_SECRET_PATCH,
    _SIMPLE_SECRET_PATCH_SCAN_RESULT,
    skipwindows,
)


@skipwindows
@pytest.mark.parametrize(
    "show_secrets",
    [pytest.param(True, id="show_secrets"), pytest.param(False, id="hide_secrets")],
)
@pytest.mark.parametrize(
    "verbose",
    [pytest.param(True, id="verbose"), pytest.param(False, id="clip_long_lines")],
)
@pytest.mark.parametrize(
    "result_input",
    [
        pytest.param(
            Result(
                content=_SIMPLE_SECRET_PATCH,
                filename="leak.txt",
                filemode=Filemode.NEW,
                scan=_SIMPLE_SECRET_PATCH_SCAN_RESULT,
            ),
            id="_SIMPLE_SECRET_PATCH_SCAN_RESULT",
        ),
        pytest.param(
            Result(
                content=_MULTI_SECRET_ONE_LINE_PATCH,
                filename="leak.txt",
                filemode=Filemode.NEW,
                scan=_MULTI_SECRET_ONE_LINE_PATCH_SCAN_RESULT,
            ),
            id="_MULTI_SECRET_ONE_LINE_PATCH_SCAN_RESULT",
        ),
        pytest.param(
            Result(
                content=_MULTI_SECRET_ONE_LINE_PATCH_OVERLAY,
                filename="leak.txt",
                filemode=Filemode.NEW,
                scan=_MULTI_SECRET_ONE_LINE_PATCH_OVERLAY_SCAN_RESULT,
            ),
            id="_MULTI_SECRET_ONE_LINE_PATCH_OVERLAY_SCAN_RESULT",
        ),
        pytest.param(
            Result(
                content=_MULTI_SECRET_TWO_LINES_PATCH,
                filename="leak.txt",
                filemode=Filemode.NEW,
                scan=_MULTI_SECRET_TWO_LINES_PATCH_SCAN_RESULT,
            ),
            id="_MULTI_SECRET_TWO_LINES_PATCH_SCAN_RESULT",
        ),
        pytest.param(
            Result(
                content=_SIMPLE_SECRET_MULTILINE_PATCH,
                filename="leak.txt",
                filemode=Filemode.NEW,
                scan=_SIMPLE_SECRET_MULTILINE_PATCH_SCAN_RESULT,
            ),
            id="_SIMPLE_SECRET_MULTILINE_PATCH_SCAN_RESULT",
        ),
        pytest.param(
            Result(
                content=_ONE_LINE_AND_MULTILINE_PATCH_CONTENT,
                filename="leak.txt",
                filemode=Filemode.NEW,
                scan=_ONE_LINE_AND_MULTILINE_PATCH_SCAN_RESULT,
            ),
            id="_ONE_LINE_AND_MULTILINE_PATCH_CONTENT",
        ),
    ],
)
def test_leak_message(result_input, snapshot, show_secrets, verbose):
    output_handler = TextOutputHandler(show_secrets=show_secrets, verbose=verbose)
    new_result = deepcopy(result_input)
    output = output_handler._process_scan_impl(
        ScanCollection(
            id="scan",
            type="test",
            results=[new_result],
            optional_header="> This is an example header",
        )
    )

    snapshot.assert_match(output)
