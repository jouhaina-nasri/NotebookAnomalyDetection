import nbformat
import pandas as pd

def get_code_cell_content(notebook_path, cell_index):
    """
    Extracts the source content of a code cell from a Jupyter notebook.
    
    :param notebook_path: Path to the Jupyter notebook file.
    :param cell_index: Index of the cell to be extracted.
    :return: The source code of the specified cell or an error message.
    """
    try:
        with open(notebook_path, 'r') as f:
            notebook_content = f.read()

        notebook = nbformat.reads(notebook_content, as_version=4)

        if cell_index < 0 or cell_index >= len(notebook.cells):
            return "Invalid cell number."

        cell = notebook.cells[cell_index]

        if cell.cell_type != "code":
            return "Not a code cell."

        return cell.source
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    # User-provided input and output CSV file paths
    input_csv_path = input("Enter the path of the input CSV file: ").strip()
    output_csv_path = input("Enter the path where you want to save the output CSV file: ").strip()

    # Read the initial CSV file
    try:
        df_input = pd.read_csv(input_csv_path)
    except FileNotFoundError:
        print("The specified input CSV file could not be found.")
        return

    # Initialize a list to store the output data
    output_data = []

    # Populate the list with the output data
    for index, row in df_input.iterrows():
        notebook_path = row['File']
        cell_index = row['Cell']
        cell_content = get_code_cell_content(notebook_path, cell_index)

        output_row = {
            "File": row['File'],
            "Cell": cell_index,
            "cell_content": cell_content
        }
        output_data.append(output_row)

    # Convert the list of dictionaries to a DataFrame
    df_output = pd.DataFrame(output_data)

    # Write the DataFrame to an output CSV file
    df_output.to_csv(output_csv_path, index=False)
    print(f"Data has been written to {output_csv_path}")

if __name__ == "__main__":
    main()
