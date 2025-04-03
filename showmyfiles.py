import os

def main():
    # Get the absolute path of the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_file_name = "myapp.txt"
    output_file_path = os.path.join(current_dir, output_file_name)
    
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        # Walk through the directory tree
        for root, dirs, files in os.walk(current_dir):
            # Skip __pycache__, .git, and storage directories
            dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git", "storage")]
            
            for file in files:
                # Skip the output file and any git-related files
                if file == output_file_name or file.startswith(".git"):
                    continue

                file_path = os.path.join(root, file)
                # Ignore this script itself
                if os.path.abspath(file_path) == os.path.abspath(__file__):
                    continue

                # Determine the relative path from the current directory
                relative_path = os.path.relpath(file_path, current_dir)
                # For files in subdirectories, prepend a "/" to match the desired format
                if os.path.dirname(relative_path):
                    display_path = "/" + relative_path.replace(os.path.sep, "/")
                else:
                    display_path = relative_path

                # Write the file header with the file name
                output_file.write(f"{display_path}:\n")
                
                # For .js and .css files, only include the name with a placeholder message
                if file.lower().endswith(('.js', '.css')):
                    output_file.write("[Library file content skipped]\n\n")
                    continue
                
                # For other files, try to open and read their contents, handling errors gracefully
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        contents = f.read()
                except Exception as e:
                    contents = f"Error reading file: {e}"
                
                # Write the file contents followed by a blank line for separation
                output_file.write(f"{contents}\n\n")

if __name__ == '__main__':
    main()
