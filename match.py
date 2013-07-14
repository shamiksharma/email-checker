import sys
import re
import difflib

"""
This method takes an email, a list of names e.g [firstname, lastname] 
and returns the confidence level of whether the email fuzzy-matches the user name

It depends on python's built-in difflib which computes distance between
two strings.

Usage is as shown below in the main function.

This can be also used from command-line using

% python match.py  janedoe123@gmail.com  "jane doe"

"""

def matcher (full_email, full_name):

   if full_name:
     names = full_name.split()

   #
   # Extract name part of the email
   # Ideally, also compute all email variants
   #
   match = re.search('([\w.-]+)@([\w.-]+)', full_email)
   if match:
     email = match.group()
     email_name = match.group(1).lower()

   #
   # Use all kinds of joining characters between names
   #

   joiners = ['','-','.','_']
   name_variants = []

   for joiner in joiners:
      joinedname = joiner.join(names)
      name_variants.append(joinedname)
   names = names + name_variants

   #
   #  add all the variants to the name
   #
   conf = 0.0

   #
   #  find the best match between all the variants of the user name
   #

   for name in names:
      similarity = difflib.SequenceMatcher(None, name, email_name).ratio()
      conf = max (conf, similarity)
      # print conf, email, name

   return conf


#-------------------------------------------------


def usage (msg):
   print msg
   print "Pass in  [email] [name]"
   print '% match  jdoedeer@gmail.com   \"jane doe\"'
   return -1

#-------------------------------------------------

def main(argv=None):

  #
  # argv is set to sys.argv if not provided.
  #
  if argv is None:
     argv = sys.argv
  if len(argv) < 3:
     return usage("Too few arguments")

  #
  # get email and full name from args
  #
  full_email = argv[1]
  full_name  = argv[2]
  confidence = 0.0
  email_name = None 

  #
  #  Just verify that email is a valid email
  #
  match = re.search('([\w.-]+)@([\w.-]+)', full_email)
  if match:
     email = match.group()
     email_name = match.group(1).lower()
  if not email_name: 
     return usage ("%s is not a valid email" % email_raw)
  if not full_name:
     return usage ("%s is not a valid name" % name_raw)


  #
  #  Confidence is based on email and name.
  #
  confidence = matcher (full_email, full_name)

  print "%0.2f  %s  %s"  % (confidence, full_email, full_name)

#-------------------------------------------------

if __name__ == "__main__":
   sys.exit(main())

#-------------------------------------------------
