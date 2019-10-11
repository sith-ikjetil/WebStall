# WebStall
An attempt at slow loris attack implementation in python.

```
Usage:
 WebStall.py [options]
 
 An attempt at slow loris HTTP attack
 
 Options:
  -h, --help                       display this help
  -a, --address             (1)    domain
  -d, --directory                  directory with HTTP request files
  -t, --threads             (2)    number of threads
  -s, --sleep                      HTTP request chars delay - in seconds
  -e, --extension           (3)    HTTP request file extension
  -r, --create-request      (4)    Creates default request files in directory
  -p, --template                   File that is used as template to -r, --create-request
  
  (1) Required field
  (2) Min: 1, Max: 999, Default: 1
  (3) Default is .txt
  (4) Creates -t number of default request files in -d directory with -e extension
```
**NB! THIS SOFTWARE HAS NO LICENSE!**
