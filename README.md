# sylas-angle

It can be hard to tell when its a good or bad idea to pick Sylas, since he is so dependent on enemy ultimates.

This tool connects to the LCU API, waits for champ select, gets enemy champs, and then checks if they have good ultimates for Sylas.

# requirements

Currently this tool uses [lcu-driver](https://github.com/sousa-andre/lcu-driver) to connect to the LCU API and manage websocket stuff.

`pip install lcu-driver`

Currently this tool is only written for Windows, though minimal change would be needed to get this running on other OS.

# TODO

lcu-driver is built around decorators that are pretty annoying to use inside of a class. This encourages a really gross dependence on global state when coding quickly.

At some point I plan to move to [Willump](https://github.com/elliejs/Willump), which appears much cleaner to use inside of a class.

If the easiest way to use a tool is not safe, and the safest way to use a tool is not easy, then the tool should be replaced.
