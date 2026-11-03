from lib.gui.simulator.simulator_renderer import PreviewRenderer
from lib.gui.simulator.simulator_panel import SimulatorPanel
from lib.exceptions import InkstitchException
from lib.i18n import _
from lib.stitch_plan import stitch_groups_to_stitch_plan
from lib.utils.threading import check_stop_flag
from lib.stitch_plan import StitchPlan

from typing import Iterator
from threading import Event

from unittest.mock import MagicMock, patch, sentinel
import pytest
import wx


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

    def on_rendered(plan: StitchPlan | None, error: BaseException | None) -> None:
        pass

    # Exercise
    renderer = PreviewRenderer(render_stitch_plan=render_plan, rendering_completed=on_rendered)
    renderer.update()

    # Verify
    assert call_after_called.wait(10), "wx.call_after was not invoked"
    call_after_mock.assert_called_once_with(on_rendered, sentinel.rendered_plan, None)


def test_no_on_render_on_cancel(call_after_called, call_after_mock):
    """ PreviewRenderer does not invoke on_rendered when cancelled. """
    render_entered = Event()
    render_done = Event()

    def render_plan() -> StitchPlan:
        render_entered.set()
        render_done.wait()
        check_stop_flag()

        return sentinel.rendered_plan

    def on_rendered(plan: StitchPlan | None, error: BaseException | None) -> None:
        pass

    # Exercise
    renderer = PreviewRenderer(render_stitch_plan=render_plan, rendering_completed=on_rendered)

    # Run an update, wait for entry
    renderer.update()
    render_entered.wait()
    # Queue another update before the stop flag is set
    renderer.update()
    # Allow the render to proceed. It should check the flag, cancel, and retry
    render_done.set()

    # Verify, should have only been called once.
    assert call_after_called.wait(10), "wx.call_after was not invoked"
    call_after_mock.assert_called_once_with(on_rendered, sentinel.rendered_plan, None)


def test_exception_reports_error_without_looping(call_after_called, call_after_mock):
    """ PreviewRenderer reports render failures on the main thread without retrying. """
    render_plan = MagicMock()
    error = InkstitchException("There is no selected stitchable element.")
    render_plan.side_effect = error

    def on_rendered(plan: StitchPlan | None, render_error: BaseException | None) -> None:
        pass

    # Exercise
    with patch('lib.gui.simulator.simulator_renderer.errormsg') as error_output:
        renderer = PreviewRenderer(render_stitch_plan=render_plan, rendering_completed=on_rendered)
        renderer.update()

        assert call_after_called.wait(10), "wx.call_after was not invoked"
        error_output.assert_called_once_with(str(error))

    # Verify - Render should have only been called once and not re-run
    render_plan.assert_called_once()
    call_after_mock.assert_called_once_with(on_rendered, None, error)


def test_render_error_clears_loading_and_shows_dialog():
    panel = MagicMock()
    error_message = _("There is no selected stitchable element. Please run "
                      "Extensions > Ink/Stitch > Troubleshoot > Troubleshoot objects in case you have expected a stitchout.")
    error = InkstitchException(error_message)

    with patch('wx.MessageBox') as message_box:
        SimulatorPanel.on_stitch_plan_rendered(panel, None, error)

    panel.dp.set_loading.assert_called_once_with(False)
    message_box.assert_called_once_with(
        error_message,
        'Simulator rendering failed',
        wx.OK | wx.ICON_ERROR
    )


def test_empty_stitch_groups_raise_user_facing_error():
    expected_error = _("There is no selected stitchable element. Please run "
                       "Extensions > Ink/Stitch > Troubleshoot > Troubleshoot objects in case you have expected a stitchout.")

    with pytest.raises(InkstitchException) as error:
        stitch_groups_to_stitch_plan([])

    assert str(error.value) == expected_error
