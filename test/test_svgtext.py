''' Tests for SVG text rendering in backends/svgtext.py

    Covers mathtextsvg(), string_width(), text_approx_size(), text_tosvg(),
    and XML special character handling.
'''
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from schemdraw.backends.svgtext import (
    mathtextsvg, string_width, text_approx_size, text_tosvg
)


def test_basic_superscript():
    ''' Basic superscript should produce valid tspan '''
    result = mathtextsvg('$x^{2}$')
    assert result is not None
    assert result.tag == 'tspan'


def test_basic_subscript():
    ''' Basic subscript should produce valid tspan '''
    result = mathtextsvg('$V_{out}$')
    assert result is not None
    assert result.tag == 'tspan'


def test_superscript_with_ampersand():
    ''' Ampersand in superscript should not crash XML parser '''
    result = mathtextsvg('$x^{a&b}$')
    assert result is not None


def test_subscript_with_angle_brackets():
    ''' Angle brackets in subscript should not crash XML parser '''
    result = mathtextsvg('$V_{<out>}$')
    assert result is not None


def test_superscript_single_char_special():
    ''' Single-char superscript with special char '''
    result = mathtextsvg('$x^>$')
    assert result is not None


def test_subscript_single_char_special():
    ''' Single-char subscript with special char '''
    result = mathtextsvg('$x_<$')
    assert result is not None


def test_overline_with_special_chars():
    ''' Overline content with special chars should not crash '''
    result = mathtextsvg(r'$\overline{a&b}$')
    assert result is not None


def test_sqrt_with_special_chars():
    ''' Sqrt content with special chars should not crash '''
    result = mathtextsvg(r'$\sqrt{a&b}$')
    assert result is not None


def test_plain_text_unchanged():
    ''' Non-math text should pass through unchanged '''
    result = mathtextsvg('Hello World')
    assert result.text == 'Hello World'


def test_mixed_math_and_text():
    ''' Text with embedded math expression '''
    result = mathtextsvg('Value: $x^{2}$ volts')
    assert result is not None


def test_numeric_superscript():
    ''' Numeric superscript uses Unicode characters '''
    result = mathtextsvg('$x^{23}$')
    text = ''.join(result.itertext())
    assert '²' in text or '³' in text


def test_numeric_subscript():
    ''' Numeric subscript uses Unicode characters '''
    result = mathtextsvg('$x_{12}$')
    text = ''.join(result.itertext())
    assert '₁' in text or '₂' in text


def test_latex_greek_replacement():
    ''' LaTeX Greek symbols get replaced '''
    result = mathtextsvg(r'$\alpha$')
    text = ''.join(result.itertext())
    assert 'α' in text


def test_latex_omega():
    ''' Omega symbol replacement '''
    result = mathtextsvg(r'$\Omega$')
    text = ''.join(result.itertext())
    assert 'Ω' in text


# --- string_width tests ---

def test_string_width_arial():
    ''' string_width returns positive value for Arial '''
    w = string_width('Hello', fontsize=12, font='Arial')
    assert w > 0


def test_string_width_times():
    ''' string_width returns positive value for Times '''
    w = string_width('Hello', fontsize=12, font='Times')
    assert w > 0


def test_string_width_serif():
    ''' string_width detects serif font '''
    w = string_width('Hello', fontsize=12, font='serif')
    assert w > 0


def test_string_width_empty():
    ''' Empty string has zero width '''
    w = string_width('', fontsize=12)
    assert w == 0


def test_string_width_special_chars_arial():
    ''' All character classes in Arial branch '''
    chars = 'lij| ![]fI.,:/\\t `-(){}r" *^zcsJkvxy aebdhnopqug#$L BSPEAKVXY&UwNRCHD QGOMm%@Ω W∠ ~'
    w = string_width(chars, fontsize=12, font='Arial')
    assert w > 0


def test_string_width_special_chars_times():
    ''' All character classes in Times branch '''
    chars = 'lij:.,;t | ![]fI/\\ `-(){}r sJ° "zcae?1 *^kvxy #$+<>=~FSP ELZT BRC DAwHUKVXYNQGO &mΩ % MW@∠'
    w = string_width(chars, fontsize=12, font='Times')
    assert w > 0


def test_string_width_fontsize_scaling():
    ''' Larger font produces wider string '''
    w12 = string_width('Hello', fontsize=12)
    w24 = string_width('Hello', fontsize=24)
    assert abs(w24 - w12 * 2) < 0.01


# --- text_approx_size tests ---

def test_text_approx_size_single_line():
    ''' Single line text size '''
    w, h, descent = text_approx_size('Hello', font='Arial', size=16)
    assert w > 0
    assert h == 16
    assert descent == 0


def test_text_approx_size_multiline():
    ''' Multiline text height '''
    w, h, descent = text_approx_size('Line1\nLine2\nLine3', font='Arial', size=16)
    assert h == 48  # 3 lines * 16


def test_text_approx_size_with_math():
    ''' Text with math expressions '''
    w, h, _ = text_approx_size('$x^{2}$ + 1', font='Arial', size=16)
    assert w > 0


# --- text_tosvg tests ---

def test_text_tosvg_basic():
    ''' Basic text to SVG element '''
    elm = text_tosvg('Hello', x=10, y=20, font='Arial', size=14)
    assert elm.tag == 'text'
    assert elm.get('fill') == 'black'


def test_text_tosvg_alignment_left():
    ''' Left-aligned text '''
    elm = text_tosvg('Test', x=10, y=20, halign='left')
    assert elm.get('text-anchor') == 'start'


def test_text_tosvg_alignment_right():
    ''' Right-aligned text '''
    elm = text_tosvg('Test', x=10, y=20, halign='right')
    assert elm.get('text-anchor') == 'end'


def test_text_tosvg_alignment_center():
    ''' Center-aligned text '''
    elm = text_tosvg('Test', x=10, y=20, halign='center')
    assert elm.get('text-anchor') == 'middle'


def test_text_tosvg_valign_top():
    ''' Top vertical alignment '''
    elm = text_tosvg('Test', x=10, y=20, valign='top')
    assert elm.get('dominant-baseline') == 'hanging'


def test_text_tosvg_valign_center():
    ''' Center vertical alignment '''
    elm = text_tosvg('Test', x=10, y=20, valign='center')
    assert elm.get('dominant-baseline') == 'central'


def test_text_tosvg_valign_bottom():
    ''' Bottom vertical alignment '''
    elm = text_tosvg('Test', x=10, y=20, valign='bottom')
    assert elm.get('dominant-baseline') == 'ideographic'


def test_text_tosvg_valign_base():
    ''' Base vertical alignment '''
    elm = text_tosvg('Test', x=10, y=20, valign='base')
    assert elm.get('dominant-baseline') == 'alphabetic'


def test_text_tosvg_rotation_anchor():
    ''' Rotation with anchor mode '''
    elm = text_tosvg('Test', x=10, y=20, rotation=45, rotation_mode='anchor')
    assert 'rotate' in (elm.get('transform') or '')


def test_text_tosvg_rotation_default():
    ''' Rotation with default mode adds translate '''
    elm = text_tosvg('Test', x=10, y=20, rotation=45, rotation_mode='default')
    xform = elm.get('transform') or ''
    assert 'translate' in xform
    assert 'rotate' in xform


def test_text_tosvg_color():
    ''' Text with custom color '''
    elm = text_tosvg('Test', x=10, y=20, color='red')
    assert elm.get('fill') == 'red'


def test_text_tosvg_decoration():
    ''' Text with decoration '''
    elm = text_tosvg('Test', x=10, y=20, decoration='underline')
    assert elm.get('text-decoration') == 'underline'


def test_text_tosvg_href():
    ''' Text with hyperlink wraps in <a> tag '''
    elm = text_tosvg('Click', x=10, y=20, href='https://example.com')
    assert elm.tag == 'a'
    assert elm.get('href') == 'https://example.com'


def test_text_tosvg_testmode():
    ''' Test mode adds debug markers '''
    elm = text_tosvg('Test', x=10, y=20, testmode=True)
    assert elm.tag == 'g'
    tags = [child.tag for child in elm]
    assert 'circle' in tags
    assert 'rect' in tags


def test_text_tosvg_multiline():
    ''' Multiline text creates multiple tspan elements '''
    elm = text_tosvg('Line1\nLine2', x=10, y=20)
    tspans = elm.findall('tspan')
    assert len(tspans) == 2


def test_text_tosvg_no_rotation():
    ''' No rotation means no transform attribute '''
    elm = text_tosvg('Test', x=10, y=20, rotation=0)
    assert elm.get('transform') is None


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
