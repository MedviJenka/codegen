# import pandas as pd
#
#
# path1 = r'C:\Users\evgenyp\PycharmProjects\codegen\output\original_page_base.csv'
# path2 = r'C:\Users\evgenyp\PycharmProjects\codegen\output\page_base.csv'
#
#
# def compare_csv_by_element_path_and_name(file1_path: str, file2_path: str, output_folder: str = "./"):
#     """
#     Compares two CSV files based on 'Element Path'. If no match is found, it falls back to 'Element Name'.
#
#     Parameters:
#         file1_path (str): Path to the first CSV file.
#         file2_path (str): Path to the second CSV file.
#         output_folder (str): Folder where the results will be saved (default is the current directory).
#
#     Returns:
#         None: Saves the comparison results as CSV files.
#     """
#     # Load both CSV files
#     df1 = pd.read_csv(file1_path)
#     df2 = pd.read_csv(file2_path)
#
#     # Normalize column names (in case of extra spaces)
#     df1.columns = df1.columns.str.strip()
#     df2.columns = df2.columns.str.strip()
#
#     # Ensure consistent case formatting for matching
#     df1["Element Path"] = df1["Element Path"].str.strip().str.lower()
#     df2["Element Path"] = df2["Element Path"].str.strip().str.lower()
#     df1["Element Name"] = df1["Element Name"].str.strip().str.lower()
#     df2["Element Name"] = df2["Element Name"].str.strip().str.lower()
#
#     # Compare based on "Element Path" first
#     merged = df1.merge(df2, on="Element Path", how="outer", suffixes=("_file1", "_file2"), indicator=True)
#
#     # Identify elements that did not match by Element Path
#     unmatched_file1 = merged[merged["_merge"] == "left_only"]
#     unmatched_file2 = merged[merged["_merge"] == "right_only"]
#
#     # Try to match the unmatched elements by "Element Name"
#     df1_unmatched = df1[df1["Element Path"].isin(unmatched_file1["Element Path"])]
#     df2_unmatched = df2[df2["Element Path"].isin(unmatched_file2["Element Path"])]
#     name_matched = df1_unmatched.merge(df2_unmatched, on="Element Name", how="inner", suffixes=("_file1", "_file2"))
#
#     # Save results as CSV files
#     merged.to_csv(f"{output_folder}/comparison_results.csv", index=False)
#     pd.concat([unmatched_file1, unmatched_file2]).to_csv(f"{output_folder}/unmatched_elements.csv", index=False)
#     name_matched.to_csv(f"{output_folder}/matched_by_name.csv", index=False)
#
#     print(f"Comparison results saved in {output_folder}")
#
#
# # Example usage:
# compare_csv_by_element_path_and_name(path1, path2, "./")


import pandas as pd


def compare_csv_by_element_path_and_name(file1_path: str, file2_path: str, output_folder: str = "./"):
    """
    Compares two CSV files based on 'Element Path'. If no match is found, it falls back to 'Element Name'.
    Skips the header row when comparing.

    Parameters:
        file1_path (str): Path to the first CSV file.
        file2_path (str): Path to the second CSV file.
        output_folder (str): Folder where the results will be saved (default is the current directory).

    Returns:
        None: Saves the comparison results as CSV files.
    """
    # Load both CSV files, skipping the first row
    df1 = pd.read_csv(file1_path, skiprows=1)
    df2 = pd.read_csv(file2_path, skiprows=1)

    # Rename columns for consistency
    column_names = ["Element Name", "Element Type", "Element Path", "Action", "Value"]
    df1.columns = column_names
    df2.columns = column_names

    # Ensure consistent case formatting for matching
    df1["Element Path"] = df1["Element Path"].str.strip().str.lower()
    df2["Element Path"] = df2["Element Path"].str.strip().str.lower()
    df1["Element Name"] = df1["Element Name"].str.strip().str.lower()
    df2["Element Name"] = df2["Element Name"].str.strip().str.lower()

    # Compare based on "Element Path" first
    merged = df1.merge(df2, on="Element Path", how="outer", suffixes=("_file1", "_file2"), indicator=True)

    # Identify elements that did not match by Element Path
    unmatched_file1 = merged[merged["_merge"] == "left_only"]
    unmatched_file2 = merged[merged["_merge"] == "right_only"]

    # Try to match the unmatched elements by "Element Name"
    df1_unmatched = df1[df1["Element Path"].isin(unmatched_file1["Element Path"])]
    df2_unmatched = df2[df2["Element Path"].isin(unmatched_file2["Element Path"])]
    name_matched = df1_unmatched.merge(df2_unmatched, on="Element Name", how="inner", suffixes=("_file1", "_file2"))

    # Save results as CSV files
    merged.to_csv(f"{output_folder}/comparison_results.csv", index=False)
    pd.concat([unmatched_file1, unmatched_file2]).to_csv(f"{output_folder}/unmatched_elements.csv", index=False)
    name_matched.to_csv(f"{output_folder}/matched_by_name.csv", index=False)

    print(f"Comparison results saved in {output_folder}")

# Example usage:
# compare_csv_by_element_path_and_name("file1.csv", "file2.csv", output_folder="output_folder")
