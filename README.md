# AutoDectVuln

## Getting Started

- Dockerfile
    ```sh
    sudo docker build -t <tag name> .
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
