
class _Attribute:
    def __init__(self, name, value, deprecated=False):
        self.name = name
        self.value = value
        self.deprecated = deprecated

    def get_config(self):
        """Get in config format"""
        return '    %s: %s\n' % (self.name, self.value) if self.value else None

    def __str__(self):
        return self.value

    # def __get__(self, instance, owner):
    #     return self

    def __set__(self, instance, value):
        self.value = value


class _Section:
    section_name = None
    deprecated = False

    # def get_config(self):
    #     sec = '%s: {\n' % self.section_name
    #     for x in self.__dict__.items():
    #         for value in x:
    #             if isinstance(value, _Attribute):
    #                 val = value.value
    #                 if val is not None:
    #                     sec += '    %s: %s\n' % (value.name, val)
    #     sec += '}'
    #     return sec

    def __str__(self):
        return self.get_config()

    def __getattribute__(self, name):
        value = object.__getattribute__(self, name)
        if hasattr(value, '__get__'):
            value = value.__get__(self, self.__class__)
        return value

    def __setattr__(self, name, value):
        try:
            obj = object.__getattribute__(self, name)
        except AttributeError:
            pass
        else:
            if hasattr(obj, '__set__'):
                return obj.__set__(self, value)
        return object.__setattr__(self, name, value)


class Config(list):
    """Qpid Dispatch configuration"""
    def __init__(self):
        super().__init__()

    def add_section(self, section: _Section):
        self.append(section)

    def get_config(self):
        conf = ''
        i = False
        num_sections = len(self)
        for section in self:
            i += 1
            conf += '%s: {\n' % section.section_name
            for attributes in section.__dict__.items():
                for attr in attributes:
                    if isinstance(attr, _Attribute):
                        tmp_val = attr.value
                        if tmp_val is not None:
                            conf += '    %s: %s\n' % (attr.name, tmp_val)
            conf += '}\n'
            if i < num_sections:
                conf += '\n'
        return conf
