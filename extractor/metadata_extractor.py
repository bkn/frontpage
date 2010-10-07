import json, glob, codecs, datetime, sys, os, time, getopt, re, arg_parse

files = []

def spec_files(f, rlvl):
	global files
	for i in range(rlvl+1):
		for fp in f:
			temp = glob.glob('./' + '*/'*i + fp)
			if len(temp)> 0:
				for string in temp:
					if not(string in files):
						files.append(string)

def type_file(f, rlvl):
	global files
	for i in range(rlvl+1):
		for ftype in f:
			temp = glob.glob('./' + '*/'*i + '*.' +ftype)
			if len(temp)>0:
				files.extend(temp)

def all_files():
	global files
	files = glob.glob('./*/*.json')

def extract():
	global files
	datasets = []
	exclude_id = re.compile('identifiers')
	exclude_type = re.compile('type_hints')

	if 'metaset.bibjs' in files:
		files.remove('metaset.bibjs')
	for i in range(len(files)):
		if not(exclude_id.search(files[i]) or exclude_type.search(files[i])):
			datasets.append(files[i])

	for fp in datasets:
		fin = codecs.open(fp, 'r', 'utf-8')
		try:
			bibjs_obj = json.load(fin)
		except:
			print 'failed to load file: ' + fp
			fin.close()
			continue
		if type(bibjs_obj).__name__ != 'dict':
			print 'not dictionary: ' + fp
			fin.close()
		else:

			if not ('dataset' in bibjs_obj):
				bibjs_obj['dataset'] = {}
	#			bibjs_obj['dataset']['type'] = 'dataset'
	#			bibjs_obj['dataset']['id'] = ''
	#			bibjs_obj['dataset']['description'] = fp + ' dataset'
	#			bibjs_obj['dataset']['source'] = ''
	#			bibjs_obj['dataset']['creator'] = ''
	#			bibjs_obj['dataset']['curator'] = ''
	#			bibjs_obj['dataset']['schema'] = ''
	#			bibjs_obj['dataset']['linkage'] = ''

			file_name = fp.split('/')
			filename_rm_ext = file_name[len(file_name)-1].split('.')[0]
			bibjs_obj['dataset']['name'] = filename_rm_ext
			bibjs_obj['dataset']['id'] = '@' + filename_rm_ext.lower()
			try:
				bibjs_obj['dataset']['records'] = len(bibjs_obj['recordList'])
			except:
				print 'No recordList property in: ' + fp
				fin.close()
				continue

			fin.close()
			fout = codecs.open(fp, 'w', 'utf-8')
			json.dump(bibjs_obj, fout, indent=2)
			fout.close()

			file_stats = os.stat(fp)
			fin = codecs.open(fp, 'r', 'utf-8')
			metaset = json.load(fin)
			fin.close()

			if file_stats.st_size < 1024:
				metaset['dataset']['size'] = str(file_stats.st_size) + ' B'
			elif file_stats.st_size < 1048576:
				metaset['dataset']['size'] = ("%.2f" % (file_stats.st_size/1023.0)) + ' KB'
			else:
				metaset['dataset']['size'] = ("%.2f" % (file_stats.st_size/1048575.0)) + ' MB'

			metaset['dataset']['createdDate'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_stats.st_ctime))
			fout = codecs.open(fp, 'wa', 'utf-8')
			json.dump(metaset, fout, indent=2)
			fout.close()

#parser = argparse.ArgumentParser(description='Extract metadata from bibjs datasets.')
#parser.add_argument('files', metavar='file.bibjs', nargs='+',
#                   help='Files to create/update metadata.')
#parser.add_argument('-f', dest='extract', action='store_const',
#                   const=spec_files, default=all_files,
#                   help='Extract metadata from specified .bibjs datasets in same directory. (default: extract all .bibjs datasets in same directory.)')

#args = parser.parse_args()
#args.extract(args.files)

def usage():
	print 'usage: metadata_extracter.py [option] ... [-s files] [-t type] [-r num] [-h] default= all *.json files in 1 lvl of recursion.'
	print 'Options and arguments'
	print '-s: exact files'
	print '-t: specify file type'
	print '-r: directory depth of search'
	print '-h: print usage'

def main():
	arg_handler = arg_parse.Argparse()
	arg_list = arg_handler.extract(sys.argv[1:])
	if len(arg_list) == 0:
		all_files()
	for key in arg_list:
		if key == '-s' or key == '--specific':
			if '-r' in arg_list:
				if type(arg_list['-r']).__name__ == 'list':
					if len(arg_list['-r']) == 1:
						if type(arg_list['-r'][0]).__name__ == 'str':
							type_file(arg_list[key], int(arg_list['-r'][0]))
						elif type(arg_list['-r'][0]).__name__ == 'int':
							type_file(arg_list[key], arg_list['-r'][0])
						else:
							print 'incorrect type to -r'
							sys.exit(2)
					else:
						print 'incorrect num of args to -r'
						sys.exit(2)
				elif type(arg_list['-r']).__name__ == 'int':
					type_file(arg_list[key], arg_list['-r'])
				else:
					print 'value specified for -r must be an int'
					sys.exit(2)
			else:
				spec_files(arg_list[key],1)
		elif key == '-t' or key == '--file-type':
			if '-r' in arg_list:
				if type(arg_list['-r']).__name__ == 'list':
					if len(arg_list['-r']) == 1:
						if type(arg_list['-r'][0]).__name__ == 'str':
							type_file(arg_list[key], int(arg_list['-r'][0]))
						elif type(arg_list['-r'][0]).__name__ == 'int':
							type_file(arg_list[key], arg_list['-r'][0])
						else:
							print 'incorrect type to -r'
							sys.exit(2)
					else:
						print 'incorrect num of args to -r'
						sys.exit(2)
				elif type(arg_list['-r']).__name__ == 'int':
					type_file(arg_list[key], arg_list['-r'])
				else:
					print 'value specified for -r must be an int'
					sys.exit(2)
			else:
				type_file(arg_list[key], 1)
		elif key == '-h' or key == '--help':
			usage()
		elif key != '-r':
			print 'unhandled option: \"' + key + '\"'
			sys.exit(2)

	extract()

"""
	try:
#		opts, args = getopt.getopt(sys.argv[1:], "hes", ["help", "--files-type=", "specific="])
	except getopt.GetoptError, err:
		# print help information and exit:
		# will print something like "option -a not recognized"
		print str(err)
		usage()
		sys.exit(2)

	for key, value in opts:
		if key in ("-s", "--specific"):
			print args
#			spec_files(args)
#			sys.exit()
		elif key in ("-e", "--file-type"):
			print args
		elif key in ("-h", "--help"):
			usage()
			sys.exit()
		else:
			assert False, "unhandled option"

#	all_files()
"""
if __name__ == "__main__":
    main()
