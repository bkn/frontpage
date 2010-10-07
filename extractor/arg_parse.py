import re

class Argparse:
	# Stores actions to take with options as keys.
	opt_arg = {}

	# Extracts matching option-argument pairs from an array. Returns a dictionary mapping options to args.
	def extract(self,arg_list):
		option = re.compile('-.')
		arg_dict = {}
		temp = []
		while len(arg_list) > 0:
			s = arg_list.pop()
			if option.match(str(s)):
				arg_dict[s] = temp
				temp = []
			else:
				temp.append(s)
		return arg_dict

	# Pairs specified option array with action array. Must be string to function mapping.
	def match(self,option, action):
		if (type(option).__name__=='list' and type(action).__name__!='list') or (type(option).__name__!='list' and type(action).__name__=='list'):
			print 'incorrect type of args to arg_parse.match'
		elif type(option).__name__ == 'list' and type(action).__name__ == 'list':
			for i in range(len(option)):
				try:
					if type(action[i]).__name__ != 'function':
						print str(action[i]) + ' must be a function'
						sys.exit(2)
					elif type(option[i]).__name__!= 'str':
						print str(option[i]) + ' must be a string'
						sys.exit(2)
					else:
						self.opt_arg[option[i]] = action[i]
				except IndexError:
					print 'Length of action argument list shorter than option argument list'
					sys.exit(2)
		else:
			if type(action).__name__ != 'function':
				print str(action) + ' must be a function'
				sys.exit(2)
			elif type(option).__name__!= 'str':
				print str(option) + ' must be a string'
				sys.exit(2)
			else:
				self.opt_arg[option] = action

	# Executes the function related to the option with the passed in argument dictionary. ex {'-s':['hi','hello'], '-g':['hey']}
	def execute(self, arg_list):
		if len(arg_list) == 0:
			try:
				self.opt_arg['default']()
			except KeyError:
				print 'Default action not specified'
				try:
					self.opt_arg['usage']()
				except KeyError:
					print 'Usage not specified'
				sys.exit(2)
		else:
			for key in arg_list:
				if key != 'default' and key != 'usage':
					if key in self.opt_arg:
						try:
							self.opt_arg[key](arg_list[key])
						except:
							self.opt_arg[key]()
					else:
						print 'Unrecognized option: ' + key

	# Default function mapping.
	def default(self, funct):
		if type(funct).__name__ == 'function':
			self.opt_arg['default'] = funct
		else:
			print 'default action must be a function'

	# Usage mapping.
	def usage(self, funct):
		if type(funct).__name__ == 'function':
			self.opt_arg['usage'] = funct
		else:
			print 'usage must be a function'
