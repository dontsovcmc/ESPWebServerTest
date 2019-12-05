
import os
import sys
import difflib
from logger import LOG_DIR, base_name, log


def diff_html(output, templ_dir, templ_name):
    """
    TODO: check ydiff utility
    """

    file_path = os.path.join(templ_dir, templ_name)

    with open(file_path, 'r') as f:
        if sys.version_info > (3, 0):
            tmpl = f.read()
        else:
            tmpl = f.read().decode('utf-8')
        tmpl = tmpl.splitlines()
        output = output.splitlines()

        d = difflib.Differ()
        diffs = [x for x in d.compare(tmpl, output) if x[0] in ('+', '-')]
        if diffs:
            diff = difflib.HtmlDiff().make_file(tmpl, output, '', '', context=True, numlines=3)
            with open(os.path.join(LOG_DIR, base_name + '_diff_' + templ_name), 'w') as f:
                f.write(diff)

            return False
        return True
