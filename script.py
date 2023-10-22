import json
import os
import subprocess

def run_shell_script(script):
    """
    Run a shell script using subprocess.

    Args:
        script (str): The shell script to execute.

    Returns:
        None
    """
    try:
        subprocess.run(script, check=True, shell=True, executable='/bin/bash')
    except subprocess.CalledProcessError as e:
        print(f"Error running the script: {e}")

def extract_hadith_data(filename):
    """
    Extract Hadith data from a JSON file and structure it into a dictionary.

    Args:
        filename (str): The filename of the input JSON file.

    Returns:
        dict: A dictionary containing structured Hadith data or None if an error occurs.
    """
    try:
        with open(filename, 'r') as infile:
            indata = json.load(infile)
        
        outdata = {
            "title": indata["metadata"]["arabic"]["title"],
            "author": indata["metadata"]["arabic"]["author"],
            "introduction": indata["metadata"]["arabic"]["introduction"],
            "chapters": []
        }

        for chapter in indata["chapters"]:
            chapter_data = {
                "title": chapter["arabic"],
                "hadiths": [hadith["arabic"] for hadith in indata["hadiths"] if hadith["chapterId"] == chapter["id"]]
            }
            outdata["chapters"].append(chapter_data)
        
        return outdata
    except Exception as e:
        print(f"Error extracting Hadith data from {filename}: {e}")
        return None

if __name__ == "__main__":
    # Clone the repository, install npm packages, and run the script
    shell_script = """
    mkdir ahmed && cd ahmed 
    git clone https://github.com/A7med3bdulBaset/hadith-json.git
    cd hadith-json
    npm install
    npm run build
    npm run start 
    # process not stopping; will fix it when I find a solution
    """
    run_shell_script(shell_script)

    # Paths for input and output
    ahmed_repo = "ahmed/hadith-json"
    rawdata_path = f"{ahmed_repo}/db/by_book/"
    output_path = "books/"

    all_paths = file_paths = [os.path.join(root, file) for root, _, files in os.walk(rawdata_path) for file in files]

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for path in all_paths:
        filename = os.path.basename(path)
        print(f"Processing {filename} ...", end=" ")
        data = extract_hadith_data(path)

        if data:
            with open(os.path.join(output_path, filename), 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, indent=4, ensure_ascii=False)
        
        print("✓")

    # Remove the cloned repository
    run_shell_script("rm -rf ahmed")
