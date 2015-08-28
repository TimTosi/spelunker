#!/usr/bin/python

import os
import glob
import ConfigParser
import blockparser.BlockParser as BlockParser
import postgreDb.DatabaseWrapper as DatabaseWrapper
import clusterizer.Clusterizer as Clusterizer

def initConfig():
	if os.path.isfile("./config.ini") != True:
		print "config.ini missing."
		return False
	config = ConfigParser.ConfigParser()
	config.read("./config.ini")
	settings = {}
	dirName = config.get("Config", "dataDirectory")
	settings["dirList"] = sorted(glob.glob(''.join([dirName, "blk*.dat"])))
	databaseName = config.get("Config", "databaseName")
	userName = config.get("Config", "userName")
	userPassword = config.get("Config", "userPassword")
	if not databaseName or not userName:
		print "Error: Database name or User Name is missing."
		exit()
	settings["dbCredentials"] = "dbname='%s' user='%s' password='%s'" % (databaseName, userName, userPassword)
	return settings


if __name__ == '__main__':
	settings = initConfig()
	db = DatabaseWrapper.DatabaseWrapper(settings["dbCredentials"])
	db.setDatabaseEnv()
	parser = BlockParser.BlockParser(db, settings)
	parser.parse()
	clusterizer = Clusterizer.Clusterizer(db)
	clusterizer.clusterize()