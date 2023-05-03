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

## Web

```sh
# need to install flask and flask_session
cd lib/web
cp app/configs/config.py.template app/configs/config.py
# edit app/configs/config.py
# change SECRET_KEY value (openssl rand -base64 32)
python3 web.py
```

## Goals

- Binary Arch

  - Arch: amd64/x86-64
  - File: ELF 

- Protection

  - **RELRO**: Full RELRO
  - **Stack**: Canary found
  - **NX**: NX enabled
  - **PIE**: PIE enabled
  - **FCF**: None

- Vulnerability

  - [x] stack_over_flow
  - [x] format_string_bug
  - [ ] use_after_free
  - [ ] heap_over_flow
  - [ ] double_free

- Testing

  - [ ] Organize test sample
  - [ ] Testing

- Report File

  - [x] Report File function

- Demo
  - [ ] Demo
