import pytest


def test_pancake_user(host):
    user = host.user('pancake')
    
    assert user.group == 'users'
    assert 'pancake' in user.groups
    assert user.home == '/var/lib/pancake'

@pytest.mark.parametrize('name', [
    ('apache2'),
    ('python3-Flask'),
    ('apache2-mod_wsgi-python3'),
    ('git')
])
def test_required_packages(host, name):
    assert host.package(name).is_installed


def test_apache2_service(host):
    srv = host.service('apache2')

    assert srv.is_running
    assert srv.is_enabled


@pytest.mark.parametrize('name', [
    ('/var/lib/pancake/wsgi.py'),
    ('/etc/apache2/vhosts.d/pancake.conf'),
    ('/var/lib/pancake/pancakes.json')
])
def test_pancake_config_files(host, name):
    wsgi = host.file(name)

    assert wsgi.exists
    assert wsgi.is_file
    assert wsgi.user == 'pancake'
    assert wsgi.group == 'pancake'
    assert oct(wsgi.mode) == '0o644'


def test_pancake_repo(host):
    wsgi = host.file('/home/ec2-user/projects/pancake')

    assert wsgi.exists
    assert wsgi.is_directory
    assert wsgi.user == 'ec2-user'
    assert wsgi.group == 'users'
    assert oct(wsgi.mode) == '0o755'


def test_instance_os_name(get_release_value):
    name = get_release_value('PRETTY_NAME')
    assert name == 'openSUSE Leap 15.1'


def test_pancake_app_get_types(host):
    cmd = host.run('curl http://localhost:5000/pancakes/')

    assert cmd.rc == 0
    assert 'banana' in cmd.stdout
    assert 'plain' in cmd.stdout


def test_pancake_app_get_type(host):
    cmd = host.run('curl http://localhost:5000/pancakes/banana')

    assert cmd.rc == 0
    assert 'banana' in cmd.stdout
    assert 'walnuts' in cmd.stdout


def test_pancake_app_add_delete_type(host):
    # Add fake pancake type with no ingredients
    cmd = host.run(
        'curl -H "Content-Type: application/json" '
        '-d \'{"name": "fake", "ingredients": []}\' '
        'http://localhost:5000/pancakes/'
    )

    assert cmd.rc == 0
    assert 'Pancake added' in cmd.stdout
    assert host.run('curl http://localhost:5000/pancakes/fake').rc == 0

    # Delete fake pancake type
    cmd = host.run(
        'curl -X DELETE curl http://localhost:5000/pancakes/fake'
    )
    assert cmd.rc == 0
    assert 'Pancake deleted' in cmd.stdout

    # Confirm fake type deleted
    out = host.run('curl http://localhost:5000/pancakes/fake').stdout
    assert 'Unable to retrieve pancake type' in out
