import sys
import re

NEW_LINE = '\n'
TAB = '    '
TAB2x = TAB + TAB


def parseArgs():
    args = {}
    inputArgs = sys.argv[1:]
    nextParam = ''
    for i in range(0, len(inputArgs)):
        if inputArgs[i].startswith('-') or inputArgs[i].startswith('--'):
            p = inputArgs[i].replace('-', '', 2)
            args[p] = ''
            nextParam = p
            continue
        if nextParam != '':
            args[nextParam] = inputArgs[i]
            nextParam = ''
    return args


def getArgParam(args, *keys):
    __keys = args.keys()
    for k in keys:
        if __keys.__contains__(k):
            return args[k]
    return ''


def camelToSnake(text):
    __snaked_name_arr = []
    n = text
    while True:
        if len(n) == 0:
            break
        __snaked_name = re.sub("(.)([A-Z].+)", r'\1_\2', n)
        arr = __snaked_name.split('_')
        if len(arr) > 1:
            __snaked_name_arr.append(arr.__getitem__(0))
            n = arr[1]
        else:
            __snaked_name_arr.append(arr.__getitem__(0))
            n = ""
    return "_".join(__snaked_name_arr).lower()


def snakeToCamel(text):
    # one_two_three => OneTwoThree
    arr = text.split("_")
    formattedArr = []
    for w in arr:
        formattedArr.append(w.replace(w[0], w[0].upper(), 1))
    return "".join(formattedArr)


def error(sentences):
    print(NEW_LINE)
    print("【❌Error】" + sentences)


def info(sentences):
    print(NEW_LINE)
    print("【📢Info】" + sentences)


def warn(sentences):
    print(NEW_LINE)
    print("【⚠️Warn】" + sentences)
