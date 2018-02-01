# canpi

### Features
- Recieve data from components
  - Filtering the messages
    - how many messages do we want to read every second
    - make sure they're actually getting interpreted
  - Query Devices that do not send messages by default
  - C-module interpret data (==look into this, does it go from c -> python?==)
    - SmartRoute
      - input current energy
      - Variables/factors that could slow us down or speed us up
      - where is the car in relation route
        - GPS
        - Checkpoints to reference current route vs predicted route, and adjust accordingly
- send data to DashU
- send data to ChaseUI
  - Direct-connect to DashUI/Car (WAP to WAP)
- Log CAN messages (timestamp, arb. Id, data) [function, process]
  - **Note:** performance concerns with reading *and* writing to SD card at the same time
  - Sampling messages
  - catching premature shutdown of device
  - write both log to scv and log to pkl
  - what is the purpose of logging?
    - post-race data analytics
    - think blackbox
- Send data for InfotainUI


### // TODO:

- setup CAN simulator to work (Andrew)
  - create connector
  - look up OBD-II pin layout
  - Hardwiring it with CAN HI/LO
- UML Diagrams
- boot-script (Andrew)
  - canpi stuff
  - reverse tunneling
- Setup environment for testing stuff easily
- Move interface setup to /etc/networking and out of program
