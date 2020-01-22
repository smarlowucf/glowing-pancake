import pytest


@pytest.fixture()
def get_release_value(host):
    def f(key):
        release = host.file('/etc/os-release')
        value = None
        key += '='

        for line in release.content_string.split('\n'):
            if line.startswith(key):
                value = line[len(key):].replace('"', '').replace("'", '')
                value = value.strip()
                break

        return value
    return f
