# Environements
- The **Production** code, developed in **Rust**, is in the `./src/` directory      
- The **Development** and **Simulation** code, developed in **Python**, is in the `./dev/` directory        
It use the production Leg class, built with [PyO3](https://github.com/PyO3/pyo3), to have a Python library thanks to [maturin](https://github.com/PyO3/maturin).     

# Rust Setup
Install Rust with [rustup](https://rustup.rs/).     

Install the cross-compilation toolchain for the raspberry pi:    
```bash
cargo install cross
```     

Build the project, here, like this:    
```bash
cargo build
```

# Python Setup
For this project I use python 3.10 in a virtual environement with `pyenv`.

## Setup python environment
First of all, create an run a virtual environment:    
```bash
pyenv virtualenv 3.10.0 robot
pyenv activate robot
```
Then, install the requirements:      
``` bash
pip install -r ./dev/requirements.txt
```
After that, you can create the python library with `maturin`:   
*(Rust code must be built before)*    
```bash
maturin develop
```
Now, you can run Python codes in the `dev` directory.
```bash
cd dev
python test.py
```

# Deploy on the robot (raspberry pi)
Install Cargo (on Linux and macOS systems)   
``` bash
curl https://sh.rustup.rs -sSf | sh
```

Build the rust code in your computer:
``` bash
docker build -t crossbuild:local .
cross build --target=armv7-unknown-linux-gnueabihf
```

Make sure you can do ssh connection with the raspberry pi and get the IP address of the raspberry pi.   

Copy the binary file `./target/armv7-unknown-linux-gnueabihf/debug/leg_controller` and the parameters file `params.json` to the raspberry pi with the `scp` command.     
``` bash
scp ./target/armv7-unknown-linux-gnueabihf/debug/leg_controller user@raspberrypi.local:leg_controller
scp ./params.json user@raspberrypi.local:params.json
```

# Upgrade th firmware of an ODrive 3.6 controller

1. Download your firmware from the [ODrive website](https://docs.odriverobotics.com/releases/firmware) or from the [ODrive Github](https://github.com/odriverobotics/ODrive/releases).

2. Convert the firmware to a binary file:
``` bash
sudo apt install binutils-arm-none-eabi
arm-none-eabi-objcopy -O binary file.elf file.bin
```
3. Switch to the `DFU` mode. (With the little switch on the ODrive board, near the USB port)

4. Install the `dfu-util` tool:
``` bash
sudo apt install dfu-util
```

5. Plug the ODrive to the computer, with USB cable. But don't power the ODrive with the power supply.

6. Flash the firmware:
``` bash
dfu-util -v -w -R -a 0 -d 0483:df11 -s 0x08000000:leave -D file.bin
```

7. Switch on the ODrive power supply.   
Wait for the firmware to be flashed.

8. At the end, turn off the ODrive power supply and switch back to the `RUN` mode.