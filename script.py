from itertools import chain
import json
import os
import subprocess
from enum import Enum


GroupBy = Enum('GroupBy', ['CHAPTER', 'BOOK'])


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


def extract_hadith_data(filename, group_by: GroupBy):
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

        match group_by:
            case GroupBy.BOOK:
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
            case GroupBy.CHAPTER:
                outdata = {
                    "title": indata["chapter"]["arabic"] if "chapter" in indata else "",
                    "hadiths": [hadith["arabic"] for hadith in indata["hadiths"]]
                }
                return outdata
    except Exception as e:
        print(f"Error extracting Hadith data from {filename}: {e}")
        return None


def processing(rawdata_path, output_path, group_by: GroupBy = GroupBy.BOOK):

    paths = [
        os.path.join(root, file) for root, _, files in os.walk(rawdata_path) for file in files
    ]

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    print(f"""
            -----------------------------------------
            ================{group_by}===============
            -----------------------------------------
    """)
    for path in paths:
        filename = os.path.basename(path)
        print(f"Processing {path} ...", end=" ")
        data = extract_hadith_data(path, group_by)

        if data:
            with open(os.path.join(output_path, filename), 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, indent=4, ensure_ascii=False)

        print("✓")


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

        # by book
        rawdata_path = os.path.join("ahmed", "hadith-json", "db", "by_book")
        processing(rawdata_path, os.path.join("output", "group_by_book"))

        # by chapter
        rawdata_path = os.path.join("ahmed", "hadith-json", "db", "by_chapter")
        book_paths = [os.path.join(rawdata_path, catgoryFolder, bookname)
              for catgoryFolder in os.listdir(rawdata_path)
              for bookname in os.listdir(os.path.join(rawdata_path, catgoryFolder))]
        
        for book_path in book_paths:
            processing(book_path, os.path.join(
                os.path.join("output", "group_by_chapter"), os.path.basename(book_path)), GroupBy.CHAPTER)

        # Remove the cloned repository
        run_shell_script("rm -rf ahmed")
