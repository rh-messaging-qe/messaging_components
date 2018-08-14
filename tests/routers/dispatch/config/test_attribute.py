from messaging_components.routers.dispatch.config import _Attribute


class TestBasic:
    attr_a = _Attribute(name='attr', value=1234)

    def test_1(self):
        assert self.attr_a.value == 1234
