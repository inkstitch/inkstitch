import wx
import moderngl

# Only used to get the texture path here.
import pathlib
basedir = pathlib.Path(__file__).parent

def load_texture(ctx: moderngl.Context) -> moderngl.Texture:
    img = wx.Image()

    with open(basedir / "texture/normals-new.png", "rb") as f:
        pnghandler = wx.PNGHandler()
        pnghandler.LoadFile(img, f)

    # wx loads the image into RGB and A, so we need to "interlace" them into RGBA ourselves
    buf = img.GetDataBuffer()
    abuf = img.GetAlphaBuffer()

    px_count = img.GetWidth() * img.GetHeight()
    texbuf = bytearray(px_count * 4)
    for i in range(px_count):
        texbuf[i*4+0] = buf[i*3+0]
        texbuf[i*4+1] = buf[i*3+1]
        texbuf[i*4+2] = buf[i*3+2]
        texbuf[i*4+3] = abuf[i]

    return ctx.texture((img.GetWidth(), img.GetHeight()), 4, texbuf)