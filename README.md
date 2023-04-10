# AutoDectVuln

## Getting Started

- Ubuntu 20.04
    ```
    ./install.sh
    ```

- Dockerfile
    ```sh
    # build
    sudo docker build -t <tag name> .

    # run (option) 
    sudo docker run <tag name>

    # run with interactive interface
    sudo docker run -it --rm <tag name> /bin/bash

    # install
    ./install.sh
    ```
or

- docker-compose.yml
    ```sh
    # up
    docker-compose up 

    # run with interactive interface
    sudo docker run -it autodetectvuln /bin/bash
    ```

## Sample Testing

- make sample
    ```sh
    make
    ```
- clean sample
    ```sh
    make clean
    ```
- Test sample file 
    ```sh
    python main.py ./path/to/binary -m module -s ./path/to/save -t limit_time
    ```
## Goals

- Protection
    - RELRO: Full RELRO
    - Stack: No canary found
    - NX:    NX enabled
    - PIE:   PIE enabled
    - FCF:   None

- Vulnerability
    - [x] stack_over_flow
    - [x] format_string_bug
    - [ ] use_after_free
    - [ ] heap_over_flow 
    - [ ] *double_free

- Report File
    - [ ] Report File function

- Demo
    - [ ] Demo
    
