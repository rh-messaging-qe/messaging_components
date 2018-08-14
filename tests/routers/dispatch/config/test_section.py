from messaging_components.routers.dispatch.config import _Section, _Attribute


class TeSection(_Section):
    """
    Section for testing purpose
    """
    section_name = 'TeSection'
    used_by = ['a', 'b']

    def __init__(self, a=None, b=1234, c=None, d='ABCD'):
        self.a = _Attribute(name='a', value=a)
        self.b = _Attribute(name='b', value=b)
        self.c = _Attribute(name='c', value=c)
        self.d = _Attribute(name='d', value=d)


class Test1:
    section = TeSection()

    def test_a(self):
        assert self.section.a.value is None
        assert self.section.b.value == 1234
        assert self.section.d.value == 'ABCD'

    def test_b(self):
        assert self.section.a.value is None

    def test_c(self):
        section = TeSection()
        section.a = 0
        assert section.a.value == 0
