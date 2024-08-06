import os

def collect_code(project_path, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith(('.py', '.html', '.js', '.css')):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, project_path)
                    
                    outfile.write(f"\n\n{'='*80}\n")
                    outfile.write(f"File: {relative_path}\n")
                    outfile.write(f"{'='*80}\n\n")
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            outfile.write(infile.read())
                    except Exception as e:
                        outfile.write(f"Error reading file: {str(e)}\n")

# Set the path to your Django project here
# place this script with target folder under same root, copy relative path
# - folder
#   - code2txt.py
#   - targetfolder
project_path = r"langTrainBackend"
output_file = "code_collection.txt"
collect_code(project_path, output_file)
# project_path = r"langTrainBackend"
# collect_code(project_path, output_file)


print(f"Code has been collected and saved to {output_file}")