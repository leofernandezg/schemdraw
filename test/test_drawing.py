''' Tests for Drawing class core functionality.

    Covers drawing creation, element placement, state management,
    configuration, theming, and output generation.
'''
import sys
import os


import schemdraw
import schemdraw.elements as elm
from schemdraw.util import Point


def setup():
    schemdraw.use('svg')


def test_drawing_add_element():
    ''' Add elements and verify they are tracked '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Resistor()
        d += elm.Capacitor()
    assert len(d.elements) == 2


def test_drawing_add_elements():
    ''' add_elements adds multiple at once '''
    setup()
    d = schemdraw.Drawing(show=False)
    d.add_elements(elm.Resistor(), elm.Capacitor(), elm.Inductor())
    assert len(d.elements) == 3


def test_drawing_contains():
    ''' __contains__ checks element membership '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        r = d.add(elm.Resistor())
        c = d.add(elm.Capacitor())
    assert r in d
    assert c in d


def test_drawing_get_bbox():
    ''' get_bbox returns bounding box of all elements '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Resistor()
        d += elm.Capacitor().down()
    bbox = d.get_bbox()
    assert bbox.xmax > bbox.xmin
    assert bbox.ymax > bbox.ymin


def test_drawing_get_segments():
    ''' get_segments returns flattened segment list '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Resistor()
    segs = d.get_segments()
    assert len(segs) > 0


def test_drawing_move():
    ''' move shifts drawing position '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Resistor()
        pos_before = Point(d.here)
        d.move(dx=2, dy=3)
        assert abs(d.here[0] - pos_before[0] - 2) < 0.01
        assert abs(d.here[1] - pos_before[1] - 3) < 0.01


def test_drawing_move_from():
    ''' move_from sets position relative to a reference point '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        r = d.add(elm.Resistor())
        d.move_from(r.end, dx=1, dy=1, theta=90)
        assert d.theta == 90


def test_drawing_push_pop():
    ''' push/pop saves and restores drawing state '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Resistor()
        d.push()
        saved_pos = Point(d.here)
        saved_theta = d.theta
        d += elm.Capacitor().down()
        d.pop()
        assert abs(d.here[0] - saved_pos[0]) < 0.01
        assert abs(d.here[1] - saved_pos[1]) < 0.01
        assert d.theta == saved_theta


def test_drawing_pop_empty():
    ''' pop on empty state stack is a no-op '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Resistor()
        d.pop()  # Should not crash


def test_drawing_set_anchor():
    ''' set_anchor stores current position as named anchor '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Resistor()
        d.set_anchor('mypoint')
    assert 'mypoint' in d.anchors


def test_drawing_config():
    ''' config sets drawing parameters '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        d.config(fontsize=16, unit=4, color='blue')
        d += elm.Resistor()
    assert d.dwgparams['fontsize'] == 16
    assert d.dwgparams['unit'] == 4


def test_drawing_get_imagedata_svg():
    ''' get_imagedata returns SVG bytes '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Resistor().label('R1')
    data = d.get_imagedata('svg')
    assert b'<svg' in data


def test_drawing_repr_svg():
    ''' _repr_svg_ returns SVG string for Jupyter '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Resistor()
    svg = d._repr_svg_()
    assert '<svg' in svg


def test_drawing_save_svg(tmp_path):
    ''' save writes SVG file '''
    setup()
    outfile = str(tmp_path / 'test.svg') if hasattr(tmp_path, '__truediv__') else '/tmp/test_schemdraw.svg'
    with schemdraw.Drawing(show=False) as d:
        d += elm.Resistor()
    d.save(outfile)
    assert os.path.exists(outfile)
    with open(outfile) as f:
        assert '<svg' in f.read()
    os.unlink(outfile)


def test_theme_dark():
    ''' theme("dark") sets dark colors '''
    setup()
    schemdraw.theme('dark')
    from schemdraw.schemdraw import schemdrawstyle
    assert schemdrawstyle['color'] == 'white'
    assert schemdrawstyle['bgcolor'] == 'black'
    schemdraw.theme('default')


def test_theme_all_options():
    ''' All theme options run without error '''
    setup()
    for t in ['solarizedd', 'solarizedl', 'onedork', 'oceans16',
              'monokai', 'gruvboxl', 'gruvboxd', 'grade3', 'chesterish']:
        schemdraw.theme(t)
    schemdraw.theme('default')


def test_theme_invalid():
    ''' Invalid theme raises ValueError '''
    setup()
    try:
        schemdraw.theme('nonexistent')
        assert False, 'Should have raised ValueError'
    except ValueError:
        pass
    schemdraw.theme('default')


def test_drawing_context_file(tmp_path):
    ''' Drawing context manager saves to file '''
    setup()
    outfile = str(tmp_path / 'ctx.svg') if hasattr(tmp_path, '__truediv__') else '/tmp/test_ctx.svg'
    with schemdraw.Drawing(file=outfile, show=False) as d:
        d += elm.Resistor()
    assert os.path.exists(outfile)
    os.unlink(outfile)


def test_drawing_hold():
    ''' hold() context manager saves and restores state '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Resistor()
        pos = Point(d.here)
        with d.hold():
            d += elm.Capacitor().down()
        assert abs(d.here[0] - pos[0]) < 0.01
        assert abs(d.here[1] - pos[1]) < 0.01


def test_drawing_config_all_params():
    ''' config sets all available parameters '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        d.config(unit=4, inches_per_unit=0.6, fontsize=16, font='serif',
                 color='red', lw=3, ls='--', fill='yellow', bgcolor='white',
                 margin=0.5, mathfont='cm')
        d += elm.Resistor()
    assert d.dwgparams['inches_per_unit'] == 0.6
    assert d.dwgparams['font'] == 'serif'
    assert d.dwgparams['lw'] == 3
    assert d.dwgparams['ls'] == '--'
    assert d.dwgparams['fill'] == 'yellow'
    assert d.dwgparams['bgcolor'] == 'white'
    assert d.dwgparams['margin'] == 0.5
    assert d.dwgparams['mathfont'] == 'cm'


def test_drawing_draw_returns_figure():
    ''' draw() returns a Figure object '''
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.Resistor()
    fig = d.draw(show=False)
    assert fig is not None


def test_drawing_save_without_draw():
    ''' save() auto-draws if not drawn yet '''
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.Resistor()
    outfile = '/tmp/test_auto_draw.svg'
    d.save(outfile)
    assert os.path.exists(outfile)
    os.unlink(outfile)


def test_drawing_get_imagedata_without_draw():
    ''' get_imagedata auto-draws if not drawn yet '''
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.Resistor()
    data = d.get_imagedata('svg')
    assert b'<svg' in data


def test_drawing_add_svgdef():
    ''' add_svgdef stores custom SVG defs '''
    setup()
    d = schemdraw.Drawing(show=False)
    d.add_svgdef('<pattern id="test"/>')
    assert len(d.svgdefs) == 1


def test_drawing_bgcolor():
    ''' Drawing with background color '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        d.config(bgcolor='lightgray')
        d += elm.Resistor()
    svg = d.get_imagedata('svg')
    assert b'lightgray' in svg


def test_drawing_interactive_mode():
    ''' interactive() sets interactive flag '''
    setup()
    d = schemdraw.Drawing(show=False)
    d.interactive(True)
    assert d._interactive is True
    d.interactive(False)
    assert d._interactive is False


def test_drawing_getattr_anchor():
    ''' Drawing anchors accessible as attributes '''
    setup()
    with schemdraw.Drawing(show=False) as d:
        d += elm.Resistor()
        d.set_anchor('test_pt')
    assert d.test_pt is not None


def test_drawing_getattr_invalid():
    ''' Invalid attribute raises AttributeError '''
    setup()
    d = schemdraw.Drawing(show=False)
    try:
        _ = d.nonexistent_attribute
        assert False, 'Should have raised AttributeError'
    except AttributeError:
        pass


if __name__ == '__main__':
    import pathlib
    tests = [v for k, v in sorted(globals().items()) if k.startswith('test_')]
    passed = 0
    failed = 0
    for test in tests:
        try:
            import inspect
            if 'tmp_path' in inspect.signature(test).parameters:
                test(pathlib.Path('/tmp'))
            else:
                test()
            print(f'  PASS: {test.__name__}')
            passed += 1
        except Exception as e:
            print(f'  FAIL: {test.__name__}: {e}')
            failed += 1
    print(f'\n{passed} passed, {failed} failed, {passed + failed} total')
    sys.exit(1 if failed else 0)
