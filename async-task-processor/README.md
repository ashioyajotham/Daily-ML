# README.md

# Async Task Processor

Async Task Processor is a Python application designed to manage and execute tasks asynchronously. It provides a flexible framework that allows for the addition of various task types, making it suitable for a wide range of applications.

## Features

- Asynchronous task execution
- Dynamic task management
- Timer functionality to track execution time
- Modular design with separate components for core functionality, task definitions, and utility functions

## Installation

To install the required dependencies, run:

```
pip install -r requirements.txt
```

## Usage

To run the application, execute the following command:

```
python src/main.py
```

You can define your own tasks by creating classes that inherit from `BaseTask` in the `src/tasks/base.py` file.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.