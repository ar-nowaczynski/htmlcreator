from htmlcreator.css import CSS


def test_CSS():
    css = CSS()
    strcss = str(css)
    assert isinstance(strcss, str)
    assert strcss.startswith('body')
    assert 'table' in strcss


if __name__ == '__main__':
    test_CSS()
