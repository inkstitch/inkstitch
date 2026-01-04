# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

"""Video exporter for embroidery simulation."""

import os
import shutil
import subprocess
import tempfile

import wx

# Check if PIL is available
try:
    from PIL import Image

    HAS_PIL = True
except ImportError:
    HAS_PIL = False


def check_ffmpeg():
    """Check if FFmpeg is available on the system."""
    return shutil.which("ffmpeg") is not None


def capture_frame(
    drawing_panel, stitch_index, width, height, background_color, transparent=False, show_crosshair=False, show_needle_points=False, padding=20
):
    """Capture a single frame at the specified stitch index.

    Args:
        drawing_panel: The DrawingPanel instance
        stitch_index: Which stitch to render up to
        width: Output width in pixels
        height: Output height in pixels
        background_color: Background color for the frame
        transparent: If True, use transparent background (for PNG)
        show_crosshair: If True, draw crosshair at the current stitch position
        show_needle_points: If True, draw needle penetration points
        padding: Padding around the design in pixels (default 20)

    Returns:
        wx.Bitmap of the rendered frame
    """
    # Create a bitmap to render to (use 32-bit depth for alpha if transparent)
    if transparent:
        bitmap = wx.Bitmap(width, height, 32)
        bitmap.UseAlpha()
    else:
        bitmap = wx.Bitmap(width, height)
    memory_dc = wx.MemoryDC(bitmap)

    # Clear with background color or transparent
    if transparent:
        memory_dc.SetBackground(wx.Brush(wx.Colour(0, 0, 0, 0)))
    elif background_color:
        memory_dc.SetBackground(wx.Brush(background_color))
    else:
        memory_dc.SetBackground(wx.Brush(wx.WHITE))
    memory_dc.Clear()

    # Create graphics context for anti-aliased rendering
    gc = wx.GraphicsContext.Create(memory_dc)

    if gc is None:
        memory_dc.SelectObject(wx.NullBitmap)
        return bitmap

    # Calculate scale to fit design in output size
    design_width = drawing_panel.width
    design_height = drawing_panel.height

    if design_width > 0 and design_height > 0:
        # Calculate available space with user-specified padding
        available_width = width - 2 * padding
        available_height = height - 2 * padding

        scale_x = available_width / design_width
        scale_y = available_height / design_height
        scale = min(scale_x, scale_y)

        # Center the design
        offset_x = (width - design_width * scale) / 2
        offset_y = (height - design_height * scale) / 2

        # Apply transform
        transform = gc.GetTransform()
        transform.Translate(offset_x, offset_y)
        transform.Scale(scale / drawing_panel.PIXEL_DENSITY, scale / drawing_panel.PIXEL_DENSITY)
        gc.SetTransform(transform)

        # Draw the stitches up to the current stitch index
        _draw_stitches_to_gc(gc, drawing_panel, stitch_index, transform, show_crosshair, show_needle_points)

    memory_dc.SelectObject(wx.NullBitmap)
    return bitmap


def _draw_stitches_to_gc(gc, drawing_panel, max_stitch, transform=None, show_crosshair=False, show_needle_points=False):
    """Draw stitches to a graphics context up to the specified stitch index.

    Args:
        gc: Graphics context to draw on
        drawing_panel: DrawingPanel instance with stitch data
        max_stitch: Maximum stitch index to draw up to
        transform: Transform matrix for coordinate conversion (for crosshair)
        show_crosshair: If True, draw crosshair at the last stitch position
        show_needle_points: If True, draw needle penetration points
    """
    gc.BeginLayer(1)

    stitch = 0
    last_stitch = None
    last_pen = None

    for pen, stitches, _jumps in zip(drawing_panel.pens, drawing_panel.stitch_blocks, drawing_panel.jumps):
        gc.SetPen(pen)
        if stitch + len(stitches) < max_stitch:
            stitch += len(stitches)
            if len(stitches) > 1:
                gc.StrokeLines(stitches)
                # Draw needle penetration points if enabled
                if show_needle_points:
                    _draw_needle_points(gc, pen, stitches, drawing_panel.PIXEL_DENSITY)
                last_stitch = stitches[-1]
                last_pen = pen
        else:
            partial_stitches = stitches[: int(max_stitch) - stitch]
            if len(partial_stitches) > 1:
                gc.StrokeLines(partial_stitches)
                # Draw needle penetration points if enabled
                if show_needle_points:
                    _draw_needle_points(gc, pen, partial_stitches, drawing_panel.PIXEL_DENSITY)
                last_stitch = partial_stitches[-1]
                last_pen = pen
            break

    # Draw crosshair at the last stitch position
    if show_crosshair and last_stitch is not None and transform is not None:
        _draw_crosshair(gc, last_stitch[0], last_stitch[1], transform, drawing_panel.PIXEL_DENSITY)

    gc.EndLayer()


def _draw_needle_points(gc, pen, stitches, pixel_density):
    """Draw needle penetration points for the given stitches."""
    from ...svg import PIXELS_PER_MM
    from ...utils.settings import global_settings

    npp_size = global_settings.get("simulator_npp_size", 0.3) * PIXELS_PER_MM * pixel_density
    npp_pen = wx.Pen(pen.GetColour(), width=int(npp_size))
    gc.SetPen(npp_pen)
    gc.StrokeLineSegments(stitches, [(s[0] + 0.001, s[1]) for s in stitches])
    gc.SetPen(pen)  # Restore original pen


def _draw_crosshair(gc, x, y, transform, pixel_density):
    """Draw a crosshair at the specified position."""
    # Transform the coordinates to screen space
    tx, ty = transform.TransformPoint(float(x), float(y))

    # Reset transform for drawing crosshair in screen space
    gc.SetTransform(gc.CreateMatrix())

    crosshair_radius = 10
    black_pen = wx.Pen(wx.Colour(128, 128, 128), width=1)
    gc.SetPen(black_pen)
    gc.StrokeLines(((tx - crosshair_radius, ty), (tx + crosshair_radius, ty)))
    gc.StrokeLines(((tx, ty - crosshair_radius), (tx, ty + crosshair_radius)))


def bitmap_to_pil_image(bitmap):
    """Convert a wx.Bitmap to a PIL Image."""
    if not HAS_PIL:
        raise ImportError("PIL/Pillow is required for image conversion")

    width = bitmap.GetWidth()
    height = bitmap.GetHeight()

    # Convert bitmap to wx.Image
    image = bitmap.ConvertToImage()

    # Get raw RGB data
    data = image.GetData()

    # Check if image has alpha channel
    if image.HasAlpha():
        # Get alpha data
        alpha_data = image.GetAlpha()

        # Create PIL RGBA image by combining RGB and Alpha
        rgb_image = Image.frombytes("RGB", (width, height), bytes(data))
        alpha_image = Image.frombytes("L", (width, height), bytes(alpha_data))
        pil_image = rgb_image.copy()
        pil_image.putalpha(alpha_image)
    else:
        # Create PIL image from raw RGB data
        pil_image = Image.frombytes("RGB", (width, height), bytes(data))

    return pil_image


def export_video(
    drawing_panel,
    output_path,
    from_stitch,
    to_stitch,
    speed,
    fps,
    width,
    height,
    background_color,
    progress_callback=None,
    show_crosshair=False,
    show_needle_points=False,
    padding=20,
):
    """Export the simulation as a video file.

    Args:
        drawing_panel: The DrawingPanel instance
        output_path: Path to save the video file
        from_stitch: Starting stitch number (1-indexed)
        to_stitch: Ending stitch number (1-indexed)
        speed: Stitches per second
        fps: Frames per second for the output video
        width: Output width in pixels
        height: Output height in pixels
        background_color: Background color
        progress_callback: Optional callback(current, total, status) for progress updates
                          status is optional string for status text
        show_crosshair: If True, draw crosshair at current stitch position
        show_needle_points: If True, draw needle penetration points
        padding: Padding around the design in pixels
    """
    # Calculate stitch range
    num_stitches = max(1, to_stitch - from_stitch + 1)

    # Calculate total frames needed
    duration_seconds = num_stitches / speed
    total_frames = int(duration_seconds * fps)

    if total_frames < 1:
        total_frames = 1

    # Stitches per frame
    stitches_per_frame = num_stitches / total_frames

    # Export as GIF (only format available without external dependencies)
    _export_as_gif(
        drawing_panel,
        output_path,
        from_stitch,
        to_stitch,
        total_frames,
        stitches_per_frame,
        fps,
        width,
        height,
        background_color,
        progress_callback,
        show_crosshair,
        show_needle_points,
        padding,
    )


def _export_as_gif(
    drawing_panel,
    output_path,
    from_stitch,
    to_stitch,
    total_frames,
    stitches_per_frame,
    fps,
    width,
    height,
    background_color,
    progress_callback,
    show_crosshair=False,
    show_needle_points=False,
    padding=20,
):
    """Export as animated GIF using PIL."""
    if not HAS_PIL:
        raise ImportError("PIL/Pillow is required for GIF export. Please install it with: pip install Pillow")

    frames = []
    num_stitches = to_stitch - from_stitch + 1

    for frame_idx in range(total_frames):
        # Calculate stitch index relative to from_stitch
        stitch_offset = min(int((frame_idx + 1) * stitches_per_frame), num_stitches)
        stitch_index = from_stitch + stitch_offset - 1

        # Capture frame with display options
        bitmap = _capture_frame_sync(drawing_panel, stitch_index, width, height, background_color, show_crosshair, show_needle_points, padding)

        # Convert to PIL
        pil_image = bitmap_to_pil_image(bitmap)
        frames.append(pil_image)

        if progress_callback:
            # 0-50% for frame capture
            capture_progress = int((frame_idx + 1) / total_frames * 50)
            progress_callback(capture_progress, 100, "capturing", frame_idx + 1, total_frames)

    # Save as GIF - show encoding status (50-100%)
    if progress_callback:
        progress_callback(50, 100, "encoding", 0, 0)

    if frames:
        frame_duration = int(1000 / fps)  # Duration per frame in milliseconds
        frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=frame_duration, loop=0, optimize=False)

    if progress_callback:
        progress_callback(100, 100, "complete", 0, 0)


def _capture_frame_sync(drawing_panel, stitch_index, width, height, background_color, show_crosshair=False, show_needle_points=False, padding=20):
    """Synchronously capture a frame (must be called from main thread)."""
    return capture_frame(drawing_panel, stitch_index, width, height, background_color, False, show_crosshair, show_needle_points, padding)


def _export_with_ffmpeg(
    drawing_panel, output_path, num_stitches, total_frames, stitches_per_frame, fps, width, height, background_color, progress_callback
):
    """Export as MP4 using FFmpeg."""
    if not check_ffmpeg():
        raise RuntimeError("FFmpeg is not available. Please install FFmpeg or use GIF format.")

    # Create temporary directory for frames
    temp_dir = tempfile.mkdtemp(prefix="inkstitch_video_")

    try:
        # Capture all frames (0-50% progress)
        for frame_idx in range(total_frames):
            stitch_index = min(int((frame_idx + 1) * stitches_per_frame), num_stitches)

            bitmap = _capture_frame_sync(drawing_panel, stitch_index, width, height, background_color)
            pil_image = bitmap_to_pil_image(bitmap)

            frame_path = os.path.join(temp_dir, f"frame_{frame_idx:06d}.png")
            pil_image.save(frame_path, "PNG")

            if progress_callback:
                capture_progress = int((frame_idx + 1) / total_frames * 50)
                progress_callback(capture_progress, 100, "capturing", frame_idx + 1, total_frames)

        # Show encoding status (50-100%)
        if progress_callback:
            progress_callback(50, 100, "encoding", 0, 0)

        # Run FFmpeg to encode video
        ffmpeg_cmd = [
            "ffmpeg",
            "-y",  # Overwrite output file
            "-framerate",
            str(fps),
            "-i",
            os.path.join(temp_dir, "frame_%06d.png"),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-crf",
            "23",  # Quality (lower = better, 18-28 is reasonable)
            output_path,
        ]

        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, check=False)

        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg failed: {result.stderr}")

        if progress_callback:
            progress_callback(100, 100, "complete", 0, 0)

    finally:
        # Clean up temporary files
        shutil.rmtree(temp_dir, ignore_errors=True)
