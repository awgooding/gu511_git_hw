#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: dbconnections.py
Author: zlamberty
Created: 2017-11-13

Description:
    integrate `boto3` into our database connection methods for `postgres`

Usage:
    <usage>

"""

import argparse
import getpass

import boto3
import pandas as pd
import psycopg2
import sqlalchemy


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #


# ----------------------------- #
#   boto3 to connection info    #
# ----------------------------- #

def get_instance_info(dbid, profile_name=None):
    """given an `rds` database instance id name and an optional `aws cli`
    profile, get the database instance info

    """
    if profile_name:
        session = boto3.session.Session(profile_name=profile_name)
    else:
        session = boto3.session.Session()

    rds = session.client('rds')

    # get the database instance information for the `rds` database instance with
    # id `dbid`. dont' forget to actually *use* that `dbid` value...
    # name it `dbinfodict` and return it below
    # ------------- #
    dbinfodict = rds.describe_db_instances()
    #instances = rds.get_all_dbinstances()
    #dbinfodict = rds.describe_instances()
    # ------------- #

    return dbinfodict


def sql_connection_params(dbid, profile_name=None):
    """given an `rds` database instance id name and an optional `aws cli`
    profile, get the database connection information for `psycopg2` and
    `sqlalchemy` connections

    """
    dbinfodict = get_instance_info(dbid, profile_name=profile_name)
    host = dbinfodict['DBInstances'][0]['Endpoint']['Address']
    port = dbinfodict['DBInstances'][0]['Endpoint']['Port']
    dbname = dbinfodict['DBInstances'][0].get('DBName', 'postgres')
    user = dbinfodict['DBInstances'][0]['MasterUsername']
    return host, port, dbname, user


# ----------------------------- #
#   psycopg2                    #
# ----------------------------- #

def make_psycopg2_connection(dbid, profile_name=None):
    password = getpass.getpass("psql password: ")
    host, port, dbname, user = sql_connection_params(dbid,
                                                     profile_name=profile_name)
    # create a connection to the database using the `psycopg2.connect` method
    # *don't forget to return it!*
    # ------------- #
    connection = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        dbname=dbname)
    # ------------- #

    return connection

# ----------------------------- #
#   sqlalchemy                  #
# ----------------------------- #

def make_sqlalchemy_engine(dbid, profile_name=None):
    password = getpass.getpass("psql password: ")
    host, port, dbname, user = sql_connection_params(dbid,
                                                     profile_name=profile_name)
    # use `sqlalchemy.engine.url.URL` to build up a database connection url.
    # name it `url`
    # ------------- #
    url = sqlalchemy.engine.url.URL(
        drivername='postgres+psycopg2',
        username=user,
        password=password,
        host=host,
        port=port,
        database=dbname
    )
    #sqlalchemy.engine.url.make_url(url)
    # ------------- #

    # use the `sqlalchemy.create_engine` function and the `url` you just created
    # to build and return `sqlalchemy` engine.
    # *don't forget to return it*
    # ------------- #
    engine = sqlalchemy.create_engine(url)
    # ------------- #
    return(engine)


# ----------------------------- #
#   testing our connections     #
# ----------------------------- #

def test_connections(dbid, profile_name=None):
    qry = "SELECT * FROM pg_database;"

    print('accessing our database using psycopg2 directly')
    with make_psycopg2_connection(dbid, profile_name=profile_name) as conn:
        df1 = pd.read_sql(qry, conn)

    print('accessing our database using psycopg2 via sqlalchem')
    engine = make_sqlalchemy_engine(dbid, profile_name=profile_name)
    df2 = pd.read_sql(qry, engine)

    assert df1.equals(df2)

    print("test passed! everything is all good.")
    return df1


# ----------------------------- #
#   Command line                #
# ----------------------------- #

def parse_args():
    parser = argparse.ArgumentParser()

    dbid = "rds database id (name at top of the instance page in the web console)"
    parser.add_argument("-d", "--dbid", help=dbid, required=True)

    profile_name = "optional aws configure profile name"
    parser.add_argument("-p", "--profile_name", help=profile_name)

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    test_connections(dbid=args.dbid, profile_name=args.profile_name)