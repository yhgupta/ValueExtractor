import json
import functools
import re
import csv


def table_create(testName):
    val_ran = []
    date_collected = []
    date_lines = []
    d = {
        "vitamin": ["ng/ml", 20, 50],
        "haemoglobin": ["gm/dl", 13.5, 17.5],
        "blood sugar": ["mg/dl", 100, 125],
        "tsh": ["ml", 0.5, 3.0],
        "thyroid stimulating hormone": ["ml", 0.5, 3.0],
        "total cholesterol": ["mg/d", 100, 199],
        "systolic": ["mmHg", 90, 120],
        "diastolic": ["mmHg", 60, 80],
    }

    class Line:
        def __init__(self, y):
            self.y = y
            self.words = []

    class Word:
        def __init__(self, name, x, y):
            self.name = name
            self.y = y
            self.x = x

    def find_lines(words):
        lines = []
        for word in words:
            line_available = False
            for line in lines:
                if abs(line.y - word.y) <= 10:
                    line.words.append(word)
                    line_available = True
                    break

            if not line_available:
                new_line = Line(word.y)
                new_line.words.append(word)
                lines.append(new_line)

        return lines

    def find_words(annotations):
        words = []
        for annotation in annotations:
            name = annotation['description']
            vertices = annotation['boundingPoly']['vertices']

            x = vertices[0]['x'] + (vertices[2]['x'] - vertices[0]['x']) / 2
            y = vertices[0]['y'] + (vertices[2]['y'] - vertices[0]['y']) / 2

            word = Word(name, x, y)
            words.append(word)

        return words

    def print_lines(lines):
        lines.sort(key=functools.cmp_to_key(compare_lines))
        for line in lines:
            text = ''
            line.words.sort(key=functools.cmp_to_key(compare_words))
            if not is_needed_line(line):
                continue
            for word in line.words:
                text += (word.name + ' ')
            return text

    def print_date_line(lines):
        lines.sort(key=functools.cmp_to_key(compare_lines))
        for line in lines:
            text = ''
            line.words.sort(key=functools.cmp_to_key(compare_words))
            if not date(line):
                continue
            for word in line.words:
                text += (word.name + ' ')
            return text

    def compare_lines(line1, line2):
        if line1.y < line2.y:
            return -1

        if line1.y == line2.y:
            return 0

        return 1

    def compare_words(word1, word2):
        if word1.x < word2.x:
            return -1

        if word1.x == word2.x:
            return 0

        return 1

    def date(line):
        text = ''
        for word in line.words:
            text += str(word.name).lower() + " "
        regex = r"((\d{1,2}|(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec))[\s\-\/](\d{1,2}|(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec))[\s\-\/]\d{1,2})"
        match_date = re.compile(regex)
        match_date = match_date.findall(text)
        for i in match_date:
            date_collected.append(i[0])
            break
        return len(match_date) > 0

    def is_needed_line(line):
        text = ''
        value = d.get(testName)[0]
        for word in line.words:
            text += str(word.name).lower() + " "
        regex = "^" + testName + ".*" + value
        match_line = re.compile(str(regex))
        match_line = match_line.findall(text)
        return match_line

    def is_number(num):
        try:
            float(str.strip(num))
            return True
        except:
            return False

    def find_range_value(line):
        line = line.lower()
        digit = "\d*\.*\d+"
        regex = r"(" + digit + ")\s(((.*" + digit + "\s*-\s*" + digit + ")|(" + digit + "\s*-\s*" + digit + ".*))|((.*" + digit + "\s*)|(\s*" + digit + ".*)))"
        # \s*
        match_line = re.compile(regex)
        match_line = match_line.findall(line)
        val_ran.append(match_line[0][0])
        val_ran.append(match_line[0][1])
        return match_line

    def find_date_from_selected():
        for text in date_lines:
            regex = r"((\d{1,2}|(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec))[\s\-\/](\d{1,2}|(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec))[\s\-\/]\d{2,4})"
            match_date = re.compile(regex)
            match_date = match_date.findall(text)
            for i in match_date:
                date_collected.append(i[0])
                break
            return len(match_date) > 0

    def main():
        with open('../Json/' + testName + '.json', encoding='utf8') as f:
            data = json.load(f)
            annotations = data['responses'][0]['textAnnotations'][1:]
            words = find_words(annotations)
            lines = find_lines(words)
            selected_line = print_lines(lines)
            print_date_line(lines)
            find_range_value(selected_line)
            find_date_from_selected()
            print('collected date', date_collected)
            print('value = {0} range = {1}'.format(val_ran[0], val_ran[1]))
            with open('csv.csv', 'w') as myFile:
                reader = csv.writer(myFile)
                t = [date_collected, val_ran[0]]
                reader.writerow(t)

    main()
