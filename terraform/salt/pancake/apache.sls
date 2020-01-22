include:
  - pancake.user

apache2:
  pkg.latest:
    - refresh: True
  service.running:
    - enable: True
    - reload: True
    - watch:
      - pkg: apache2

apache2-mod_wsgi-python3:
  pkg.latest:
    - refresh: True
    - require:
      - pkg: apache2

/etc/apache2/vhosts.d:
  file.directory:
    - user: root
    - group: root
    - mode: 755
    - makedirs: True

/var/lib/pancake/wsgi.py:
  file.managed:
    - source: salt://pancake/files/wsgi.py
    - user: pancake
    - group: pancake
    - mode: 644
    - require:
      - sls: pancake.user

/etc/apache2/vhosts.d/pancake.conf:
  file.managed:
    - source: salt://pancake/files/pancake.conf
    - user: pancake
    - group: pancake
    - mode: 644
    - require:
      - file: /etc/apache2/vhosts.d
      - sls: pancake.user
