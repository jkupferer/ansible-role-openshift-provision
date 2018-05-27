# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
      lookup: file_source
        author: Johnathan Kupferer <jkupfere@redhat.com>
        version_added: "2.5"
        short_description: Get source of multiple files in a directory
        description:
        - This lookup returns the result of running oc process
        options:
          _terms:
            description: Template file or directory to source
            required: True
        notes:
        - Currently does not support non-file templates
"""
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase

import os
import stat

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        basedir = self.get_basedir(variables)

        ret = []
        for term in terms:
            term_file = os.path.basename(term)
            dwimmed_path = self._loader.path_dwim_relative(basedir, 'files', os.path.dirname(term))
            path = os.path.join(dwimmed_path, term_file)

            path_stat = os.stat(path)
            if stat.S_ISREG(path_stat.st_mode):
                with open(path) as f: ret.append(f.read())
            elif stat.S_ISDIR(path_stat.st_mode):
                for root, dirs, files in os.walk(path, topdown=True, followlinks=True):
                    for entry in dirs + files:
                        fpath = os.path.join(root, entry)
                        path_stat = os.stat(fpath)
                        if stat.S_ISREG(path_stat.st_mode):
                            with open(fpath) as f: ret.append(f.read())

        return ret
