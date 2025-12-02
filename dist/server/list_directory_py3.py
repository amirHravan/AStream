import os
import sys
import html
import urllib.parse
from io import BytesIO

def list_directory(path):
    """Helper to produce a directory listing (absent index.html)."""
    print("Get DIR listing for ", path)
    try:
        dir_list = os.listdir(path)
        print("The path for ", path, " is ", dir_list)
    except OSError:
        return BytesIO(b"404  No permission to list directory")
        
    dir_list.sort(key=lambda a: a.lower())
    f = BytesIO()
    displaypath = html.escape(urllib.parse.unquote(path))
    
    content = []
    content.append('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
    content.append("<html>\n<title>Directory listing for %s</title>\n" % displaypath)
    content.append("<body>\n<h2>Directory listing for %s</h2>\n" % displaypath)
    content.append("<hr>\n<ul>\n")
    
    for name in dir_list:
        fullname = os.path.join(path, name)
        displayname = linkname = name
        # Append / for directories or @ for symbolic links
        if os.path.isdir(fullname):
            displayname = name + "/"
            linkname = name + "/"
        if os.path.islink(fullname):
            displayname = name + "@"
            # Note: a link to a directory displays with @ and links with /
        content.append('<li><a href="%s">%s</a>\n'
                % (urllib.parse.quote(linkname), html.escape(displayname)))
    content.append("</ul>\n<hr>\n</body>\n</html>\n")
    
    f.write("".join(content).encode('utf-8'))
    f.seek(0)
    return f
