# AirBnB clone - The console
![Latest commit](https://img.shields.io/github/last-commit/EskiasYilma/AirBnB_clone?style=round-square)

---
![](https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/medias/2018/6/65f4a1dd9c51265f49d0.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARDDGGGOUSBVO6H7D%2F20230306%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230306T142614Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=87ce82fe3c547da81afb6b56e07e2f04c034368f739ed54126e3f787be7a448d)
---

## Background Context

Write a command interpreter to manage your AirBnB objects.

## Execution
### Interactive mode:
```
$ ./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  help  quit

(hbnb)
(hbnb)
(hbnb) quit
$
```

### Non-Interactive mode:
```
$ echo "help" | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb)
$
$ cat test_help
help
$
$ cat test_help | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb)
$
```
