#!/usr/bin/env python

import sys
import time
import boto
import boto.ec2
import boto.ec2.elb
import boto.utils

from ec2_elb_config import *
from pprint import pprint
from optparse import OptionParser

def get_options():
    parser = OptionParser()

    parser.add_option( "--account",           dest="account",     action="store",      help="select ec2 account %s"%accounts)
    parser.add_option( "-e", "--elb",         dest="elb",         action="store",      help="select ec2 elb")
    parser.add_option( "-m", "--mode",        dest="mode",        action="store",      help="select mode %s"%modes)
    parser.add_option( "-i", "--instance_id", dest="instance_id", action="store",      help="select an instance_id")
    parser.add_option( "-r", "--region",      dest="region",      action="store",      help="select a region"                 , default=default_region)
    parser.add_option( "-d", "--debug",       dest="debug",       action="store_true", help="enable debug"                    , default=default_debug)
    parser.add_option( "--validate",          dest="validate",    action="store_true", help="verify instance belong to elb"   , default=default_validate)

    (options, args) = parser.parse_args()

    if options.mode == 'status':
        if not options.account or not options.elb:
            print "options : " + str(options)
            print "invalid options"
            sys.exit(1)
        return args, options

    if not options.account or not options.elb or not options.mode or not options.instance_id:
        print "options : " + str(options)
        print "invalid options"
        sys.exit(1)

    return args, options

def check_account(account):

    if account not in accounts:
        print "[%s] is an invalid account, please select %s" % ( account, accounts )
        sys.exit(1)

    return account

def check_elb(elb):

    elbs = [ str(i.name) for i in elb_conn.get_all_load_balancers() ]

    if elb not in elbs:
        print "[%s] is an invalid load balancer, please select %s" % ( elb, elbs )
        sys.exit(1)

    return elb

def check_instance_id(instance_id, elb):

    if instance_id not in instance_in_elb[elb]['instances']:
        print "[%s] in not a valid instance_id for load balancer [%s]" % ( instance_id, elb )
        sys.exit(1)

    return instance_id

def check_mode(mode):

    if mode not in modes:
        print "[%s] is not a valid mode, please select %s" % ( mode, modes)
        sys.exit(1)

    return mode

def check_region(region):

    regions = [ str(i.name) for i in boto.ec2.elb.regions() ]

    if region not in regions:
        print "[%s] is not a valid region, please select %s" % ( region, regions )
        sys.exit(1)

    return region

def register_instance_to_elb(mode):

    if instance_id in [ i.instance_id for i in instances_in_elb ]:
        print "instance_id [%s] is already registered to elb [%s] [%s]" % ( instance_id, elb, instance_heath[0].state )
        return
    else:
        print "registering instance [%s]" % (instance_id)
        current_elb.register_instances(instance_id)
    
    check_instance(mode)

def unregister_instance_from_elb(mode):

    if instance_id not in [ i.instance_id for i in instances_in_elb ]:
        print "instance_id [%s] is already unregistered from elb [%s] [%s]" % ( instance_id, elb, instance_heath[0].state )
        return
    else:
        print "unregistering instance [%s]" % (instance_id)
        current_elb.deregister_instances(instance_id)

    check_instance(mode)

def check_instance(mode):

    if mode == 'register':
        status = 'InService'
    else:
        status = 'OutOfService'

    print "checking status ..."
    for retry_count in range (1, check_retry):

        instance_heath = current_elb.get_instance_health(instance_id)
        health = instance_heath[0]

        if health.state == status:
           print "Instance [%s] is now [%s] for elb [%s]" % ( instance_id, status, elb )
           return

        time.sleep(check_interval)

        if debug:
            print instance_heath[0].state

        print " retry_count[%s]" % (retry_count)

    print "Instance [%s] failed to return status [%s] for elb [%s] in the time allowed" %  ( instance_id, status, elb )
    sys.exit(1)

def get_instance_name():

    instance_conn = boto.ec2.connect_to_region(region, aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
    reservations  = instance_conn.get_all_instances(instance_ids=instance_id)
    instance =  [i for r in reservations for i in r.instances]
    for i in instance:
        return i.tags['Name']

def get_elb_status():

    instances_in_elb = current_elb.get_instance_health()
    instance_count   = 0

    print "\ninstances in elb [%s]" % (elb)
    for i in instances_in_elb:
        print i.instance_id
        instance_count += 1
    print "Total Instances : %s" % (instance_count)

if __name__ == "__main__":

    try:
        args, options = get_options()
    except KeyboardInterrupt:
        print "Stopping utility!"
    
    mode        = check_mode(options.mode)
    account     = check_account(options.account)
    region      = check_region(options.region)
    debug       = options.debug
    validate    = options.validate
    
    if validate:
        instance_id = check_instance_id(options.instance_id, options.elb)
    else:
        instance_id = options.instance_id
    
    access_key_id     = elb_account[account]['access_key_id']
    secret_access_key = elb_account[account]['secret_access_key']
    
    instance_name = get_instance_name()
    
    elb_conn         = boto.ec2.elb.connect_to_region( region, aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
    elb              = check_elb(options.elb)

    print "\n=========================================================\n"
    print " load balancer : %s" % (elb)
    if mode != 'status':
        print " instance      : %s" % (instance_id)
        print " instance_name : %s" % (instance_name)
    print "\n account_id    : %s" % (elb_account[account]['account_id'])
    print " account_desc  : %s" % (elb_account[account]['account_desc'])
    print " iam user      : %s" % (elb_account[account]['iam_name'])
    print " region        : %s" % (region)
    print " mode          : %s" % (mode)
    print "\n=========================================================\n"

    current_elb      = boto.ec2.elb.loadbalancer.LoadBalancer(elb_conn, name=elb)
    instances_in_elb = current_elb.get_instance_health()
    instance_heath   = current_elb.get_instance_health(instance_id)
    
    if mode == 'register':
        register_instance_to_elb(mode)
    else:
        if mode == 'unregister':
            unregister_instance_from_elb(mode)
    
    get_elb_status()

    print "\nDone\n" 
