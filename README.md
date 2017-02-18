# interminal

`interminal` is a utility for running commands in an interactive shell session
in a graphical terminal emulator. It is for Linux only.

## Installation

to install `interminal`, run:

```
$ pip3 install interminal
```

or to install from source:

```
$ python3 setup.py install
```

## Introduction

`interminal` is mostly useful for things like making an external tool for your
text editor, or making a launcher for a terminal program, or things like that.
For example, You might want to run the command `python3 my_script.py` whenever
you press a certain keyboard shortcut in your text editor whilst you've got
the file `my_script.py` open. It's easy to make an extension to do this in,
for example, Sublime Text 3, but the output will be shown in a panel at the
bottom of Sublime's GUI. Sublime's GUI is not a terminal emulator, it does not
give you the power to re-run the command with different arguments, inspect
output files, etc. Sometimes what you really want is for your favourite
terminal emulator to be a keystroke away.

You'd think that would be easy, right? All terminal emulators have command
line options for telling them what command to run — can't we just use those?
Unfortunately it's not that simple. The following command:

```
$ gnome-terminal -x python3 my_script.py
```

Has a few problems. One, it closes the terminal as soon as the command exits,
preventing you from seeing its output. Secondly, the script is not run from
within a shell, meaning any environment variables you've set in your `.bashrc'
or similar may not be available. If you want your commands to be run in a
'normal' environment, you need to run a shell in the terminal first, and tell
the shell to run your command. Then you have to start another shell to ensure
the terminal emulator stays open:

```
$ gnome-terminal -x bash -c "python3 my_script.py; bash"
```

This is almost good enough. It doesn't add the command to your shell history,
but it's basically what we want. But if you need to escape some characters in
your command, you are two-layers deeo in "passing commands to other commands"
— the quoting is going to get out of control fast. And for reasons I can't
grasp, I can't get the above to work with some terminal emulators.

Ideally we want something that will work with the minimum quoting, and that
emulates exactly what would happen if you typed something into a terminal
yourself. That's where `interminal` comes in.



## Usage

To run a command such as `echo hello` in a terminal emulator, run the command:

```
$ interminal echo hello
```

This will launch a new terminal emulator, run the command `echo hello`, and
then leave you at an interactive prompt, with the command `echo hello` in your
shell history, exactly as if you had launched the terminal emulator and typed
it yourself. In fact, `interminal` works by injecting the command into the
input of a pseudoterminal connected to your shell, and so as far as that shell
is concerned, you *did* type it in. In this way, `interminal` can respect
whatever crazy hacks you have decided to apply to your shell — by just typing
things into a terminal the same as a human would.

If you have something more complex, you can instead do:

```
$ interminal --script 'du -hs $HOME/* | sort -hr; echo hello'
```

This allows you to include things that will be interpreted by the shell in the
launched terminal emulator (but not by the shell, if any, from which you are
executing the above command).



## Notes

Which terminal emulator to launch is guessed based on the `XDG_DESKTOP`
environment variable — the default terminal emulator for the desktop
environment is used. If you want to use a different one, you can call
interminal like this, using the terminology terminal emulator as an example:

```
$ terminology -e inshell --script 'du -hs $HOME/* | sort -hr; echo hello'
```

interminal is actually just a very short script that replaces its own process
with the terminal emulator running the `inshell` script, which also part of
this package. So you can call `inshell` yourself as above to control which
terminal to launch. If this sounds like it defeats the purpose of this
project, it doesn't — inserting the command into a shell that otherwise
behaves like an ordinary interactive shell is the tricky bit.


If you are running the `interminal` command from a shell, then you must make
sure that its arguments, *after being interpreted by that shell* are what you
want to run in the interactive shell that is started in the terminal emulator.
For example, if you run:

```
$ interminal echo $PATH
```

then `$PATH` will be expanded *prior* to `interminal` being called. This might
be undesirable if, for example, the shell you are running `interminal` from is
`/bin/sh`, and your `$SHELL` environment variable (which is what `interminal`
will run) is /bin/bash. The current shell won't have run your `.bashrc` and so
might not have any additions you have made there to your `$PATH` variable. So
as a general rule, in these cases you should do:

```
$ interminal --script 'echo $PATH'
```

Of course if you want to have single quotes in your command, the required
escape sequences can get unwieldy:

```
$ interminal --script 'echo $PATH > '"'"'my file with spaces'"'"''
```

(this will run `echo $PATH > 'my file with spaces'`)

Hopefully, you are using `interminal` from an environment that lets you pass
in command line arguments that are not interpreted by a shell, but instead
are passed directly to the `exec()` system call, in which case the above
quoting is unnecessary. For example, in Python, this is fine:

```python
import subprocess
subprocess.Popen(["interminal", "--script", "echo $PATH > 'my file with spaces'"])
```

In fact, you have an arbitrarily long multi-line shell script as that final
argument, it will be executed as-is.

But if you have to pass something to a shell, and you don't know in advance
what the arguments are, you should try to quote them programatically to ensure
you get the quoting right:

```python
import pipes
import os

# This works too, if you can't avoid having to go through a shell:
args = ["interminal", "--script", "echo $PATH > 'my file with spaces'"]
command = ' '.join(pipes.quote(arg) for arg in args)

# Then pass the single command to whatever shell will interpret it:
os.system(command)
```
