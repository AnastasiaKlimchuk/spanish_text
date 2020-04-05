import PyPDF2
import json
import docx
import os
import re

pdfFiles = []
# pdfFiles.append("/Users/stasy/PycharmProjects/spanish_text/3580.pdf")
# pdfFiles.append("/Users/stasy/PycharmProjects/spanish_text/3198.pdf")
for filename in os.listdir('.'):
    if filename.endswith('.pdf'):
        pdfFiles.append(filename)

words_url = 'words.docx'


def pdf_to_text(url):
    f = open(url, 'rb')
    pdf_text = list()
    # List of every page's text.
    # The index will correspond to the page number.
    pdf_reader = PyPDF2.PdfFileReader(f)
    for p in range(pdf_reader.numPages):
        page = pdf_reader.getPage(p)
        pdf_text.append(page.extractText())
    f.close()
    return pdf_text


def docx_to_list(url):
    words = list()
    f = open(url, 'rb')
    document = docx.Document(f)
    f.close()
    for para in document.paragraphs:
        if para.text != '':
            words.append(para.text)
    return words


def text_to_list(text):
    words = list()
    for page in text:
        words_bag = page.split()
        for i in range(len(words_bag)):
            words.append(words_bag[i].lower())
        # i = 0
        # try:
        #     while (i < len(words_bag)):
        #         if words_bag[i].endswith('-'):
        #             words_bag[i] = words_bag[i][:-1] + words_bag[i + 1]
        #             words.append(words_bag[i].lower())
        #             i += 2
        #         else:
        #             words.append(words_bag[i].lower())
        #             i += 1
        # except:
        #     print("Error in text_to_list")
        #     print(text)
        #     print(page)
        #     print(words_bag[i - 1])
    return words


def find_matches(text, words):
    idioms = dict()
    for word in words:
        indices = []
        for i, x in enumerate(text):
            x = re.sub('[\W_]+', '', x)
            if x == word or x == word + 's':
                indices.append(i)

        if indices:
            idioms[word] = list()

        for x in indices:
            phrase_list = text[x - 4:x + 5]

            idiom = ' '.join(phrase_list)
            idioms[word].append(idiom)
    return idioms


def find_all_idioms(pdf_url, words_url):
    group_words = docx_to_list(words_url)
    text = pdf_to_text(pdf_url)
    form_text = text_to_list(text)
    idioms = find_matches(form_text, group_words)
    return idioms


def wright_all_idioms(pdfFiles, words_url):
    root = dict()
    for pdf_url in pdfFiles:
        root[pdf_url] = find_all_idioms(pdf_url, words_url)

    with open('2017La_vanguardia.json', 'w', encoding='utf8') as json_file:
        json.dump(root, json_file, ensure_ascii=False)


wright_all_idioms(pdfFiles, words_url)
