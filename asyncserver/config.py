KNOWN_SETTINGS = []


class SettingMeta(type):
    def __new__(cls, name, bases, attrs):
        # TODO check if config options is legal
        super_new = super(SettingMeta, cls).__new__
        new_class = super_new(cls, name, bases, attrs)

        if not name == "Setting":
            KNOWN_SETTINGS.append(new_class)
        return new_class


Setting = SettingMeta('Setting', (), {})


class BindHost(Setting):
    _name = "--host"
    default = "127.0.0.1"
    help = "bind host default: 127.0.0.1"


class BindPort(Setting):
    _name = "--port"
    default = 8000
    help = "bind port default: 8000"
