#!/usr/bin/env python
# coding: utf-8

# Python code for extracting and preprocessing UNSC speech transcripts

# Procedures for speech extraction
import re

# Parsing and cleaning UNSC speech records
def clean_PV(path, form="pdf"):
    """
    Arguments:
    - path (string): path to an input plain text file (converted from either MS doc file or PDF)
    - form (string): format of the original file obtained from UN Document system ('doc': MS Word, 'pdf': PDF)
    
    Returns:
    - president (tupl): the counbcil's president name ('string') and country ('string')
    - agenda (string): meeting agenda
    - text (string): cleaned text
    - num_words (integer): # of words contained in the text
    - num_paras (integer): # of paragraphs contained in the text
    """
    
    f = open(path, 'r')
    lines = f.readlines()
    num_lines = len(lines)
    main = False
    search_president = True
    search_agenda = [True, False]
    agenda_para = 0
    pdf_correction1 = [True, False]
    text_to_move = []
    pdf_correction2 = False
    
    president = []
    agenda = ''
    processed = []
    
    # Matching with regular expressions
    reg0 = re.compile(r"^(adoption of the agenda|expression of.+|opening statement).*$")
    reg1 = re.compile(r"^.+(\.{1}|\?|\")$")
    reg2 = re.compile(r"^.+:.*$")
    reg3 = re.compile(r"[\t\r\n\f]")
    reg4 = re.compile(r"\s\s+")
    reg5 = re.compile(r"^(\d+|\d+/\d+.{0,1}|\d{2}/\d{2}/\d{4}|\d{2}-\d{5}.*|S/PV\.\s*\d{4})$")
    reg6 = re.compile(r"^(\d{4}\D{2}\smeeting|Security Council|(For|Fif|Six|Sev)\D+\syear|\d+\s\S+\s\d{4})$")
    reg7 = re.compile(r"^\(((mr|mrs|ms|dr|sir|lord).+,.+|the president|the secretary-general|the secretary general)\)$")
    reg8 = re.compile(r"^(mr|mrs|ms|dr|sir|lord|the president|the secretary-general|the secretary general).*:.*$")
    reg9 = re.compile(r"^(mr|mrs|ms|dr|sir|lord|the president|the secretary-general|the secretary general).*$")
    reg10 = re.compile(r"^(arabic|russian|chinese|french|spanish|english).+$")
    reg11 = re.compile(r"^\*(\s|\*)+$")
    
    for i, line in enumerate(lines):
        
        line = str(line).strip()
        
        # Blank lines are not read.
        if len(line) == 0:
            continue
        
        # Procedure before reading the main text
        if not main:
            
            reg = re.compile(r"^the meeting (was called to order|resumed|was resumed|was suspended).+$")
            if reg.match(line.strip('\t').lower()):
                main= True
                continue
            
            # Obtaining information on the Council President
            if search_president:
                reg = re.compile(r"^(mr|mrs|ms|dr|sir|lord).+$")
                if reg.match(line.lower()):
                    reg = re.compile(r"\.(\s\.)+")
                    pres_name = reg.sub('', line).replace('later', '').strip()
                    president.append(pres_name)
                    continue
                reg = re.compile(r"^\(.+\)$")
                if reg.match(line):
                    pres_country = line.replace('(', '').replace(')', '').strip()
                    president.append(pres_country)
                    search_president = False
                    continue
            
            # Obtaining information on the agenda items
            if search_agenda[0]:
                if line.lower() == 'agenda':
                    search_agenda[1] = True
                    continue
                if search_agenda[1]:
                    agenda = line
                    if agenda.isupper():
                        agenda = agenda.title()
                    search_agenda[0] = False
                    continue

            continue
        
        # Termination
        reg = re.compile(r"^the meeting (rose|was suspended).+$")
        if reg.match(line.lower()) or (i >= num_lines - 1):
            break
            
        # Additional procedure for pdf
        if form == 'pdf':
            
            if pdf_correction1[0]:
                reg = re.compile(r"^the president.*:")
                if reg0.match(line.lower()) or reg.match(line.lower()):
                    pdf_correction1[0] = False
                elif (len(line) > 0) and (not pdf_correction1[1]):
                    pdf_correction1[1] = True
            
            if not pdf_correction2:
                if line == 'The Security Council will now':
                    pdf_correction2 = True
                    line_to_add = len(processed)
            else:
                reg = re.compile(r"^(begin|resume)$")
                if reg.match(line):
                    processed[line_to_add] = (processed[line_to_add] + ' ' + line)
                    continue
                elif line == 'its':
                    processed[line_to_add] = (processed[line_to_add] + ' ' + line)
                    pdf_correction2 = False
                    continue
            
            page_break = False
            if (reg5.match(line)) or (reg6.match(line)) or (reg7.match(line.lower())):
                page_break = True
            elif (agenda_para > 1) and (line.lower() in agenda.lower()):
                page_break = True
            elif (agenda_para == 0) and ('resumption' in path.lower()) and (line.lower() in agenda.lower()):
                page_break = True
            if page_break:
                if pdf_correction1[1] and (len(text_to_move) > 0):
                    processed.extend(text_to_move)
                    text_to_move = []
                    pdf_correction1[1] = False
                continue
        
        # Reading the main body of text

        # If agenda information has not been  detected on the front cover...
        if search_agenda[0]:
            if 'the agenda was adopted' in line.lower():
                search_agenda[1] = True
            elif search_agenda[1]:
                agenda = line
                if agenda.isupper():
                    agenda = agenda.title()
                search_agenda[0] = False
        
        # Inserting line breaks for agenda adoption, opening remarks, acknowledgements, etc.
        if line[0].isupper() and reg0.match(line.lower()):
            line = '--para--' + line + '--para--'
          
        else:
            if reg1.match(line):
                line = line + '--para--'
            
            if reg2.match(line.strip('--para--')):
                 if (line[0].isupper()) and (reg8.match(line.lower())):
                    line = '--para--' + line
                    if len(processed) > 0:
                        previous = processed[-1]
                        if not previous.endswith('\n'):
                            processed[-1] = previous + '\n'
                
                elif len(processed) > 0:
                    previous = processed[-1]
                    if reg9.match(previous.lower()):
                        processed[-1] = '\n' + previous
                        if len(processed) > 1:
                            preceding = processed[-2]
                            if not preceding.endswith('\n'):
                                processed[-2] = preceding + '\n'
        
        # Forced line breaks for agenda-setting paragraphs
        if agenda_para == 0:
            if 'adoption of the agenda' in line.lower():
                agenda_para += 1
        elif agenda_para == 1:
            if reg8.match(line.lower().strip('--para--')):
                agenda_para += 1
            elif not line.endswith('--para--'):
                if i + 1 < num_lines:
                    next_line = lines[i+1].strip()
                    if (len(next_line) > 0) and next_line[0].isupper():
                        line = line + '--para--'
                    elif len(next_line) == 0:
                        line = line + '--para--'
        
        # Ignore some symbols
        if reg11.match(line):
            continue
        
        # Common procedure
        line = reg4.sub(' ', reg3.sub(' ', line))
        line = line.strip().replace('--para--', '\n')
        if len(line) == 0:
            continue
        
        # Correction for reading in pdf
        if (form == 'pdf') and pdf_correction1[0]:
            text_to_move.append(line)
            continue
        
        processed.append(line)
    
    text = ' '.join(processed).replace('\n ', '\n').replace(' \n', '\n').strip()
    num_words = len(text.split())
    num_paras = len(text.split('\n\n'))
    return president, agenda, text, num_words, num_paras


# Extraction of speech texts and other information from a single cleaned meeting record
def speech_extraction(path, president_as_delegate=True, remove_quotes=True, speaker_thres=5):
    """
    Arguments:
    - path (string): path to an input text file that contains a cleaned speech record, i.e., output of clean_PV()
    - president_as_delegate (boolean): if True, presidents' procedural statements are discarded
    - remove_quotes (boolean): if True, all in-speech quotes are removed
    - speaker_thres (integer): a threshold number of tokens for detecting a speaker's name
    
    Returns:
    - records (2d list): each row consists of information on a single speech, which includes:
      - speaker (string): the speaker's name
      - country (string): the country represented by the speaker
      - speech (string): speech text
      - count (integer): word count of the speech
    """
    
    f = open(path, 'r')
    text = f.read()
    paras = text.split('\n\n')  # given that paragraphs are separated with double line-breaks (\n\n)

    speakers = []
    countries = []
    speeches = []
    records = []

    # Matching with regular expressions
    reg0 = re.compile(r"^(mr|mrs|ms|dr|sir|lord|the president|the secretary-general|the secretary general).*:.*")
    reg1 = re.compile(r"(in my capacity as|in my national capacity|resume my functions as)")
    reg2 = re.compile(r"“[^“\n]+”")
    reg3 = re.compile(r"“[^”\n]+\n")
    reg4 = re.compile(r"\s—\s")
    reg5 = re.compile(r"\s\s+")
    reg6 = re.compile(r"\s")
    reg7 = re.compile(r"\"[^\"\n]+\"")
    reg8 = re.compile(r"\"[^\"\n]+\n")

    # Procsseing each speech paragraph
    for para in paras:
        para = para.strip()
        speaker = "NULL"
        country = "NULL"
        speech = "NULL"
        if reg0.match(para.lower()):
            parts = para.split(':')
            head = parts[0]
            speech = (':'.join(parts[1:])).strip()

            # Deleting an in-speech quotation
            if remove_quotes:
                speech = reg5.sub(' ', reg4.sub(' ', reg3.sub('', reg2.sub('', speech))))
                speech = reg5.sub(' ', reg4.sub(' ', reg8.sub('', reg7.sub('', speech))))

            # Separating the colon that follows the speaker's name from the colon that appears in the speech text
            part = head.split('(')[0].strip()
            if len(part.split()) <= speaker_thres:
                speaker = part.strip()
                country = 'n.a.'
                if ('(' in head) and (')' in head):
                    country = head.split('(')[1].split(')')[0].strip()
            else:
                if len(speeches) > 0:
                    previous = speeches[-1]
                    if previous != "NULL":
                        speeches[-1] = (previous + ' ' + para)
                continue
                
            # In the case that the President is referred to as "Mr. President" etc. instead of "The President"
            if (speaker.lower() == 'mr. president') or (speaker.lower() == 'ms. president'):
                speaker = 'The President'
            
            # To record statements made by the President on behalf of his or her country
            if speaker.lower() == 'the president' and president_as_delegate:
                if not reg1.search(reg5.sub(' ', speech.replace('\n', ' ').lower())):
                    speaker = "NULL"
                    country = "NULL"
                    speech = "NULL"
        
        speakers.append(speaker)
        countries.append(country)
        speeches.append(speech)

    # To aggregate and format the entire output
    num_speakers = len(speakers)
    for i in range(num_speakers):
        speaker = speakers[i].title()
        country = countries[i]
        # Dealing with irregularities for the speaker's name or country
        if speakers[i].upper() == "NULL":
            continue
        if speaker.lower() == 'the president':
            country = 'n.a.'
        elif (country.lower().startswith('spoke')) or (country.lower().startswith('interpretation')):
            country = 'n.a.'
        speech = speeches[i]
        count = len(reg5.sub(' ', reg6.sub(' ', speech)).split())
        if count == 0:
            continue
        row = [speaker, country, speech, count]
        records.append(row)
    
    return records

