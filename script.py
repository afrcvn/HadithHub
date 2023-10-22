import json
import os

def extract_hadith_data(filename: str) -> dict:
    """
    Extracts Hadith data from a JSON file and structures it into a dictionary.

    Args:
        filename (str): The filename of the input JSON file.

    Returns:
        dict: A dictionary containing structured Hadith data.

    Example raw data format:
    {
        "metadata": {
            "arabic": {
                "title": "Book Title",
                "author": "Author Name",
                "introduction": "Introduction to the Book"
            }
        },
        "chapters": [
            {
                "id": 1,
                "arabic": "Chapter 1 Title"
            },
            {
                "id": 2,
                "arabic": "Chapter 2 Title"
            }
        ],
        "hadiths": [
            {
                "chapterId": 1,
                "idInBook": 1,
                "arabic": "This is the text of Hadith 1 in Chapter 1"
            },
            {
                "chapterId": 1,
                "idInBook": 2,
                "arabic": "This is the text of Hadith 2 in Chapter 1"
            },
            {
                "chapterId": 2,
                "idInBook": 1,
                "arabic": "This is the text of Hadith 1 in Chapter 2"
            },
            {
                "chapterId": 2,
                "idInBook": 2,
                "arabic": "This is the text of Hadith 2 in Chapter 2"
            }
        ]
    }
    """

    # Initialize an empty dictionary to store the extracted data
    outdata = {
        "title": "",
        "author": "",
        "introduction": "",
        "chapters": []
    }
    
    # Open and read the input JSON file
    with open(filename + '.json', 'r') as infile:
        indata = json.load(infile)
    
    # Extract metadata information
    outdata["title"] = indata["metadata"]["arabic"]["title"]
    outdata["author"] = indata["metadata"]["arabic"]["author"]
    outdata["introduction"] = indata["metadata"]["arabic"]["introduction"]
    
    # Process chapters and their associated Hadiths
    for chapter in indata["chapters"]:
        chapter_data = {
            "title": chapter["arabic"],
            "hadiths": []
        }
        i = 0
        for hadith in indata["hadiths"]:
            if hadith["chapterId"] == chapter["id"]:
                i += 1
                # Create a dictionary for each Hadith and append it to the chapter's list
                chapter_data["hadiths"].append({
                    "id": i,
                    "content": hadith["arabic"]
                })
        outdata["chapters"].append(chapter_data)
    
    return outdata

if __name__ == "__main__":
    
    # Paths for input and output
    input_path = "raw/"
    output_path = "hadiths/"
    
    # Get a list of filenames (without the ".json" extension) in the "raw" folder
    booknames = [os.path.splitext(filename)[0] for filename in os.listdir(input_path) if filename.endswith(".json")]

    # Check if the output directory exists; if not, create it
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # Process each book and save the extracted data to output JSON files
    for bookname in booknames:
        data = extract_hadith_data(input_path + bookname)
        output_filename = bookname + '.json'
        print(f"Processing {bookname} ✓")
        with open(output_path + output_filename, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)
