# Function to read and write CSV files
read_and_write_csv <- function(input_file_path, output_file_path, sample_size) {
  # Load the data from the input CSV file
  data <- read.csv(input_file_path)

  # Sample rows from the data
  nsample <- min(sample_size, nrow(data))
  samp_idx <- sample(seq_len(nrow(data)), nsample)
  new_data <- data[samp_idx, ]

  # Write the sampled data to the output CSV file
  write.csv(new_data, output_file_path, row.names = FALSE)

  # Read the CSV file again
  new_data <- read.csv(output_file_path)

  # Rename the column
  colnames(new_data)[colnames(new_data) == "x"] <- "File Name"

  # Write the modified data to a new CSV file
  write.csv(new_data, output_file_path, row.names = FALSE)
}

# Main function
main <- function() {
  # Input file paths
  input_file_path <- "/home/jouhaina/Documents/AIEnabledSystem/21-07-2023/randomly_collect_data/filename.csv"
  output_file_path <- "/home/jouhaina/Documents/AIEnabledSystem/21-07-2023/randomly_collect_data/output.csv"
  sample_size <- 383

  # Call the function to read and write CSV files
  read_and_write_csv(input_file_path, output_file_path, sample_size)
}

# Call the main function
main()
