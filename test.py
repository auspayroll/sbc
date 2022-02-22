import re
import pdb

via = "Via: SIP/2.0/UDP 192.168.56.7:5060;rport;branch=z9hG4bKPjbbb623d6-20c8-4cfa-92ad-f92e37dbf825"
via_pattern = re.compile(r'Via:\s+SIP\/2\.0\/(?P<protocol>UDP|TCP)\s+(?P<host>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(:(?P<port>\d+))?(\s*;\s*rport)?(\s*;\s*branch\s*=\s*(?P<branch>\w+))?', re.IGNORECASE)
match = re.search(via_pattern, via)
pdb.set_trace()
