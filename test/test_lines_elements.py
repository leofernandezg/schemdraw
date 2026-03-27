''' Tests for line and annotation elements (schemdraw/elements/lines.py).

    Exercises all element types defined in lines.py to improve coverage.
'''
import sys


import schemdraw
import schemdraw.elements as elm


def setup():
    schemdraw.use('svg')


def test_line():
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Line()
    assert len(d.elements) == 1


def test_arrow():
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Arrow()
    assert len(d.elements) == 1


def test_arrowhead():
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Line()
        d += elm.Arrowhead()
    assert len(d.elements) == 2


def test_dot():
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Dot()
        d += elm.Dot(open=True)
    assert len(d.elements) == 2


def test_dot_dot_dot():
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.DotDotDot()
    assert len(d.elements) == 1


def test_gap():
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Gap().label('V')
    assert len(d.elements) == 1


def test_label_element():
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Label().label('A')
    assert len(d.elements) == 1


def test_tag():
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Tag().label('Vcc')
        d += elm.Tag().right().label('GND').reverse()
    assert len(d.elements) == 2


def test_wire():
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Wire('n')
        d += elm.Wire('|-')
        d += elm.Wire('-|')
    assert len(d.elements) == 3


def test_arc2():
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Arc2()
    assert len(d.elements) == 1


def test_arc3():
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Arc3()
    assert len(d.elements) == 1


def test_arcn():
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.ArcN()
    assert len(d.elements) == 1


def test_arcz():
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.ArcZ()
    assert len(d.elements) == 1



def test_current_label():
    setup()
    with schemdraw.Drawing(show=False) as d:
        r = d.add(elm.Resistor())
        d += elm.CurrentLabel().at(r).label('I')
    assert len(d.elements) == 2


def test_current_label_inline():
    setup()
    with schemdraw.Drawing(show=False) as d:
        r = d.add(elm.Resistor())
        d += elm.CurrentLabelInline(direction='in').at(r)
        d += elm.CurrentLabelInline(direction='out').at(r)
    assert len(d.elements) == 3


def test_loop_current():
    setup()
    with schemdraw.Drawing(show=False) as d:
        r1 = d.add(elm.Resistor())
        c1 = d.add(elm.Capacitor().down())
        l1 = d.add(elm.Line().left())
        v1 = d.add(elm.SourceV().up())
        d += elm.LoopCurrent([r1, c1, l1, v1])
    assert len(d.elements) == 5


def test_loop_arrow():
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.LoopArrow()
    assert len(d.elements) == 1


def test_rect():
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Rect(corner1=(0, 0), corner2=(3, 2))
    assert len(d.elements) == 1


def test_annotate():
    setup()
    with schemdraw.Drawing(show=False) as d:
        r = d.add(elm.Resistor())
        d += elm.Annotate().at(r.start).delta(dx=0, dy=1).label('Note')
    assert len(d.elements) == 2


def test_encircle():
    setup()
    with schemdraw.Drawing(show=False) as d:
        r = d.add(elm.Resistor())
        c = d.add(elm.Capacitor())
        d += elm.Encircle([r, c])
    assert len(d.elements) == 3


def test_encircle_box():
    setup()
    with schemdraw.Drawing(show=False) as d:
        r = d.add(elm.Resistor())
        c = d.add(elm.Capacitor())
        d += elm.EncircleBox([r, c])
    assert len(d.elements) == 3


def test_data_bus_line():
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.DataBusLine()
    assert len(d.elements) == 1


def test_zlabel():
    setup()
    with schemdraw.Drawing(show=False) as d:
        from schemdraw.elements.lines import ZLabel
        d += ZLabel().label('Z')
    assert len(d.elements) == 1


def test_voltage_label_arc():
    setup()
    d = schemdraw.Drawing(show=False)
    r = d.add(elm.Resistor())
    from schemdraw.elements.lines import VoltageLabelArc
    d += VoltageLabelArc().at(r).label('V')
    assert len(d.elements) == 2


def test_voltage_label_arc_reversed():
    setup()
    d = schemdraw.Drawing(show=False)
    r = d.add(elm.Resistor())
    from schemdraw.elements.lines import VoltageLabelArc
    d += VoltageLabelArc(reverse=True).at(r)
    assert len(d.elements) == 2


def test_voltage_label_arc_bottom():
    setup()
    d = schemdraw.Drawing(show=False)
    r = d.add(elm.Resistor())
    from schemdraw.elements.lines import VoltageLabelArc
    d += VoltageLabelArc().at(r).label('V', loc='bottom')
    assert len(d.elements) == 2


def test_wire_all_shapes():
    ''' Test all Wire shape options '''
    setup()
    shapes = ['-', '|-', '-|', 'n', 'N', 'z', 'Z', 'c']
    with schemdraw.Drawing(show=False) as d:
        for s in shapes:
            d += elm.Wire(s)
    assert len(d.elements) == len(shapes)


def test_line_with_styling():
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.Line().color('red').linestyle('--')
    d += elm.Arrow().color('blue')
    fig = d.draw(show=False)
    svg = d.get_imagedata('svg')
    assert b'<svg' in svg


def test_encircle_with_draw():
    ''' Encircle drawn to SVG exercises anchor computation '''
    setup()
    d = schemdraw.Drawing(show=False)
    r = d.add(elm.Resistor())
    c = d.add(elm.Capacitor().down())
    d += elm.Encircle([r, c], padx=0.3, pady=0.3)
    svg = d.get_imagedata('svg')
    assert len(svg) > 100


def test_encircle_box_with_draw():
    ''' EncircleBox drawn to SVG exercises anchor computation '''
    setup()
    d = schemdraw.Drawing(show=False)
    r = d.add(elm.Resistor())
    c = d.add(elm.Capacitor().down())
    d += elm.EncircleBox([r, c], padx=0.3, pady=0.3)
    svg = d.get_imagedata('svg')
    assert len(svg) > 100


def test_encircle_anchors():
    ''' Encircle has cardinal and intercardinal anchors '''
    setup()
    d = schemdraw.Drawing(show=False)
    r = d.add(elm.Resistor())
    enc = d.add(elm.Encircle([r]))
    assert hasattr(enc, 'N')
    assert hasattr(enc, 'SE')
    assert hasattr(enc, 'NNE')


def test_encircle_box_anchors():
    ''' EncircleBox has cardinal anchors '''
    setup()
    d = schemdraw.Drawing(show=False)
    r = d.add(elm.Resistor())
    enc = d.add(elm.EncircleBox([r]))
    assert hasattr(enc, 'N')
    assert hasattr(enc, 'SE')


def test_current_label_arrow():
    ''' CurrentLabel with arrow (exercises _place_segment) '''
    setup()
    d = schemdraw.Drawing(show=False)
    r = d.add(elm.Resistor())
    d += elm.CurrentLabel(ofst=0.3).at(r).label('I')
    d += elm.CurrentLabel(ofst=0.3, reverse=True).at(r)
    assert len(d.elements) == 3


def test_current_label_arrow_bottom():
    ''' CurrentLabel on bottom side '''
    setup()
    d = schemdraw.Drawing(show=False)
    r = d.add(elm.Resistor())
    d += elm.CurrentLabel(loc='bottom').at(r)
    assert len(d.elements) == 2


def test_voltage_label_arrow_at_element():
    ''' VoltageLabelArrow placed at an element '''
    setup()
    d = schemdraw.Drawing(show=False)
    r = d.add(elm.Resistor())
    from schemdraw.elements.lines import VoltageLabelArc
    d += VoltageLabelArc().at(r).label('V')
    d += VoltageLabelArc(reverse=True).at(r)
    fig = d.draw(show=False)
    assert len(d.elements) == 3


def test_voltage_label_arrow_rotated():
    ''' VoltageLabelArrow on rotated element '''
    setup()
    d = schemdraw.Drawing(show=False)
    r = d.add(elm.Resistor().down())
    from schemdraw.elements.lines import VoltageLabelArc
    d += VoltageLabelArc().at(r)
    fig = d.draw(show=False)
    assert len(d.elements) == 2


def test_wire_idot():
    ''' Wire with idot parameter '''
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.Line().idot()
    d += elm.Line().idot(open=True)
    assert len(d.elements) == 2


def test_arc2_delta():
    ''' Arc2 with delta parameter '''
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.Arc2().delta(dx=2, dy=1)
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
