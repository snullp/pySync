# pySync
## A quick data depository synchonizer
This is a file synchonizer written in python, intentially to compare and sync two folder with big and static files.

It has following features:

* Don't rely on inode, so it is compatiable to NTFS.
* Designed for big and static files, it only check file's size and mtime for identification. For the same reason, it uses copy rather than rsync.
* Fully controllable operation.

TODO:

* Add folder tier support.
* Add fingerprint for the folder, which can help determine new files and misc information.
* Add sync script support.
