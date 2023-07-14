import os
import shutil
from datetime import date
import streamlit as st


def filing():
    def copy_files_with_date(source_folder):
    # Set the destination folders
            destination_folders = [
                r"C:\Users\express\Documents\abrar field",
                r"C:\Users\express\Documents\abrar south field",
                r"C:\Users\express\Documents\ferdaus field"
            ]

            # Get today's date
            today = date.today().strftime("%Y-%m-%d")  # Format the date as "YYYY-MM-DD"

            # Loop through the files in the source folder
            for filename in os.listdir(source_folder):
                file_path = os.path.join(source_folder, filename)
                print(file_path)

                # Check if the item is a file
                if os.path.isfile(file_path):
                    # Loop through each destination folder
                    for destination_folder in destination_folders:
                        # Loop through the subfolders in the destination folder
                        for folder_name in os.listdir(destination_folder):
                            print(folder_name)
                            subfolder_path = os.path.join(destination_folder, folder_name)

                            # Check if the item is a folder
                            if os.path.isdir(subfolder_path):
                                # Check if the file name matches the subfolder name
                                filename_without_extension = os.path.splitext(filename)[0]
                                if filename_without_extension.lower() == folder_name.lower():
                                    # Add today's date to the end of the file name
                                    new_filename = filename_without_extension + "." + today + os.path.splitext(filename)[1]
                                    # Copy the file to the corresponding subfolder with the updated filename
                                    new_file_path = os.path.join(subfolder_path, new_filename)
                                    shutil.copy(file_path, new_file_path)
                                    print(f"Copied file: {filename} -> {new_file_path}")
                                    break  # Exit the inner loop if the file is copied
                        else:
                            continue  # Continue to the next destination folder if not found in the current folder
                        break  # Exit the outer loop if the file is copied

            print("File copying completed!")


    st.header("Document Filing System")

    dfl_button = st.button('DFL & Dyna')

    detailed_button = st.button('Detailed production')




    if dfl_button:
        copy_files_with_date(r"C:\Users\express\Documents\dfl update")
        st.write('done filing')
        


