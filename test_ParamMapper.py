import ParamMapper

pm = ParamMapper.ParamMapper()

def test_params():
    param_strs = [
        'id=6 title=This is a title. The end.',
        '',
        'just text without param',
        'just text with param=42',
    ]

    expected = [
        {'id':'6', 'title': 'This is a title. The end.'},
        {},
        {'none': 'just text without param'},
        {'none': 'just text with', 'param': '42'},
    ]

    for i, arg_str in enumerate(param_strs):
        result = pm.parse(arg_str)
        assert result == expected[i]