import json

def extract_fields(input_file="loc_books_data.json", output_file="extracted_books_data.json"):
    extracted_data = []

    # Load the JSON data
    with open(input_file, "r") as f:
        data = json.load(f)

    # Extract relevant fields from each entry
    for entry in data:
        title = entry.get("title", "No Title")
        translated_title = entry.get("translated_title", "No Translated Title")
        language = entry.get("language", ["No Language"])
        subjects = entry.get("subject", ["No Subject"])
        summary = entry.get("description", "No Summary")
        contributors = entry.get("contributor", ["No Contributors"])

        # If fields are lists, join them into a single string
        language = ", ".join(language) if isinstance(language, list) else language
        subjects = ", ".join(subjects) if isinstance(subjects, list) else subjects
        contributors = ", ".join(contributors) if isinstance(contributors, list) else contributors

        # Add to extracted data
        extracted_data.append({
            "title": title,
            "translated_title": translated_title,
            "language": language,
            "subjects": subjects,
            "summary": summary,
            "contributors": contributors
        })

    # Save the extracted data to a new JSON file
    with open(output_file, "w") as f:
        json.dump(extracted_data, f, indent=2)
    
    print(f"Extracted data saved to {output_file}")

# Run the extraction
if __name__ == "__main__":
    extract_fields()
