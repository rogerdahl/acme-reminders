# ACME Notifications

## Start on boot

Set service up to start on boot. 

```
$ sudo bash -c '
  cd config
  rsync *.service /etc/systemd/system
  rsync emperor.ini /etc/uwsgi
  rsync acme-notifications.ini /etc/uwsgi/vassals
  systemctl enable emperor.uwsgi.service
  systemctl start  emperor.uwsgi.service
'
```

Initialize the db

    $ sqlite3 db.sqlite < schema.sql

