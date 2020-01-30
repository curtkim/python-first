import re

p = re.compile('\(double\[\]\) \[(.*)\]')

def append_parentheses_assertEquals(input):
    p = re.compile(r'assertEquals (.*), (.*)')
    r = r'assertEquals(\1, \2);'
    result = p.subn(r, input)
    print(f"append_parentheses_assertEquals: {result[1]} times")
    return result[0]

def append_parentheses_assertTrue(input):
    p = re.compile(r'assertTrue (.*)')
    r = r'assertTrue(\1);'
    result = p.subn(r, input)
    print(f"append_parentheses_assertTrue: {result[1]} times")
    return result[0]

def append_parentheses_assertFalse(input):
    p = re.compile(r'assertFalse (.*)')
    r = r'assertFalse(\1);'
    result = p.subn(r, input)
    print(f"append_parentheses_assertFalse: {result[1]} times")
    return result[0]

def replace_double_array(input):
    p = re.compile(r'\(double\[\]\) \[([\s|\d|,|\.|\-]*)\]')
    r = r'new double__{\1}'
    result = p.subn(r, input)
    print(f"replace_double_array: {result[1]} times")
    return result[0]

def replace_array_to_list(input):
    p = re.compile(r' \[(.*)\]')
    r = r' Arrays.asList(\1)'
    result = p.subn(r, input)
    print(f"replace_array_to_list: {result[1]} times")
    return result[0]

def replace_array_to_list1(input):
    p = re.compile("\[")
    r = r'Arrays.asList('
    result = p.subn(r, input)
    print(f"replace_array_to_list1: {result[1]} times")
    return result[0]

def replace_array_to_list2(input):
    p = re.compile("\]")
    r = r')'
    result = p.subn(r, input)
    print(f"replace_array_to_list2: {result[1]} times")
    return result[0]

### by line

def append_semicolon_by_line(input):
    """ 앞에 공백이 4개 있는 경우만 """
    if input.startswith("    ") and input[4] != ' ' and not input.endswith(";"):
        return (input + ";") #.replace(";;", ";")
    else:
        return input

def append_semicolon_to_import_by_line(input):
    p = re.compile(r'^import (.*)')
    r = r'import \1;'
    return p.sub(r, input)

def append_semicolon_to_package_by_line(input):
    p = re.compile(r'^package (.*)')
    r = r'package \1;' + """
import java.util.Arrays;
import java.util.Map;
import java.util.List;
import java.util.ArrayList;
import java.util.Set;
import java.util.HashSet;
import java.util.HashMap;
    """
    return p.sub(r, input)

def process_by_line(line):
    line = append_semicolon_to_import_by_line(line)
    line = append_semicolon_to_package_by_line(line)
    line = append_semicolon_by_line(line)
    return line


import os
from pathlib import Path

SOURCE_DIR = 
DEST_DIR = 

for path in Path(SOURCE_DIR).glob('**/*.groovy'):
    #path = SOURCE_DIR + "/com/kakao/mapmatch/common/UtilsTest.groovy"
    with open(path, 'r') as file:
        content = file.read()

        content = replace_double_array(content)
        content = replace_array_to_list(content)
        content = replace_array_to_list1(content)
        content = replace_array_to_list2(content)
        content = content.replace("__", "[]", 9999)
        content = content.replace("class", "public class", 9999)
        content = append_parentheses_assertEquals(content)
        content = append_parentheses_assertTrue(content)
        content = append_parentheses_assertFalse(content)

        lines = content.split("\n")
        content = "\n".join([process_by_line(line) for line in lines])

        newpath = str(path).replace(SOURCE_DIR, DEST_DIR)
        newpath = newpath.replace('.groovy', '.java')
        (dir, filename) = os.path.split(newpath)

        Path(dir).mkdir(parents=True, exist_ok=True)
        f = open(newpath, "w")
        f.write(content)
        f.close()

        print("=========" + newpath)
        print(content)
