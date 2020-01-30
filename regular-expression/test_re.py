import re

def test_string_replace():
    content = "0123456789"
    assert content[3:5] == "34"

    assert "_123456789"==content.replace("0", "_", 100)
    #content[3:5] = "a"
    #assert content == "012a56789"

def test_re_sub():
    input = "abcdefghi"
    assert "[def]" == re.sub('abc(def)ghi', r'[\1]', input)
    assert "[12345]" == re.sub(r'_(.*)_', r'[\1]', "_12345_")

def test_re_sub2():
    content = "Utils.createLine((double[]) [50, 0, 100, 0, 100, 0]), 172)]"
    p = re.compile(r'\(double\[\]\) \[([\s|\d|,]*)\]')
    assert "Utils.createLine(new double[]{50, 0, 100, 0, 100, 0}), 172)]" == p.sub(r'new double[]{\1}', content)

def test_re_subn():
    input = """
        _a_
        _b_
        _c_
    """
    p = r'_(.*)_'
    r = r'[\1]'

    # replace underbar to blacket
    result = re.subn(p, r, input)
    assert """
        [a]
        [b]
        [c]
    """ == result[0]
    assert 3 == result[1], "check count"

def test_re_remove_last_comma_in_array():
    p = re.compile(r'\[(.*),(\s)*\]')
    r = r'[\1]'
    assert "[a,b,c]" == p.sub(r, "[a,b,c,]")
    assert "[a,b,c]" == p.sub(r, "[a,b,c,\n]")
    assert "[a,b,c]" == p.sub(r, "[a,b,c,\t]")
    assert "[ a,b,c]" == p.sub(r, "[ a,b,c, \n    ]")

def test_re_change_array_to_list():
    p = re.compile(r'\[(.*)]')
    r = r'Arrays.asList(\1)'
    assert "Arrays.asList(1l)" == p.sub(r, "[1l]")
    assert "Arrays.asList(1l,2l)" == p.sub(r, "[1l,2l]")
    assert "Arrays.asList()" == p.sub(r, "[]")

def test_re_append_semicolon_on_import():
    p = re.compile(r'^import (.*)[\n|\r]')
    r = r'import \1;'+'\n'
    assert "import a;\n" == p.sub(r, "import a\n")
    assert "import a;\n" == p.sub(r, "import a\r")
    assert "import com.kakao.mapmatch.ComplexPoint;\n" == p.sub(r, "import com.kakao.mapmatch.ComplexPoint\n")

    # don't support multi line
    #assert "import a;\nimport b;\n" == p.subn(r, "import a\nimport b\n")[0]

def test_re_append_parentheses():
    p = re.compile(r'assertEquals (.*), (.*)')
    r = r'assertEquals(\1, \2);'
    assert "assertEquals(a, b);" == p.sub(r, "assertEquals a, b")
    assert "assertEquals(6, target.approximate(new NetworkRange(900, [1l, 10l, 11l], 100)), DELTA);" == p.sub(r, "assertEquals 6, target.approximate(new NetworkRange(900, [1l, 10l, 11l], 100)), DELTA")
