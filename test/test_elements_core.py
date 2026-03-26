''' Tests for Element base class and common element operations.

    Covers element creation, label placement, anchors, transforms,
    reverse, flip, and various element types.
'''
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import schemdraw
import schemdraw.elements as elm


def setup():
    schemdraw.use('svg')


def test_element_label_positions():
    ''' Labels can be placed at top, bottom, left, right, center '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        r = d.add(elm.Resistor()
                  .label('top', loc='top')
                  .label('bot', loc='bottom')
                  .label('lft', loc='left')
                  .label('rgt', loc='right')
                  .label('ctr', loc='center'))
    assert len(r.segments) > 0


def test_element_label_with_params():
    ''' Labels accept fontsize, color, rotation '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        r = d.add(elm.Resistor().label('R1', fontsize=18, color='red', rotate=45))
    assert len(r.segments) > 0


def test_element_directions():
    ''' Elements can be placed in all four directions '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Resistor().right()
        d += elm.Capacitor().down()
        d += elm.Inductor().left()
        d += elm.Diode().up()
    assert len(d.elements) == 4


def test_element_at_anchor():
    ''' Elements can be placed at another element's anchor '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        r = d.add(elm.Resistor())
        c = d.add(elm.Capacitor().at(r.start).down())
    assert c is not None


def test_element_anchors():
    ''' Two-terminal elements have start, end, center anchors '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        r = d.add(elm.Resistor())
    assert hasattr(r, 'start')
    assert hasattr(r, 'end')
    assert hasattr(r, 'center')


def test_element_reverse():
    ''' Reversing an element flips it horizontally '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Diode().reverse()
    assert len(d.elements) == 1


def test_element_flip():
    ''' Flipping an element mirrors it vertically '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Diode().flip()
    assert len(d.elements) == 1


def test_element_scale():
    ''' Elements can be scaled '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Resistor().scale(2)
    assert len(d.elements) == 1


def test_element_color():
    ''' Elements accept color parameter '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Resistor().color('blue')
        d += elm.Capacitor().color('#ff0000')
    assert len(d.elements) == 2


def test_element_fill():
    ''' Elements accept fill parameter '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Resistor().fill('yellow')
    assert len(d.elements) == 1


def test_element_linestyle():
    ''' Elements accept line style '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Resistor().linestyle('--')
        d += elm.Capacitor().linestyle(':')
    assert len(d.elements) == 2


def test_element_length():
    ''' Elements can have custom length '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Resistor().length(5)
    assert len(d.elements) == 1


def test_element_theta():
    ''' Elements can be placed at arbitrary angles '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Resistor().theta(45)
    assert len(d.elements) == 1


def test_element_zorder():
    ''' Elements accept zorder for layering '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Line().zorder(1)
        d += elm.Resistor().zorder(5)
    assert len(d.elements) == 2


def test_element_get_bbox():
    ''' Elements have bounding boxes '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        r = d.add(elm.Resistor())
    bbox = r.get_bbox(transform=True)
    assert bbox.xmax > bbox.xmin


def test_various_elements():
    ''' Smoke test for various element types '''
    setup()
    elements_to_test = [
        elm.Resistor, elm.Capacitor, elm.Inductor,
        elm.Diode, elm.LED, elm.Ground, elm.Dot,
        elm.Line, elm.Arrow, elm.SourceV, elm.SourceI,
        elm.BatteryCell, elm.Switch,
    ]
    with schemdraw.Drawing(show=False) as d:
        for E in elements_to_test:
            d += E()
    assert len(d.elements) == len(elements_to_test)


def test_opamp():
    ''' Opamp element has correct anchors '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        op = d.add(elm.Opamp())
    assert hasattr(op, 'in1')
    assert hasattr(op, 'in2')
    assert hasattr(op, 'out')


def test_element_tox_toy():
    ''' tox and toy extend elements to coordinate '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        r = d.add(elm.Resistor())
        d += elm.Line().down().toy(r.start)
    assert len(d.elements) == 2


def test_element_multiline_label():
    ''' Labels can be multiline (list of strings) '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Resistor().label(['Line 1', 'Line 2'])
    assert len(d.elements) == 1


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
