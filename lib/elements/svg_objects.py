def rect_to_path(node):
    x = float(node.get('x', '0'))
    y = float(node.get('y', '0'))
    width = float(node.get('width', '0'))
    height = float(node.get('height', '0'))
    rx = None
    ry = None

    # rounded corners
    # the following rules apply for radius calculations:
    #   if rx or ry is missing it has to take the value of the other one
    #   the radius cannot be bigger than half of the corresponding side
    #   (otherwise we receive an invalid path)
    if node.get('rx') or node.get('ry'):
        if node.get('rx'):
            rx = float(node.get('rx', '0'))
            ry = rx
        if node.get('ry'):
            ry = float(node.get('ry', '0'))
            if not ry:
                ry = rx

        rx = min(width/2, rx)
        ry = min(height/2, ry)

        path = 'M %(startx)f,%(y)f ' \
               'h %(width)f ' \
               'q %(rx)f,0 %(rx)f,%(ry)f ' \
               'v %(height)f ' \
               'q 0,%(ry)f -%(rx)f,%(ry)f ' \
               'h -%(width)f ' \
               'q -%(rx)f,0 -%(rx)f,-%(ry)f ' \
               'v -%(height)f ' \
               'q 0,-%(ry)f %(rx)f,-%(ry)f ' \
               'Z' \
               % dict(startx=x+rx, x=x, y=y, width=width-(2*rx), height=height-(2*ry), rx=rx, ry=ry)

    else:
        path = "M %f,%f H %f V %f H %f Z" % (x, y, width+x, height+y, x)

    return path


def ellipse_to_path(node):
    rx = float(node.get('rx', "0")) or float(node.get('r', "0"))
    ry = float(node.get('ry', "0")) or float(node.get('r', "0"))
    cx = float(node.get('cx'))
    cy = float(node.get('cy'))

    path = 'M %(cx_r)f,%(cy)f' \
           'C %(cx_r)f,%(cy_r)f %(cx)f,%(cy_r)f %(cx)f,%(cy_r)f ' \
           '%(cxr)f,%(cy_r)f %(cxr)f,%(cy)f %(cxr)f,%(cy)f ' \
           '%(cxr)f,%(cyr)f %(cx)f,%(cyr)f %(cx)f,%(cyr)f ' \
           '%(cx_r)f,%(cyr)f %(cx_r)f,%(cy)f %(cx_r)f,%(cy)f ' \
           'Z' \
           % dict(cx=cx, cx_r=cx-rx, cxr=cx+rx, cy=cy, cyr=cy+ry, cy_r=cy-ry)

    return path


def circle_to_path(node):
    cx = float(node.get('cx'))
    cy = float(node.get('cy'))
    r = float(node.get('r'))

    path = 'M %(xstart)f, %(cy)f ' \
           'a %(r)f,%(r)f 0 1,0 %(rr)f,0 ' \
           'a %(r)f,%(r)f 0 1,0 -%(rr)f,0 ' \
           % dict(xstart=(cx-r), cy=cy, r=r, rr=(r*2))

    return path
