from IPython import get_ipython
import nbformat
import re

def get_notebook_dev_params():
    ipython = get_ipython()
    # Use the global variable __vsc_ipynb_file__ as the notebook path
    try:
        notebook_path = ipython.user_ns["__vsc_ipynb_file__"]
    except NameError:
        raise RuntimeError("The global variable '__vsc_ipynb_file__' is not defined.")

    # Read the notebook file
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_data = nbformat.read(f, as_version=4)
    except Exception as e:
        raise RuntimeError(f"Failed to read the notebook file: {e}")

    # Retrieve the first cell
    if not notebook_data.cells or len(notebook_data.cells) < 1:
        raise ValueError("The notebook does not contain any cells.")

    parameter_cell = None
    for cell in notebook_data.cells:
        if "parameters" in cell.metadata.tags:
            parameter_cell = cell
            break

    if not parameter_cell:
        raise ValueError("No cell with 'parameters' tag found.")

    # Extract code from Markdown code block
    try:
        code_match = re.search(r"```python\n(.*?)\n```", parameter_cell.source, re.DOTALL)
        if not code_match:
            raise ValueError("No valid Python code block found in the 'parameters' cell.")
        code = code_match.group(1)

        # Parse the extracted code into a dictionary
        param_dict = {}
        exec(code, {}, param_dict)
        return {key: value for key, value in param_dict.items() if not key.startswith("__")}
    except Exception as e:
        raise RuntimeError(f"Failed to parse parameters: {e}")

# Example usage
if __name__ == "__main__":
    try:
        params = get_notebook_dev_params()
        print("Parsed Parameters:")
        print(params)
    except Exception as e:
        print(f"Error: {e}")