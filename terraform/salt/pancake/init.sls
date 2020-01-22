include:
  - pancake.user

/home/ec2-user/projects/pancake:
  file.directory:
    - user: ec2-user
    - group: users
    - mode: 755
    - makedirs: True

git package is installed:
  pkg.installed:
    - name: git

python3-Flask installed:
  pkg.installed:
    - name: python3-Flask

pancake-code:
  git.latest:
    - name: https://github.com/smarlowucf/glowing-pancake.git
    - target: /home/ec2-user/projects/pancake/
    - user: ec2-user
    - branch: master
    - require:
      - pkg: git
      - pkg: python3-Flask

pancake-dev:
  cmd.run:
    - name: sudo python3 setup.py develop
    - cwd: /home/ec2-user/projects/pancake
    - require:
      - git: pancake-code

/var/lib/pancake/pancakes.json:
  file.managed:
    - source: salt://pancake/files/pancakes.json
    - user: pancake
    - group: pancake
    - mode: 644
    - require:
      - sls: pancake.user
