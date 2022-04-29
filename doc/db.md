videos:

```
+----------+--------------+------+-----+---------+----------------+
| Field    | Type         | Null | Key | Default | Extra          |
+----------+--------------+------+-----+---------+----------------+
| id       | int          | NO   | PRI | NULL    | auto_increment |
| bvid     | varchar(32)  | YES  |     | NULL    |                |
| aid      | int          | YES  |     | NULL    |                |
| pic      | varchar(128) | YES  |     | NULL    |                |
| title    | varchar(128) | YES  |     | NULL    |                |
| pubdate  | int          | YES  |     | NULL    |                |
| desc     | varchar(256) | YES  |     | NULL    |                |
| owner    | int          | YES  |     | NULL    |                |
| view     | int          | YES  |     | NULL    |                |
| danmaku  | int          | YES  |     | NULL    |                |
| reply    | int          | YES  |     | NULL    |                |
| favorite | int          | YES  |     | NULL    |                |
| coin     | int          | YES  |     | NULL    |                |
| share    | int          | YES  |     | NULL    |                |
| like     | int          | YES  |     | NULL    |                |
+----------+--------------+------+-----+---------+----------------+
```

replies:

```
+---------+---------------+------+-----+---------+----------------+
| Field   | Type          | Null | Key | Default | Extra          |
+---------+---------------+------+-----+---------+----------------+
| id      | int           | NO   | PRI | NULL    | auto_increment |
| rpid    | bigint        | YES  |     | NULL    |                |
| oid     | bigint        | YES  |     | NULL    |                |
| mid     | int           | YES  |     | NULL    |                |
| root    | int           | YES  |     | NULL    |                |
| dialog  | int           | YES  |     | NULL    |                |
| rcount  | int           | YES  |     | NULL    |                |
| ctime   | int           | YES  |     | NULL    |                |
| like    | int           | YES  |     | NULL    |                |
| uname   | varchar(128)  | YES  |     | NULL    |                |
| content | varchar(1024) | YES  |     | NULL    |                |
+---------+---------------+------+-----+---------+----------------+
```

