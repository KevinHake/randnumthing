# "Simple" Random Number Server in C++ with Python-Bokeh Gui Client 

Here is my version of a Client-Server according to the requirements of the coding challenge:
- Write a C++ program to generate a random number once per sec.
- Each new random number will be transmitted via websocket to a Python script
- The Python script uses the Bokeh Python GUI framework to create a very simple display (just a screen, with the number shown, continuously updating).


## Getting started

## Environment setup/build

0. This project was written for Linux - so start there.
1. First, clone the repository with submodules (required for uWebSockets library and dependencies):
`git clone --recurse-submodules <myrepo url>`
2. Python setup:
  2.1. To be sure, use Python 3.12, and an updated pip. It _should_ work down to Python version 3.10 (this version of Bokeh's limit), but I did not test other versions.
  2.2. I recommend installing/setting up a virtual environment for python. If you're already using something like conda or pyenv to make sure your Python version matches, just use that. If not, you can use the built in venv before installing dependencies:
```
python3 -m venv .venv
source .venv/bin/activate```
  2.3. Install websockets and Bokeh libraries, and the dependencies those bring:
`pip install -r requirements.txt`

3. C++ setup:
  3.1 Ensure you have a C and C++ compiler installed with modern C++ support (C++20 or newer), and a recent version of Make. For the record I used gcc 14.2.1 and GNU make 4.4.1.
  3.2 

## Running
Here's how to run the example once you've followed the previous steps:
1. Launch the C++ server:
`./server` <<<<<<<TODO>>>>>>>
2. Launch the Python GUI client with bokeh for updates:
`bokeh serve --show gui.py`

Joke versions I did not make:
- only use 1 randomly generated number rather than generating a new one each tick
- "just a sec" mode, where "1 sec" is a random time period between 30-300 seconds.


I hard coded port number and localhost instead of a config file/input args, but I'm not a feature creep.



Note submodule... maybe do automatic check of submodule init for new repo..?
I used uWebSockets, just because I was avoiding pulling in boost, and it seemed lightweight. Ask me how I feel about it.

To keep it as bare bones as possible, it's a non-secure connection (no TLS), and obviously no need for compression. So no need for OpenSSL or Zlib dependencies.



This is also why I send the number unwrapped, in binary. I decided on a 32-bit unsigned int to keep it simple (yeah, uchar would've been simpler:P).


This library has its own timer mechanism 

Rather than a simple "sleep 1" for delay, I wake at an absolute time to avoid drift. And tho it's probably negligible, I calculate the next random number while waiting so we send the next request as close to the target time as possible.

TODO? I implemented a signal handler to gracefully exit on SIGINT/SIGTERM because it drives me nuts when ports get tied up this way.
TODO: python client shuts down if serer closes connection/we stop receiving data.
TODO tag
TODO: add license and strings in my files.

If I were to do this again, I might try https://github.com/machinezone/IXWebSocket/tree/master/test instead. At a glance, the code and usage looks more readable and straightforward to understand.
uWebSockets library complaints:
- Examples are using such new features that gcc calls it "experimental"
- 
- The project goals seem more oriented towards a consulting honeypot than an easy-to-use websockets library.
- It's a bit messy, and this pretty basic use case requires poking holes in their abstraction. E.g. defining a periodic timer is a bit clunky. It might be nicer to access the listen socket and open websockets from one context, rather than squirreling this away in custom structs and global variables.
- The license strings are confusing... it's "Apache 2.0" but I'm not sure they're even applying the simple Apache 2.0 terms.
- The build files for the examples are strange
