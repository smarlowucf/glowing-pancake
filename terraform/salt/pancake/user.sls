pancake-group:
  group.present:
    - name: pancake

pancake-user:
  user.present:
    - name: pancake
    - fullname: Pancake App User
    - home: /var/lib/pancake
    - groups:
      - pancake
    - require:
      - group: pancake
  group.present: []
