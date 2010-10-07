import json, glob, codecs, time, os, arg_parse, sys, re

files = []
meta_records = []
file_types = []
rlvl = 0

def update():
	global files, meta_records, rlvl, file_types
	metaset_bibjs = re.compile('metaset.bibjs')
	for i in range(rlvl+1):
		for types in file_types:
			temp = glob.glob('./' + '*/'*i + '*.' + types)
			if len(temp) > 0:
				for string in temp:
					if not(string in files):
						files.append(string)

	temp = glob.glob('metaset.bibjs')

	for file_records in files:
		if metaset_bibjs.search(file_records):
			files.remove(file_records)
			metaset_file = codecs.open(file_records, 'r', 'utf-8')
			update_file = json.load(metaset_file)
			meta_records = update_file['recordList']
			metaset_file.close()
		elif len(temp)>0:
			metaset_file = codecs.open('metaset.bibjs', 'r', 'utf-8')
			try:
				update_file = json.load(metaset_file)
				meta_records = update_file['recordList']
			except:
				print 'ill formatted metaset.bibjs'
			metaset_file.close()

	extract()

def find(name):
	global meta_records
	if len(meta_records) != 0:
		for i in range(len(meta_records)):
			if name == meta_records[i]['name']:
				return i
		return -1
	else:
		return -1

def extract():
	global meta_records, files
	meta_format = {'dataset':{}, 'recordList':[]}

	meta_format['dataset']['name'] = 'metaset.bibjs'
	meta_format['dataset']['type'] = 'metadataset'
	meta_format['dataset']['id'] = ''
	meta_format['dataset']['description'] = 'Metadata Set'
	meta_format['dataset']['source'] = ''
	meta_format['dataset']['table_cols'] = ["name", "size", "records", "description"]
	meta_format['dataset']['creator'] = ''
	meta_format['dataset']['curator'] = ''
	meta_format['dataset']['linkage'] = ["http://www.bibkn.org/drupal/bibjson/iron_linkage.json"]

	for fp in files:
		fin = codecs.open(fp, 'r', 'utf-8')
		try:
			bibjs_obj = json.load(fin)
		except:
			print 'failed to load file: ' + fp
			continue
		if type(bibjs_obj).__name__ != 'dict':
			print 'not dictionary: ' + fp
			continue
		else:
			try:
				meta_data = bibjs_obj['dataset']
				i = find(fp)
				if i == -1:
					
					meta_data['name'] = bibjs_obj['dataset']['name']
					meta_records.append(meta_data)
				else:
					if meta_data['createdDate'] != meta_records[i]['createdDate']:
						meta_records.pop(i)
						meta_records.append(meta_data)
				fin.close()
			except:
				print 'no dataset property in: ' + fp

	meta_format['recordList'] = meta_records
	meta_format['dataset']['records'] = len(meta_format['recordList'])

	fout = codecs.open('metaset.bibjs', 'wa', 'utf-8')
	json.dump(meta_format, fout, indent=2)
	fout.close()
	file_stats = os.stat('metaset.bibjs')
	fin = codecs.open('metaset.bibjs', 'r', 'utf-8')
	metaset = json.load(fin)
	fin.close()

	if file_stats.st_size < 1024:
		metaset['dataset']['size'] = str(file_stats.st_size) + ' B'
	elif file_stats.st_size < 1048576:
		metaset['dataset']['size'] = ("%.2f" % (file_stats.st_size/1023.0)) + ' KB'
	else:
		metaset['dataset']['size'] = ("%.2f" % (file_stats.st_size/1048575.0)) + ' MB'

	metaset['dataset']['createdDate'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_stats.st_ctime))
	fout = codecs.open('metaset.bibjs', 'wa', 'utf-8')
	json.dump(metaset, fout, indent=2)
	fout.close()

def type_file(types):
	global file_types
	file_types.extend(types)

def set_recursion_lvl(x):
	global rlvl
	if type(x).__name__ == 'list':
		if len(x) ==1:
			rlvl = int(x[0])
		else:
			print 'Incorrect num of args to -r'

def default():
	global file_types, rlvl
	file_types.append('json')
	rlvl = 1

def usage():
	print 'usage: metaset_extracter.py [option] ... [-t type] [-r num] [-h] default= all *.json files in 1 lvl of recursion.'
	print 'Options and arguments'
	print '-t: specify file type'
	print '-r: directory depth of search'
	print '-h: print usage'

def main():
	arg_handler = arg_parse.Argparse()
	arg_list = arg_handler.extract(sys.argv[1:])
	arg_handler.match(['-t','-r','-h'], [type_file, set_recursion_lvl, usage])
	arg_handler.default(default)
	arg_handler.usage(usage)
	arg_handler.execute(arg_list)
	update()


if __name__ == "__main__":
	main()
