# AutoDectVuln

## Getting Started

- docker

  ```sh
  # run docker container in background
  sudo docker compose up -d

  # stop docker container
  sudo docker compose stop

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

- change working directory to web

  ```sh
  cd lib/web
  ```

- setup database (sqlite3) **first time only**

  ```sh
  python3 app/database/init_db.py
  ```

- run web

  ```sh
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
  - [x] use_after_free
  - [x] heap_over_flow
  - [x] double_free

- Testing

  - [x] Organize test sample
  - [x] Testing

- Report File

  - [x] Report File function

- Demo
  - [x] Demo
