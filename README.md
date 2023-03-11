# undocs

This repository contains Python code that processes and analyzes various policy documents published by the United Nations. As of March 2023, the code exclusively handles the speech transcripts of official meetings at the UN Security Council (UNSC) and consists of the following components:
- *preprocesses_speech.py*: extracts and preprocesses UNSC speech transcripts, converting these documents into machine-readable text data.

# Getting Started
## Prerequisites
- Python 3.6.x
## Data Preparation
To use this code, follow these steps:
- Obtain the original documents from the [Official Document System (ODS)](https://undocs.org/) of the United Nations. In the case of UNSC meeting records, the website of the Dag Hammarskjöld Library provides  [a useful gateway](https://research.un.org/en/docs/sc/quick/)  to the entire body of these records.
- Convert the obtained documents into plain text format using an appropriate command (such as *textutil* and *pdftotext*) or software (such as Microsoft Word).
## Usage
You can use the functions and procedures contained in the code in any way you like. In the case of UNSC meeting records, the typical workflow involves cleaning the converted plain texts with the *clean_PV()* function and extracting individual speeches from the preprocessed texts with the *speech_extraction()* function.

# Versions
- 0.0 (May 17, 2020)
- 1.0 (March 11, 2023)
