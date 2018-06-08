# template.py
# Rohan Weeden
# Created: May 24, 2018

# Holds the troposphere template object used to create the hyp3-in-a-box
# cloudformation stack

from troposphere import Template

t = Template()
t.add_description(
    "ASF HyP3 system"
)
