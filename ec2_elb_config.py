#!/usr/bin/env python

elb_account = {}

check_retry      = 24 
check_interval   = 5
default_debug    = False
default_region   = 'us-east-1'
default_validate = False

accounts = [ 'dev', 'stg', 'prd' ]
modes    = [ 'register', 'unregister', 'status' ]

elb_account['dev'] = { 'account_id'        : '123456789023',
                       'account_desc'      : 'dev env',
                       'iam_name'          : 'elb-user',
                       'access_key_id'     : 'GUJCMHNQUFTVDZXKGPMA',
                       'secret_access_key' : 'FYtgMgy4jUsFL9AN3TrCR7bcha8AhP2qqYM4cYXG',
}

elb_account['stg'] = { 'account_id'        : '234567890123',
                       'account_desc'      : 'stg env',
                       'iam_name'          : 'elb-user',
                       'access_key_id'     : 'TKTMXJQCTLCFKUVBPPVQ',
                       'secret_access_key' : 'n5TkLcz5dCG7gQsDeKZNX3Afd3CuMqmfvMmeN4kR',
}


elb_account['prd'] = { 'account_id'        : '098765432132',
                       'account_desc'      : 'prd',
                       'iam_name'          : 'elb-user',
                       'access_key_id'     : 'RCBSLTWSCDBSAPAOPOGL',
                       'secret_access_key' : '5pyyzzntwMsW9bxsnwdxhNgqv8A547CEKBfEG7YS',
}

############################################################
# Optional if you want to validate an instance against a elb
# use the --validate option

instance_in_elb = {}

instance_in_elb['dev-elb'] = { 'instances' :
[
  'i-faae153f',
  'i-1d61bbc6',
  'i-a6409b60',
],
}

instance_in_elb['stg-elb'] = { 'instances' : 
[ 
  'i-faae153f',
  'i-1d61bbc6',
  'i-a6409b60',
],
}

instance_in_elb['prd-elb'] = { 'instances' : 
[ 
  'i-a177cc64',
  'i-ed8f552b',
  'i-20db7efb',
  'i-de42d21a',
  'i-2ab66cf3',
  'i-86ebaa42',
  'i-a3f2b367',
  'i-30f3b2f4',
  'i-9df2b359',
  'i-06f2b3c2',
  'i-f2a3e336',
  'i-d4a6e610',
  'i-e1a6e625',
  'i-57a5e593',
  'i-67a6e6a3',
  'i-1ca5e5d8',
  'i-4ba7e78f',
  'i-b3a6e677',
  'i-c0cd4719',
  'i-72cd47ab',  
],
}

