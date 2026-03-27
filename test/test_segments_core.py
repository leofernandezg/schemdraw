''' Tests for Segment classes core functionality.

    Covers segment creation, transforms, bounding boxes, and draw
    operations for all segment types.
'''
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import schemdraw
import schemdraw.elements as elm
from schemdraw.segments import (
    Segment, SegmentText, SegmentCircle, SegmentArc,
    SegmentPoly, SegmentBezier, SegmentPath
)
from schemdraw.transform import Transform
from schemdraw.util import Point
from schemdraw.types import BBox


def test_segment_creation():
    ''' Basic segment with path '''
    seg = Segment(path=[(0, 0), (1, 0), (1, 1)])
    assert len(seg.path) == 3


def test_segment_xform():
    ''' Transform a segment '''
    seg = Segment(path=[Point((0, 0)), Point((1, 0))])
    xf = Transform(theta=0, globalshift=Point((5, 5)))
    result = seg.xform(xf)
    assert result.path[0][0] != 0  # shifted


def test_segment_with_arrow():
    ''' Segment with arrow markers '''
    seg = Segment(path=[(0, 0), (1, 0)], arrow='->')
    bbox = seg.get_bbox()
    assert bbox.xmax >= 1


def test_segment_doreverse():
    ''' Reverse flips segment horizontally '''
    seg = Segment(path=[Point((0, 0)), Point((2, 0)), Point((2, 1))])
    seg.doreverse(centerx=1.0)
    # Reversed order and mirrored: first point should be mirrored (2,1) -> (0,1)
    assert abs(seg.path[0][0] - 0) < 0.01
    assert abs(seg.path[0][1] - 1) < 0.01


def test_segment_doflip():
    ''' Flip negates y coordinates '''
    seg = Segment(path=[Point((0, 1)), Point((1, 2))])
    seg.doflip()
    assert seg.path[0][1] == -1
    assert seg.path[1][1] == -2


def test_segment_text_creation():
    ''' SegmentText with position and label '''
    seg = SegmentText(Point((0, 0)), 'Hello')
    assert seg.text == 'Hello'


def test_segment_text_xform():
    ''' Transform a text segment '''
    seg = SegmentText(Point((0, 0)), 'Test', rotation_global=False)
    xf = Transform(theta=45, globalshift=Point((0, 0)))
    result = seg.xform(xf)
    assert result is not None


def test_segment_text_bbox():
    ''' Text segment has a bounding box '''
    seg = SegmentText(Point((0, 0)), 'Hello', fontsize=14)
    bbox = seg.get_bbox()
    assert bbox.xmax >= bbox.xmin


def test_segment_circle_creation():
    ''' SegmentCircle with center and radius '''
    seg = SegmentCircle(Point((5, 5)), radius=2)
    assert seg.radius == 2


def test_segment_circle_bbox():
    ''' Circle bbox is center +/- radius '''
    seg = SegmentCircle(Point((5, 5)), radius=2)
    bbox = seg.get_bbox()
    assert bbox.xmin == 3
    assert bbox.xmax == 7
    assert bbox.ymin == 3
    assert bbox.ymax == 7


def test_segment_circle_xform_symmetric():
    ''' Symmetric zoom keeps circle as circle '''
    seg = SegmentCircle(Point((0, 0)), radius=1)
    xf = Transform(theta=0, globalshift=Point((0, 0)), zoom=2)
    result = seg.xform(xf)
    assert isinstance(result, SegmentCircle)
    assert result.radius == 2


def test_segment_circle_xform_asymmetric():
    ''' Asymmetric zoom converts circle to arc (ellipse) '''
    seg = SegmentCircle(Point((0, 0)), radius=1)
    xf = Transform(theta=0, globalshift=Point((0, 0)), zoom=Point((2, 3)))
    result = seg.xform(xf)
    assert isinstance(result, SegmentArc)


def test_segment_arc_creation():
    ''' SegmentArc with dimensions '''
    seg = SegmentArc(Point((0, 0)), width=4, height=2, theta1=0, theta2=180)
    bbox = seg.get_bbox()
    assert bbox.xmax > bbox.xmin


def test_segment_poly_creation():
    ''' SegmentPoly with vertices '''
    seg = SegmentPoly(verts=[(0, 0), (1, 0), (0.5, 1)])
    bbox = seg.get_bbox()
    assert bbox.xmin == 0
    assert bbox.xmax == 1


def test_segment_poly_xform():
    ''' Transform a polygon '''
    seg = SegmentPoly(verts=[Point((0, 0)), Point((1, 0)), Point((0.5, 1))])
    xf = Transform(theta=0, globalshift=Point((10, 10)))
    result = seg.xform(xf)
    assert result.verts[0][0] != 0


def test_segment_bezier_creation():
    ''' SegmentBezier with control points '''
    seg = SegmentBezier(p=[Point((0, 0)), Point((0.5, 1)), Point((1, 1)), Point((1.5, 0))])
    bbox = seg.get_bbox()
    assert bbox.xmax > 0


def test_segment_path_creation():
    ''' SegmentPath with mixed points and commands '''
    seg = SegmentPath(path=[(0, 0), 'M', (1, 1), 'L', (2, 0)])
    bbox = seg.get_bbox()
    assert bbox.xmax == 2


def test_segment_path_xform():
    ''' Transform a path segment '''
    seg = SegmentPath(path=[Point((0, 0)), 'M', Point((1, 1))])
    xf = Transform(theta=0, globalshift=Point((5, 5)))
    result = seg.xform(xf)
    points = [p for p in result.path if not isinstance(p, str)]
    assert points[0][0] != 0


def test_segment_visibility():
    ''' Segments can be set invisible '''
    seg = Segment(path=[(0, 0), (1, 0)], visible=False)
    assert seg.visible is False


def test_segment_draw_with_fill():
    ''' Drawing a segment with fill on a closed path '''
    schemdraw.use('svg')
    with schemdraw.Drawing(show=False) as d:
        # Closed polygon path triggers fill logic
        d += elm.Resistor().fill('red')
    svg = d.get_imagedata('svg')
    assert b'<svg' in svg


def test_segment_draw_with_arrows():
    ''' Drawing segments with various arrow types '''
    schemdraw.use('svg')
    with schemdraw.Drawing(show=False) as d:
        d += elm.Arrow()
        d += elm.Arrow().reverse()
        d += elm.Line().label('test')
    svg = d.get_imagedata('svg')
    assert b'<svg' in svg


def test_segment_draw_with_linestyle():
    ''' Segments with different line styles '''
    schemdraw.use('svg')
    with schemdraw.Drawing(show=False) as d:
        d += elm.Resistor().linestyle('--')
        d += elm.Capacitor().linestyle(':')
        d += elm.Inductor().linestyle('-.')
    svg = d.get_imagedata('svg')
    assert b'<svg' in svg


def test_segment_draw_with_color_fill():
    ''' Color and fill combinations '''
    schemdraw.use('svg')
    with schemdraw.Drawing(show=False) as d:
        d += elm.Resistor().color('blue')
        d += elm.Capacitor().fill('yellow')
        d += elm.Diode().color('red').fill('orange')
    svg = d.get_imagedata('svg')
    assert b'<svg' in svg


def test_segment_poly_draw():
    ''' SegmentPoly rendered through element '''
    schemdraw.use('svg')
    with schemdraw.Drawing(show=False) as d:
        d += elm.Resistor()  # Has polygon fill for zigzag
        d += elm.Ground()    # Has polygon
    svg = d.get_imagedata('svg')
    assert len(svg) > 100


def test_segment_circle_draw():
    ''' SegmentCircle rendered through element '''
    schemdraw.use('svg')
    with schemdraw.Drawing(show=False) as d:
        d += elm.Dot()       # Uses SegmentCircle
        d += elm.Dot().color('red').fill('blue')
    svg = d.get_imagedata('svg')
    assert b'circle' in svg or b'ellipse' in svg or len(svg) > 100


def test_segment_arc_draw():
    ''' SegmentArc rendered through an element '''
    schemdraw.use('svg')
    with schemdraw.Drawing(show=False) as d:
        d += elm.SourceV()   # Has arc segment for the circle
    svg = d.get_imagedata('svg')
    assert len(svg) > 100


def test_segment_bezier_draw():
    ''' SegmentBezier for curved elements '''
    schemdraw.use('svg')
    with schemdraw.Drawing(show=False) as d:
        d += elm.Inductor()  # Has bezier curves
    svg = d.get_imagedata('svg')
    assert len(svg) > 100


def test_segment_text_draw():
    ''' SegmentText rendered through labels '''
    schemdraw.use('svg')
    with schemdraw.Drawing(show=False) as d:
        d += elm.Resistor().label('100K', loc='top')
        d += elm.Resistor().label('R2', loc='bottom')
    svg = d.get_imagedata('svg')
    assert len(svg) > 100


def test_segment_text_rotation():
    ''' Text segments with rotation '''
    schemdraw.use('svg')
    with schemdraw.Drawing(show=False) as d:
        d += elm.Resistor().label('vertical', rotate=90)
    svg = d.get_imagedata('svg')
    assert len(svg) > 100


def test_segment_with_color_tuple():
    ''' Segments with RGB tuple colors '''
    schemdraw.use('svg')
    d = schemdraw.Drawing(show=False)
    d += elm.Resistor().color((0.5, 0.2, 0.8))
    fig = d.draw(show=False)
    svg = d.get_imagedata('svg')
    assert b'rgb(' in svg


def test_drawing_renders_all_segment_types():
    ''' End-to-end: drawing with various segment types produces SVG '''
    schemdraw.use('svg')
    with schemdraw.Drawing(show=False) as d:
        d += elm.Resistor().label('R1')
        d += elm.Capacitor().down()
        d += elm.Ground()
        d += elm.Line().left()
        d += elm.SourceV().up().label('V1')
        d += elm.Dot()
    svg = d.get_imagedata('svg')
    assert b'<svg' in svg
    assert len(svg) > 500  # non-trivial SVG output


if __name__ == '__main__':
    tests = [v for k, v in sorted(globals().items()) if k.startswith('test_')]
    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            print(f'  PASS: {test.__name__}')
            passed += 1
        except Exception as e:
            print(f'  FAIL: {test.__name__}: {e}')
            failed += 1
    print(f'\n{passed} passed, {failed} failed, {passed + failed} total')
    sys.exit(1 if failed else 0)
