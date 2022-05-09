# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

import re

regex = b"\\\\x[0-9]+PNG.*"

test_str = b"HTTP/1.0 200 OK\\r\\nServer: BaseHTTP/0.6 Python/3.9.2\\r\\nDate: Mon, 09 May 2022 13:27:26 GMT\\r\\nContent-type: image/jpeg\\r\\nConnection: keep-alive\\r\\nContent-length: 236\\r\\n\\r\\n\\x89PNG\\r\\n\\x1a\\n\\x00\\x00\\x00\\rIHDR\\x00\\x00\\x00\\t\\x00\\x00\\x00\\x06\\x08\\x02\\x00\\x00\\x00\\x9e\\xa5#\\x92\\x00\\x00\\x00\\xb3IDATx\\xda\\x01\\xa8\\x00W\\xff\\x01\\x8bhG'%%21-\\xb2\\xcb\\xde\\xe6\\xf6\\xfe\\x1b\\x12\\x0fL0\\x18\\xd2\\xe2\\xec\\x00$D\\x03YK9\\xfd\\xfa\\xf9\\xe8\\xe9\\xed\\xf7\\xfa\\xfe\\x08\\t\\r\\xf6\\xf3\\xf5\\xe7\\xe3\\xe0\\x01\\x06\\t6<M\\x03\\xfe\\xfb\\xfc\\x9c\\xb0\\xc4\\xf9\\xfb\\x00=\\x1d\\x0e\\x1d\\xfa\\xf1\\x05\\xff\\xfb\\xa7\\xb8\\xc8\\xa1\\xac\\xba\\xe0\\xdf\\xe0\\x03\\xe4\\xec\\xfaQ*\\x15nP:\\x05\\xf1\\xeb\\x1e\\x19\\x11\\xff\\xf2\\xebKA7\\xc7\\xcd\\xd4\\xb6\\xc7\\xd1\\x03dE5zsd\\xdb\\xcf\\xcf\\x10\\x05\\xf7\\x02\\x04\\x01\\xe2\\xde\\xdf\\x07\\x18$JEC\\xe2\\xe1\\xdf\\x03xJ0\\x02\\x00\\xff\\x08\\xfa\\xf7\\xe2\\xf3\\xfb\\xf0\\x0f$\\x12\\n\\n\\xf2\\xf0\\xf4\\x00\\xf7\\xf6\\x15\\x05\\x01_\\xdcUA\\x88\\x99\\xfee\\x00\\x00\\x00\\x00IEND\\xaeB`\\x82"
print(type(test_str))
matches = re.finditer(regex, test_str, re.MULTILINE)

for matchNum, match in enumerate(matches, start=1):
    
    print ("{match}".format( match = match.group()))
    
    # for groupNum in range(0, len(match.groups())):
    #     groupNum = groupNum + 1
        
    #     print ("2 Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))

# Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.
