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


def test_bjt2_variants():
    ''' Bjt2 with different parameters '''
    setup()
    d = schemdraw.Drawing(show=False)
    from schemdraw.elements.transistors import BjtPnp2c, BjtPnp2c2
    d += BjtPnp2c()
    d += BjtPnp2c2()
    assert len(d.elements) == 2


def test_bjt_no_circle():
    ''' BJT without circle '''
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.BjtNpn(circle=False)
    d += elm.BjtPnp(circle=False)
    assert len(d.elements) == 2


def test_fet_bulk():
    ''' FET with bulk terminal '''
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.NFet(bulk=True)
    d += elm.PFet(bulk=True)
    assert len(d.elements) == 2


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


def test_switch_open_close():
    ''' Switch with action parameter '''
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.Switch(action='open')
    d += elm.Switch(action='close')
    assert len(d.elements) == 2


def test_switch_spdt_action():
    setup()
    d = schemdraw.Drawing(show=False)
    from schemdraw.elements.switches import SwitchSpdt
    d += SwitchSpdt(action='open')
    d += SwitchSpdt(action='close')
    assert len(d.elements) == 2


def test_switch_dpdt_action():
    setup()
    d = schemdraw.Drawing(show=False)
    from schemdraw.elements.switches import SwitchDpdt
    d += SwitchDpdt(action='open')
    d += SwitchDpdt(action='close')
    assert len(d.elements) == 2


def test_switch_dpst_action():
    setup()
    d = schemdraw.Drawing(show=False)
    from schemdraw.elements.switches import SwitchDpst
    d += SwitchDpst(action='open')
    d += SwitchDpst(action='close')
    assert len(d.elements) == 2


def test_switch_dip_options():
    setup()
    d = schemdraw.Drawing(show=False)
    from schemdraw.elements.switches import SwitchDIP
    d += SwitchDIP(n=4, pattern=(True, False, True, False))
    assert len(d.elements) == 1


def test_switch_rotary_options():
    setup()
    d = schemdraw.Drawing(show=False)
    from schemdraw.elements.switches import SwitchRotary
    d += SwitchRotary(n=6, position=3)
    assert len(d.elements) == 1


# --- contacts=False and nc=True variants ---

def test_switch_no_contacts():
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.Switch(contacts=False)
    assert len(d.elements) == 1


def test_switch_nc():
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.Switch(nc=True)
    assert len(d.elements) == 1


def test_switch_spdt2_no_contacts():
    setup()
    d = schemdraw.Drawing(show=False)
    from schemdraw.elements.switches import SwitchSpdt2
    d += SwitchSpdt2(contacts=False)
    assert len(d.elements) == 1


def test_button_no_contacts():
    setup()
    d = schemdraw.Drawing(show=False)
    from schemdraw.elements.switches import Button
    d += Button(contacts=False)
    assert len(d.elements) == 1


def test_switch_dpst_no_contacts():
    setup()
    d = schemdraw.Drawing(show=False)
    from schemdraw.elements.switches import SwitchDpst
    d += SwitchDpst(contacts=False)
    assert len(d.elements) == 1


def test_switch_dpdt_no_contacts():
    setup()
    d = schemdraw.Drawing(show=False)
    from schemdraw.elements.switches import SwitchDpdt
    d += SwitchDpdt(contacts=False)
    assert len(d.elements) == 1


# --- Transistor parameter variants ---

def test_mosfet_with_diode():
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.NFet(diode=True)
    d += elm.PFet(diode=True)
    assert len(d.elements) == 2


def test_mosfet_with_circle():
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.NFet(circle=True)
    d += elm.PFet(circle=True)
    assert len(d.elements) == 2


def test_mosfet2_with_diode():
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.NFet2(diode=True)
    d += elm.PFet2(diode=True)
    assert len(d.elements) == 2


def test_mosfet2_with_circle():
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.NFet2(circle=True)
    d += elm.PFet2(circle=True)
    assert len(d.elements) == 2


def test_nfet2_bulk():
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.NFet2(bulk=True)
    assert len(d.elements) == 1


def test_pfet2_bulk():
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.PFet2(bulk=True)
    assert len(d.elements) == 1


def test_nfet2_reverse():
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.NFet2().reverse()
    assert len(d.elements) == 1


def test_pfet2_reverse():
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.PFet2().reverse()
    assert len(d.elements) == 1


def test_jfet2_circle():
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.JFetN2(circle=True)
    d += elm.JFetP2(circle=True)
    assert len(d.elements) == 2


def test_jfet2_reverse():
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.JFetN2().reverse()
    d += elm.JFetP2().reverse()
    assert len(d.elements) == 2


def test_bjt2_circle():
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.BjtNpn2(circle=True)
    d += elm.BjtPnp2(circle=True)
    assert len(d.elements) == 2


def test_bjt2_reverse():
    setup()
    d = schemdraw.Drawing(show=False)
    d += elm.BjtNpn2().reverse()
    d += elm.BjtPnp2().reverse()
    assert len(d.elements) == 2


def test_hemt_split():
    setup()
    d = schemdraw.Drawing(show=False)
    from schemdraw.elements.transistors import Hemt
    d += Hemt(split=True)
    assert len(d.elements) == 1


def test_hemt_arrow():
    setup()
    d = schemdraw.Drawing(show=False)
    from schemdraw.elements.transistors import Hemt
    d += Hemt(arrow='>')
    d += Hemt(arrow='<')
    assert len(d.elements) == 2


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
