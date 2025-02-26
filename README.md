# Speech Transcript Extraction and Cleaning for UNSC Meeting Data

This repository contains a collection of Jupyter Notebook cells and Python scripts designed to extract, clean, and parse speech transcripts from OCR-processed Word documents. The code is tailored for processing United Nations Security Council (UNSC) meeting records, extracting speaker and speech information, and merging it with meeting data.

## Overview

The code in this repository performs the following main tasks:

1. **Text Extraction:**  
   Extracts text from OCR’d Word documents using ABBYY FineReader output. It filters for English paragraphs and removes unwanted formatting like hyphenation and extra newlines.

2. **Text Cleaning and Parsing:**  
   Cleans the extracted text using regular expressions. This step also segments the transcript into paragraphs and counts words and paragraphs.

3. **Merging Meeting Data:**  
   Matches the cleaned transcript files with meeting metadata and augments the transcript data with meeting details such as meeting number, date, topic, and agenda.

4. **Speaker and Speech Extraction:**  
   Uses regular expressions to extract speaker names and individual speech blocks from the cleaned text. Special handling is included for cases like the President, Acting President, Secretary-General, and Chairman.

5. **Combining Speech Data:**  
   Merges newly extracted speech data with any existing speech data, sorts the combined data, and saves the final outputs in a TSV file.

## File Structure

- **Notebooks / Scripts:**  
  The notebook contains all the cells for processing the data in sequential steps:
  - Text extraction from Word documents.
  - Text cleaning and parsing.
  - Merging of meeting data.
  - Extraction of speaker and speech data.
  - Updating meeting data with speech data availability.
  - Merging and final output of speech transcripts.

- **Data Files:**  
  The code uses several data files:
  - **Word Documents:** OCR’d files located in a folder specified by the placeholder `PATH_TO_ORIGINAL_WORD_FILES`.
  - **Corrections File:** A CSV file containing text correction mappings (placeholder: `PATH_TO_CORRECTIONS_FILE/corrections.csv`).
  - **Titles File:** A CSV file with honorific and position labels (placeholder: `PATH_TO_TITLES_FILE/titles.csv`).
  - **Meeting Data:** A TSV file containing meeting metadata (placeholder: `PATH_TO_MEETINGS_FILE/meetings.tsv`).

- **Output Directories:**  
  The code writes output files to directories with paths:
  - Extracted text files (`PATH_TO_EXTRACTED_TEXT`).
  - Cleaned transcript files (`PATH_TO_CLEANED_TEXT`).
  - Updated document lists and merged data (`PATH_TO_OUTPUT_DF`).
  - Final speech data (`PATH_TO_SPEECH_OUTPUT`).

## Requirements

- **Python 3.7+** (tested with Python 3.12.7)
- **Libraries:**
  - `python-docx`
  - `langdetect`
  - `pandas`
  - `re` (standard library)
  - `glob` (standard library)

## Usage Instructions

1. **Update Paths:**  
   Before running the notebook, update all the placeholder paths (e.g., `PATH_TO_ORIGINAL_WORD_FILES`, `PATH_TO_CORRECTIONS_FILE`, etc.) with the actual paths on your system.

2. **Run the Notebook:**  
   Execute the notebook cells sequentially to:
   - Extract text from the OCR’d Word files.
   - Clean and parse the extracted text.
   - Merge the cleaned transcript data with the meeting metadata.
   - Extract speaker and speech data.
   - Update and merge speech data with previous records.
   
3. **Output Files:**  
   After running the notebook, the cleaned transcripts, merged meeting data, and final speech data will be saved in the respective output directories specified by your updated paths.
