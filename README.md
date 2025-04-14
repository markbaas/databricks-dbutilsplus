# Databricks DBUtils Plus

Databricks DBUtils Plus is a Python library that extends the functionality of the Databricks SDK by providing an enhanced interface for managing widgets and accessing workspace utilities.

## Installation

To install the library, you can use Poetry. First, ensure you have Poetry installed, then run:

```bash
pip install git+https://github.com/markbaas/databricks-dbutilsplus
```

## Usage

To use the library, you can import the `dbutils` object from the package:

```python
from dbutilsplus import dbutils
```

In order to use this library by default add this to your vscode user config:

```json
    "jupyter.runStartupCommands": [
        "from dbutilsplus import dbutils"
    ]
```

In order to specify widget values, you have to create a .params.json file at the same level as your notebook. For example:

```json
{
    "param1": "default development value"
}
```

### Widgets Management

The `Widgets` class allows you to manage widget parameters easily. You can refresh parameters and retrieve widget values using the following methods:

- `getAll()`: Retrieves all widget values after refreshing parameters.
- `getArgument(*args, **kwargs)`: Retrieves a specific argument from the widgets.
- `get(*args, **kwargs)`: Retrieves a widget after refreshing parameters.

### Accessing Workspace Utilities

The `DbUtils` class provides access to various utilities in the Databricks workspace. You can access the underlying `WorkspaceClient`'s dbutils by using the `dbutils` object.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.