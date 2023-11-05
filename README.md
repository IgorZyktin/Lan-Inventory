# Lan-Inventory

Simple script that scans machines in LAN. Was initially written because I
started to mess ip addresses of different machines in my home.

`config.json` example:

```json
{
  "subnet": "192.168.1",
  "known_hosts": {
    "b4:a5:ef:10:14:8c": "Router"
  }
}

```

Usage example:

```shell
python3 main.py
```

```shell
+---+-------------------+--------------+----------+---------+
| N |        MAC        |      IP      | Hostname | Comment |
+---+-------------------+--------------+----------+---------+
| 1 | b4:a5:ef:10:14:8c | 192.168.1.1  |          |  Router |
| 2 | 50:ff:20:53:a2:da | 192.168.1.65 |          |         |
| 3 | 00:11:32:f1:0a:39 | 192.168.1.66 |          |         |
| 4 | 28:87:ba:71:73:d6 | 192.168.1.68 |          |         |
| 5 | 78:02:f8:20:98:0a | 192.168.1.70 |          |         |
| 6 | 02:be:94:c8:ae:57 | 192.168.1.71 |          |         |
| 7 | 24:18:c6:12:8b:46 | 192.168.1.72 |          |         |
| 8 | 7c:c2:94:6f:5b:52 | 192.168.1.73 |          |         |
| 9 | 58:11:22:8a:f4:87 | 192.168.1.74 |          |         |
+---+-------------------+--------------+----------+---------+
```
