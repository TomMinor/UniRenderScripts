#!/usr/bin/python

import sys
import subprocess
import os, os.path
import math
import re
import time
from optparse import OptionParser

usage="""usage: %prog [options] FILE HOSTNAME BEGIN END
ie %prog -r rman myscene.ma w115 0 10"""

description="Render wrangler 0.1"

# -------------------- Globals ------------------------
log_path = os.environ['HOME'] + '/logs'
maya_render ='/opt/autodesk/maya2014-x64/bin/Render'


def split_callback(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))

def printHelpAndExit(parser, message):
    print message + '\n'
    parser.print_help()
    sys.exit(1)

def main():
  parser = OptionParser(usage = usage, description = description)
  parser.add_option("-r", "--renderer", 
                    dest="renderer", 
                    help="Which renderer to use? [rman]", 
                    default='rman')
  parser.add_option("-p", "--package", 
                    dest="package", 
                    help="Which software package to expect? [maya]", 
                    default='rman')
  parser.add_option("--res", 
                    dest="resolution", 
                    type='string',
                    help="Override render resolution", 
                    action='callback', 
                    callback=split_callback)
  parser.add_option("--hosts", 
                    dest="hosts", 
                    type='string',
                    help="Which host machines to use e.g --hosts w323,0,10,w115,0,90", 
                    action='callback', 
                    callback=split_callback)
  parser.add_option("-s", "--startFrame", 
                    dest="startFrame", 
                    default=0, 
                    type=int,
                    help="Start frame")
  parser.add_option("-e", "--endFrame", 
                    dest="endFrame", 
                    default=0, 
                    type=int,
                    help="End frame")
  parser.add_option("-u", "--user", 
                    dest="user", 
                    default='', 
                    type='string',
                    help="The user to begin the render with")
  parser.add_option('--dry-run', action='store_true', dest='dryrun')
  parser.add_option('-v', '--verbose', action='store_true', dest='verbose')
  parser.add_option('--test-ssh', action='store_true', dest='testSSH')
  parser.add_option('--getProgress', action='store_true', dest='getProgress')
  parser.add_option('--printCmd', action='store_true', dest='printcmd')

  (options, args) = parser.parse_args()
  options = vars(options)

  if len(args) != 1:
    printHelpAndExit(parser, "Error: 1 argument expected")

  if options['hosts'] == None:
    printHelpAndExit(parser, "Error: No hosts supplied")

  renderFile = args[0]
  if not os.path.isfile(renderFile):
    printHelpAndExit(parser, "Error: Scene file does not exist")

  # Dissect into (host, startNum, endNum)
  hostInput = zip(*[iter(options['hosts'])]*3)
  hosts = []
  for hostData in hostInput:
    hostRoom, hostStart, hostEnd = hostData

    try:
      hostStart = int(hostStart)
      hostEnd  = int(hostEnd)
    except ValueError:
      printHelpAndExit(parser, "Error: Host limits are invalid")

    for i in range(hostStart, hostEnd):
      host = hostRoom + str(i).zfill(2)
      hosts.append(host)

  #try:
  #  hostLower = int(args[2])
  #  hostUpper = int(args[3]) 
  #except ValueError:
  #  pass

  #hostRoom = args[1]

  # ------------------------ Verify hosts --------------------------
  validHosts = []
  invalidHosts = []
  #for hostID in xrange(hostLower, hostUpper + 1):
  #  host = hostRoom + str(hostID).zfill(2)
  for host in hosts:
    ret = subprocess.call(['getent', 'hosts', host], stdout=subprocess.PIPE)

    #ToDo: Add host blacklist for broken hosts (or more tests)
    if ret == 0 and host != "w32320" and host != "w11549":
      # Assume we were successful
      validHosts.append(host)
    else:
      # Assume something went wrong
      invalidHosts.append(host)

  if len(validHosts) == 0:
    print "Error: No valid hosts found"
    sys.exit(1)
  elif len(invalidHosts) > 1:
    print "Warning: Invalid hosts detected" 
    print "These will be ignored: "+ str(invalidHosts)

  if options['endFrame'] < options['startFrame']:
      printHelpAndExit(parser, "Error: Frame range is invalid")

  totalHosts = len(validHosts)
  totalFrames = options['endFrame'] - options['startFrame'] + 1
  framesPerHost = int( (float(totalFrames) / float(totalHosts)) )
  remainder = totalFrames - (framesPerHost * totalHosts) # It's unlikely we'll get a perfect fit

  if totalFrames < totalHosts:
    print ""
    print "Warning: Not enough frames to satisfy 1 frame per host, ignoring unused hosts"
    for i in xrange(totalHosts - totalFrames):
      validHosts.pop()
    totalHosts = totalFrames
    framesPerHost = 1
    remainder = 0

  # ------------------------ Print Info --------------------------
  print "\n--------------- Host Info ---------------"
  print "Total Valid Hosts : " + str(totalHosts)
  print "Hosts : " 
  for host in validHosts: 
    print '\t\t' + host

  print "\n--------------- Frame Info ---------------"
  print "Total Frames: " + str(totalFrames)
  print "Frames Per Host: " + str(framesPerHost)
  print "Remainder Frames: " + str(remainder)

  if not os.path.exists(log_path):
    os.makedirs(log_path)

  # ------------------------ Begin Renders --------------------------
  jobRanges = []
  currentFrame = options['startFrame']

  if options['startFrame'] == options['endFrame']:
    jobRanges.append( (options['startFrame'], options['endFrame'] ) )
  else:
    for i, host in enumerate(validHosts):
		a = currentFrame
		b = currentFrame + framesPerHost
		if remainder > 0:
			remainder -= 1
			b += 1

		if( i == totalHosts):
			jobRanges.append( (a, totalFrames) )
		else:
			jobRanges.append( (a, b) )

		currentFrame = b 

  for i, job in enumerate(jobRanges):
    presetup = 'export MAYA_RENDER_DESC_PATH=/opt/pixar/RenderManStudio-19.0-maya2014/etc; source ~/fixRmanCl.sh;'
    renderCommands = [presetup, maya_render, '-r', options['renderer'], '-s', str(job[0]), '-e', str(job[1]), renderFile]

    #if options['verbose']:
    renderCommands.insert(2, '-verb')

    res = options['resolution']
    if res and res[0] != 0 and res[1] != 0:
      renderCommands.insert(2, '-res {0} {1}'.format(res[0], res[1]))

    renderDateTime = time.strftime("%d_%m_%Y/%H_%M_%S")
    currentLogPath = log_path + '/' + options['renderer'] + '/' + renderDateTime + '/'
    if not os.path.exists(currentLogPath):
      os.makedirs(currentLogPath)
    hostName = validHosts[i]

    renderCommands.append('>' + currentLogPath + hostName + '.log')
    renderCommands.append('2>' + currentLogPath + hostName + '_error.log')

    sshCommands = ['ssh', '-oStrictHostKeyChecking=no -oPasswordAuthentication=no -oBatchMode=yes -oNumberOfPasswordPrompts=0', validHosts[i]]

    commands = sshCommands

    finalCommands = ""
    if options['getProgress']:
      print "Progress [" + hostName + "] : "
      commands.append( '"ps aux | grep prman | grep -v grep"'  )
      finalCommands = ' '.join(commands)
      pid = subprocess.Popen(finalCommands, universal_newlines=True, shell=True).pid
    elif options['testSSH']:
      print "Testing SSH..."
      commands.append( '"echo \$(hostname)"'  )
      finalCommands = ' '.join(commands)
      pid = subprocess.Popen(finalCommands, universal_newlines=True, shell=True).pid
    elif options['dryrun'] == None:
      catRenderCommands =  ' '.join(renderCommands)
      commands.append( '"' + catRenderCommands + '"'  )
      finalCommands = ' '.join(commands)
      pid = subprocess.Popen(finalCommands, universal_newlines=True, shell=True).pid
    else:
      pid = 0

    if options['printcmd']:
      print finalCommands

    if not options['getProgress']:
      print str(hostName) + " PID : " + str(pid) + " " + str(job[0]) + "-" + str(job[1])

if __name__ == '__main__':
  main()
