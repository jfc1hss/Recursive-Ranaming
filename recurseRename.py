recurseRename

import os, sys, re, itertools, time, shutil, csv, win32com.client
from stat import *

start_time = time.time()
itemcount = 0
changesmade = 0
Bytes_used = 0
changes = [["Root","Original","New name"]]
acad_dwgs = 0
acad_changes = 0

outputFile = open((os.path.join(sys.argv[1], 'Name Change Record.csv')), 'a', newline='')
outputWriter = csv.writer(outputFile)

fileregex = re.compile(r'''
	#Place regex here
	''', re.VERBOSE)

def walktree(top, callback, end):
	'''recursively descend the directory tree rooted at top,
	calling the callback function for each regular file'''
	try: 
		os.mkdir(os.path.join(top, "Originals"))	
	except OSError:
		pass
	for f in os.listdir(top):
		if f != "Originals":
			global itemcount
			itemcount += 1
			pathname = os.path.join(top, f)
			mode = os.stat(pathname).st_mode
			filematch = fileregex.search(os.path.split(pathname)[1])
			if pathbreak(pathname, "users") == False:
			# i.e if it's not an SS folder
				if S_ISDIR(mode):
					# It's a directory, recurse into it
					walktree(pathname, callback, end)
					callback(pathname, top)
				elif S_ISREG(mode) and filematch != None:
					shutil.copy(pathname, os.path.join(os.path.split(pathname)[0], "Originals"))
				# It's a file, call the callback function
					callback(pathname, top)
				else:
					# Unknown file type, print a message
					print('Skipping %s' % pathname)
		else:
			pass

def pathbreak(pathname, end):
	result = list((os.path.split(pathname)))
	result.append(os.path.split(result[0]))
	count = 2
	
	while end not in (itertools.chain.from_iterable(result)):
		result.append(os.path.split(result[count][0]))
		count+=1
	
	chained_list = [word.lower() for word in itertools.chain.from_iterable(result)]
	return("Place name of folder to avoid here" in chained_list or "Place name of folder to avoid here" in chained_list)
	
def visitfile(pathname, top):
	filematch = fileregex.search(os.path.split(pathname)[1])
	if filematch!=None:
		filename=filematch.group()
	    
		First = filematch.group(1)
		Second = filematch.group(2)
		Penultimate = filematch.group(n-1)
		Last = filematch.group(n)
				
		global changesmade, Bytes_used, changes
		changesmade += 1
		Bytes_used += ((os.stat(pathname)[6]))
		filename = os.path.split(pathname)
		fileext = os.path.splitext(pathname)
		
		print(filename, fileext)
	
		newName = ("shuffle regex components here, can be concatenated with constants" + ext)
		os.rename(pathname, newName)
		print(pathname)
		update = [os.path.split(pathname)[0],os.path.split(pathname)[1],os.path.split(newName)[1]]
		changes.append(update)
	else:
		pass


if __name__ == '__main__':
	walktree(sys.argv[1], visitfile, "users")
	
print("\n\t\t\t\tResult Summary:\n")
print("\n\t\t\t\tScript run on: ", time.strftime("%d/%m/%Y"), " at: ", time.strftime("%H:%M:%S"))
print("\t\t\t\tPath used: ", sys.argv[1], "\n")
print("\t\t\t\tItems checked = ", itemcount)
print("\t\t\t\tChanges made = ", changesmade)
print("\n\t\t\t\tThe script took", round((time.time() - start_time), 2),"seconds to complete.")
print("\t\t\t\tDuplicating the files required an additional: ", round((Bytes_used/(1024*1024)), 1) ," MB\n" )

for row in changes:
		outputWriter.writerow(row)
outputFile.close()

#pathname = the path of the file, equal to top + f
#top = the path without the file/dir name
#f = the file/dir name to be changed
#callback = the secondary function referred back to when the script is called. i.e. "visitfile"