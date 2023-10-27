import csv
import ast  # Import missing in the original code
import nbformat
import glob

def file_name(notebook_files, download_path):
    output_path = f"{download_path}/filename.csv"

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)

        notebook_cells = []  # List to store cells for each notebook file

        for notebook_file in notebook_files:
            try:
                notebook = nbformat.read(notebook_file, nbformat.NO_CONVERT)

                for cell_number, cell in enumerate(notebook.cells):
                    if cell.cell_type == 'code':
                        file_name = notebook_file.split("/")[-1]
                        cell_source = cell.source.strip()  # Remove leading and trailing whitespace

                        # Skip empty cells
                        if not cell_source:
                            continue

                        # Skip code cells that start with a Jupyter magic command
                        if cell_source.startswith('%'):
                            continue

                        try:
                            cell_ast = ast.parse(cell_source)
                        except SyntaxError:
                            continue  # Skip cells with syntax errors

                        notebook_cells.append([file_name, cell_number])  # Add the cell index

            except AttributeError as e:
                continue

        # Generate the header row with the appropriate number of cell columns
        header_row = ["Notebook", "Cell"]

        # Write the CSV header
        csv_writer.writerow(header_row)

        # Write the cells from the notebook files
        for file_name, cell_index in notebook_cells:
            csv_writer.writerow([file_name, cell_index])

    print(f"Résultats sauvegardés dans {output_path}")

if __name__ == '__main__':
    print('Enter folder path :')
    folder_path = input().strip()  # Remove spaces at the beginning and end
    notebook_files = glob.glob(f"{folder_path}/*.ipynb")

    print('Enter download path :')
    download_path = input().strip()  #
