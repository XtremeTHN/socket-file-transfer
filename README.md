# Unsecure Socket Data Transfer

An unsecure data transfer (USDT) written in python, this program has the ability for executing os commands or python commands in the server.

### How to use it
You can use this program in three ways, hosting a server, connecting to a server, or activating shell mode.

##### Hosting a server
To host a socket server with this program you need to run USDT like this:
```batch
python3 .\main.py -cs
```
There are two features you can activate by passing the argument `--allow-shell` or `--allow-multi-connection` to the program.
```batch
python3 .\main.py -cs --allow-shell --allow-multi-connection
```
The `--allow-shell` argument will allow the client to execute python, os commands in the server.

And the `--allow-multi-connection` argument will execute a connection scanner in another thread to accept more than one connection (maybe cause some errors).

Also you can host the server by executing the program with the shell argument and typing `server start` and the arguments mentioned above.

In any way you start the server, it will print the address where the server is hosted

##### Connecting to a server
To connect to a server you can run the program like this:
```batch
python3 .\main.py -c [ip]
```
This command will connect to a server and exit, to send data or a file you need to provide the `--data` or the `--file` argument:
```batch
python3 .\main.py -c [ip] --file .\TestFile.zip
```
```batch
python3 .\main.py -c [ip] --data "Hello World"
```

The recommended way to connect into a server is using the `--shell` argument, and typing `client connect [ip]`

```batch
python3 .\main.py -s
```
```
>>> client connect [ip]
```
Then you can send data, files, os commands and python commands:
```
>>> client send "Hello World"
>>> client send ".\TestFile.zip"
```

##### Executing commands in the server
If you execute the `client execute [python] [os]` it will show you a command line (the shell will change depending of your operating system) for executing commands (with syntax highlighting, thanks pygments and python-prompt-toolkit):

###### Windows
```
>>> client execute os
Posh> echo "Hello World"
Hello World

>
```
###### Linux
```
>>> client execute os
Bash> echo "Hello World"
Hello World

>
```
Note that this executor its still in development and may be unstable

### Known bugs

- In the os command execution if the command output its too large, the recv method of the client socket will failed and recieve part of the output instead of the buffer size
- In the python command execution the variables will not be saved, and the commands need to be wrapped in one line
- In some ocassions the thread of the connection scanner will frezee, and you will not be able to close it with any of the commands (`client poweroff` or the `--shutdown` argument) (killing the terminal its the best solution)