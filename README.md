# AutoDectVuln

## Getting Started

- Ubuntu 20.04
    ```
    ./install.sh
    ```

- Docker
    ```sh
    sudo docker build -t <tag name> .

    # run 
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
    sudo docker run -it autodetectvul /bin/bash
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
