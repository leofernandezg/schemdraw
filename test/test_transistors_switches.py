''' Tests for transistor and switch elements to improve coverage.

    Exercises all element types in transistors.py and switches.py.
'''
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import schemdraw
import schemdraw.elements as elm


def setup():
    schemdraw.use('svg')


# --- Transistors ---

def test_bjt_npn():
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.BjtNpn()
    d += elm.BjtNpn2()
    assert len(d.elements) == 2


def test_bjt_pnp():
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.BjtPnp()
    d += elm.BjtPnp2()
    assert len(d.elements) == 2


def test_nfet():
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.NFet()
    d += elm.NFet2()
    assert len(d.elements) == 2


def test_pfet():
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.PFet()
    d += elm.PFet2()
    assert len(d.elements) == 2


def test_jfet():
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.JFetN()
    d += elm.JFetN2()
    d += elm.JFetP()
    d += elm.JFetP2()
    assert len(d.elements) == 4


def test_nmos_pmos():
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.NMos()
    d += elm.NMos2()
    d += elm.PMos()
    d += elm.PMos2()
    assert len(d.elements) == 4


def test_analog_fets():
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.AnalogNFet()
    d += elm.AnalogPFet()
    d += elm.AnalogBiasedFet()
    assert len(d.elements) == 3


def test_igbt():
    setup()
    d = schemdraw.Drawing(show=False)
    from schemdraw.elements.transistors import IgbtN, IgbtP
    d += IgbtN()
    d += IgbtP()
    assert len(d.elements) == 2


def test_photo_transistors():
    setup()
    d = schemdraw.Drawing(show=False)
    from schemdraw.elements.transistors import NpnPhoto, PnpPhoto
    d += NpnPhoto()
    d += PnpPhoto()
    assert len(d.elements) == 2


def test_schottky_transistors():
    setup()
    d = schemdraw.Drawing(show=False)
    from schemdraw.elements.transistors import NpnSchottky, PnpSchottky
    d += NpnSchottky()
    d += PnpSchottky()
    assert len(d.elements) == 2


def test_hemt():
    setup()
    d = schemdraw.Drawing(show=False)
    from schemdraw.elements.transistors import Hemt
    d += Hemt()
    assert len(d.elements) == 1


def test_transistor_anchors():
    setup()
    d = schemdraw.Drawing(show=False)
    t = d.add(elm.BjtNpn())
    assert hasattr(t, 'base')
    assert hasattr(t, 'collector')
    assert hasattr(t, 'emitter')


def test_fet_anchors():
    setup()
    d = schemdraw.Drawing(show=False)
    t = d.add(elm.NFet())
    assert hasattr(t, 'gate')
    assert hasattr(t, 'drain')
    assert hasattr(t, 'source')


# --- Switches ---

def test_switch():
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.Switch()
    assert len(d.elements) == 1


def test_switch_spdt():
    setup()
    d = schemdraw.Drawing(show=False)
    from schemdraw.elements.switches import SwitchSpdt, SwitchSpdt2
    d += SwitchSpdt()
    d += SwitchSpdt2()
    assert len(d.elements) == 2


def test_switch_dpst():
    setup()
    d = schemdraw.Drawing(show=False)
    from schemdraw.elements.switches import SwitchDpst
    d += SwitchDpst()
    assert len(d.elements) == 1


def test_switch_dpdt():
    setup()
    d = schemdraw.Drawing(show=False)
    from schemdraw.elements.switches import SwitchDpdt
    d += SwitchDpdt()
    assert len(d.elements) == 1


def test_button():
    setup()
    d = schemdraw.Drawing(show=False)
    from schemdraw.elements.switches import Button
    d += Button()
    assert len(d.elements) == 1


def test_switch_dip():
    setup()
    d = schemdraw.Drawing(show=False)
    from schemdraw.elements.switches import SwitchDIP
    d += SwitchDIP()
    assert len(d.elements) == 1


def test_switch_rotary():
    setup()
    d = schemdraw.Drawing(show=False)
    from schemdraw.elements.switches import SwitchRotary
    d += SwitchRotary()
    assert len(d.elements) == 1


def test_switch_reed():
    setup()
    d = schemdraw.Drawing(show=False)
    from schemdraw.elements.switches import SwitchReed
    d += SwitchReed()
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
