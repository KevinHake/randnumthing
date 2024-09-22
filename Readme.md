# Random Number Server in C++ with Python-Bokeh Gui Client 

Here is my version of a Client-Server according to the requirements of the coding challenge:
- Write a C++ program to generate a random number once per sec.
- Each new random number will be transmitted via websocket to a Python script
- The Python script uses the Bokeh Python GUI framework to create a very simple display (just a screen, with the number shown, continuously updating).

## Environment setup/build

0. I wrote this for Linux - so start there. I'm running Manjaro (Arch-based), so my versions of things might be annoyingly recent, but I bet it will work fine on any modern Linux with slightly older packages too.
1. First, clone the repository with submodules (required for uWebSockets library and dependencies):
   ```
   mkdir <repo dir name>; cd <repo dir name>
   git clone --recurse-submodules <this repo's url> .
   ```
2. Python setup:
   - To be sure, use Python 3.12, and an updated pip. It _should_ work down to Python version 3.10 (this version of Bokeh's limit), but I did not test other versions.
   - I recommend installing/setting up a virtual environment for python. If you're already using something like conda or pyenv, just use that. If not, you can use the built in venv before installing dependencies:
     ```
     cd <path/to/repo>
     python3 -m venv .venv
     source .venv/bin/activate
     ```

   - Install websockets and Bokeh libraries, and the dependencies those bring:
     ```
     pip install -r requirements.txt
     ```

3. C++ setup/build:
   - Ensure you have a C and C++ compiler installed with modern C++ support (C++17 or newer). For the record I used gcc 14.2.1 and GNU make 4.4.1.
   - Run `./build.sh` from the root of the repository (it's written for bash). This just calls gcc in a couple of one-liners, and outputs the executable "server" to the same directory.

## Running
Here's how to run the example once you've followed the previous steps:
1. Launch the C++ server:
`./server`
2. Launch the Python GUI:
`python gui.py`

Both C++ server and python scripts log the random number to stdout for easy verification they are in sync.
The gui should launch automatically in a browser window.

## Implementation Notes
I hard coded port number and localhost for both the C++ and python. No config file or input params.

It uses non-secure websocket connections (no TLS).

### Python
It's a little hokey but gui.py is using a separate websocket connection with the C++ server to grab the raw random numbers. It runs a Bokeh server (with its own, independent websocket protocol that I didn't feel like implementing in C++) to display the number on a plot in a browser window.

### C++
The random number is generated each second from whatever the system has available (std::random_device). I don't use a pseudo-random number generator because I figure the system RNG can handle 1 Hz (tho who knows if the system RNG isn't pseudorandom).

I send the number as a 32-bit unsigned int. Would've been simpler to limit this to uchar, but as it is I have the python script hard-coded to interpret the number as little-endian (which is how the C++ sends it on my machine).

I used the uWebSockets library because I was avoiding pulling in boost, and it seemed lightweight. 
I use its special timer mechanism instead of launching my own periodically firing thread... it seems to schedule things right.
The design of this library feels like a consultation honeypot rather than easy to use. They go wild with templates and a builder pattern that make it hard to debug. [IXWebSocket](github.com/machinezone/IXWebSocket/) API looks easier to use without needing to know the internals.
