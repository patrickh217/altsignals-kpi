import os.path
import os

HOST = 'lkdn-db.cimrjryakibb.eu-west-3.rds.amazonaws.com'


# DB parameters to access the Postgre DB
def postgre_access_aws_external():
    host = HOST
    database = 'linkedin_scraper_external'
    port = '5432'
    user = 'postgres'
    password = 'Mach1neL0nd0n'
    return host, port, database, user, password
