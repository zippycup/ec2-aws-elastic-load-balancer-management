# ec2/aws elastic load balancer management

## Description

This is a simple script written in python using boto to manage instance in an elastic load balancer

## Installation

### Requirements

installed the following software:

* **boto** >= 2.34.0
* **python** >= 2.6

amazon ec2
* account iam user with permission to ec2:Describe* and elasticloadbalancing:*
* account id
* access_key_id
* secret_access_key

edit ec2_elb_config.py

```
  accounts = [ 'dev', 'stg', 'prd' ] # These are the account_name you put in elb_account[]

  elb_account['dev'] = { 'account_id'        : '123456789023',
                         'account_desc'      : 'dev env',
                         'iam_name'          : 'elb-user',
                         'access_key_id'     : 'GUJCMHNQUFTVDZXKGPMA',
                         'secret_access_key' : 'FYtgMgy4jUsFL9AN3TrCR7bcha8AhP2qqYM4cYXG',
  }

  #optional validation
  instance_in_elb['dev-elb'] = { 'instances' :
  [
    'i-faae153f',
    'i-1d61bbc6',
    'i-a6409b60',
  ],
  }

```
## Run utility

Optional --validate flag. If your ec2_elb_config.py has the information for instances associated with an elastic load balancer, it will perform the verification.

### status
python ec2_elb.py --account [account_name] --mode status --elb [elb-name] --region [region]

    python ec2_elb.py --account dev --mode status --elb dev-elb -i i-1d61bbc6

    =========================================================

     load balancer : dev-elb

     account_id    : 123456789023
     account_desc  : dev env
     iam user      : elb-user
     region        : us-east-1
     mode          : status

    =========================================================


    instances in elb [dev-elb]
    i-1d61bbc6
    i-faae153f
    Total Instances : 2

    Done

### register
python ec2_elb.py --account [account_name] --mode register --elb [elb-name] -i [instance_id] --region [region]

    python ec2_elb.py --account dev --mode register --elb dev-elb -i i-1d61bbc6 --validate

    =========================================================

     load balancer : dev-elb
     instance      : i-1d61bbc6
     instance_name : dev-app-1

     account_id    : 123456789023
     account_desc  : dev env
     iam user      : elb-user
     region        : us-east-1
     mode          : register

    =========================================================

    registering instance [i-1d61bbc6]
    checking status ...
     retry_count[1]
     retry_count[2]
     retry_count[3]
    Instance [i-1d61bbc6] is now [InService] for elb [dev-elb]

    instances in elb [dev-elb]
    i-1d61bbc6
    i-faae153f
    Total Instances : 2

    Done

### unregister
python ec2_elb.py --account [account_name] --mode unregister --elb [elb-name] -i [instance_id] --region [region]

    python ec2_elb.py --account dev --mode unregister --elb dev-elb -i i-1d61bbc6 --validate

    =========================================================

     load balancer : dev-elb
     instance      : i-1d61bbc6
     instance_name : dev-app-1

     account_id    : 123456789023
     account_desc  : dev env
     iam user      : elb-user
     region        : us-east-1
     mode          : unregister

    =========================================================

    unregistering instance [i-1d61bbc6]
    checking status ...
     retry_count[1]
     retry_count[2]
     retry_count[3]
    Instance [i-1d61bbc6] is now [OutOfService] for elb [dev-elb]

    instances in elb [dev-elb]
    i-faae153f
    Total Instances : 1

    Done
