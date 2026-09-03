from lib.gui.simulator.simulator_renderer import PreviewRenderer
from lib.utils.threading import check_stop_flag
from lib.stitch_plan import StitchPlan

from typing import Iterator
from threading import Event

from unittest.mock import MagicMock, patch, sentinel
import time
import pytest


def test_check_stop_flag_on_main():
    """ Using check_stop_flag on a non-preview-renderer thread doesn't throw"""
    check_stop_flag()


# ThreadingMock is only available in 3.13+, so we'll have to set up waiting on
# this mock being called ourselves.
@pytest.fixture
def call_after_called() -> Event:
    return Event()


@pytest.fixture
def call_after_mock(call_after_called) -> Iterator[MagicMock]:
    with patch('wx.CallAfter') as call_after:
        def call_after_side_effect(self, *args, **kwargs):
            call_after_called.set()
        call_after.side_effect = call_after_side_effect

        yield call_after


def test_basic(call_after_called, call_after_mock):
    """ PreviewRenderer calls render_plan and invokes on_rendered on main thread. """
    def render_plan() -> StitchPlan:
        return sentinel.rendered_plan

    def on_rendered(plan: StitchPlan | None) -> None:
        pass

    # Exercise
    renderer = PreviewRenderer(render_plan, on_rendered)
    renderer.update()

    # Verify
    assert call_after_called.wait(10), "wx.call_after was not invoked"
    call_after_mock.assert_called_once_with(on_rendered, sentinel.rendered_plan)


def test_no_on_render_on_cancel(call_after_called, call_after_mock):
    """ PreviewRenderer does not invoke on_rendered when cancelled. """
    render_entered = Event()
    render_done = Event()

    def render_plan() -> StitchPlan:
        render_entered.set()
        render_done.wait()
        check_stop_flag()

        return sentinel.rendered_plan

    def on_rendered(plan: StitchPlan | None) -> None:
        pass

    # Exercise
    renderer = PreviewRenderer(render_plan, on_rendered)

    # Run an update, wait for entry
    renderer.update()
    render_entered.wait()
    # Queue another update before the stop flag is set
    renderer.update()
    # Allow the render to proceed. It should check the flag, cancel, and retry
    render_done.set()

    # Verify, should have only been called once.
    assert call_after_called.wait(10), "wx.call_after was not invoked"
    call_after_mock.assert_called_once_with(on_rendered, sentinel.rendered_plan)


def test_exception_does_not_loop(call_after_called, call_after_mock):
    """ PreviewRenderer does not retry when the render function throws. """
    render_plan = MagicMock()
    render_plan.side_effect = RuntimeError("Oops")

    def on_rendered(plan: StitchPlan | None) -> None:
        pass

    # Exercise
    renderer = PreviewRenderer(render_plan, on_rendered)
    renderer.update()

    # Wait a moment. Not ideal but we can't otherwise prove a negative.
    time.sleep(1)

    # Verify - Render should have only been called once and not re-run
    render_plan.assert_called_once()
    # ...and wx.call_after should never have neen invoked
    call_after_mock.assert_not_called()
