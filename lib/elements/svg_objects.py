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

    path = 'M %(cxrx)f,%(cy)f ' \
           'A %(rx)f,%(ry)f 0 0 1 '\
           '%(cx)f,%(cyry)f %(rx)f,%(ry)f 0 0 1 ' \
           '%(cx_rx)f,%(cy)f %(rx)f,%(ry)f 0 0 1 ' \
           '%(cx)f,%(cy_ry)f %(rx)f,%(ry)f 0 0 1 ' \
           '%(cxrx)f,%(cy)f ' \
           % dict(cxrx=cx+rx, cyry=cy+ry, cx_rx=cx-rx, cy_ry=cy-ry, rx=rx, ry=ry, cx=cx, cy=cy)

    return path


def circle_to_path(node):
    cx = float(node.get('cx'))
    cy = float(node.get('cy'))
    r = float(node.get('r'))

    path = 'M %(xstart)f,%(cy)f ' \
           'a %(r)f,%(r)f 0 0 1 '\
           '-%(r)f,%(r)f %(r)f,%(r)f 0 0 1 ' \
           '-%(r)f,-%(r)f %(r)f,%(r)f 0 0 1 ' \
           '%(r)f,-%(r)f %(r)f,%(r)f 0 0 1 ' \
           '%(r)f,%(r)f ' \
           % dict(xstart=cx+r, cy=cy, r=r)

    return path
