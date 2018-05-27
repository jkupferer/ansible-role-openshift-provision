# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
      lookup: oc_process
        author: Johnathan Kupferer <jkupfere@redhat.com>
        version_added: "2.5"
        short_description: Return output from oc process
        description:
        - This lookup returns the result of running oc process
        options:
          _terms:
            description: Template file to process
            required: True
          file_template:
            description: Boolean flag to indicate template should be processed as a file
            required: False
          params_file:
            description: Option --params-file value
            required: False
        notes:
        - Currently does not support non-file templates
"""
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()

import json
import subprocess

class LookupModule(LookupBase):

    def run(self, template, variables=None, param_file=None, file_template=False, **kwargs):
        oc_cmd = variables.get('oc_cmd', 'oc').split()

        # lookups in general are expected to both take a list as input and output a list
        # this is done so they work with the looping construct `with_`.
        display.debug("oc process lookup template: %s" % template)
        oc_cmd += ['process','-o','json']
        if file_template:
            oc_cmd += ['-f']
        oc_cmd += template
        if param_file:
            oc_cmd += ['--param-file', param_file]
        output = subprocess.check_output( oc_cmd )
        return [output]
