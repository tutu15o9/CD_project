# defining registers with their initial values.
# 01=A, 02=B, ...., 06=F

registers={'01': 0, '02': 0, '03': 0, '04': 0, '05': 0, '06': 0}
mem=0

# defining flag initially set to 0
flag=0

# all commands allowed in interpreter.
commands={'101': 'print', '102': 'add', '103': 'sub', '104': 'mul', '105': 'div', '106': 'mod', '107': 'inc', '108': 'dec', '109': 'band', '110': 'bor',
		 '111': 'bxor', '201': 'and', '202': 'or', '205': 'equal', '206': 'gt', '207': 'lt', '208': 'gte',
		  '209': 'lte', '210': 'cmp', '301': 'mov', '302': 'mvi', '304': 'sta',
		  '401': 'jmp', '402': 'jt', '403': 'jf', '501': 'push', '502': 'pop', '100': 'hlt', '200': 'nop', '400': 'inp'}

# defining stack which will store registers and flag when any function call is  made
stack=[]
fileName='a.txt'

# function to print argument and exit code execution
def exit0(argument):
	print(argument)
	exit()

# defining memory of size 2000
memory=[]
for i in range(2000):
	memory.append(0)

# opening file containing the assembly code and stored it line by line
with open(fileName) as f:
    line = f.readlines()

inputline={}
z=1

# removing /n tag from each line and splitting on basis of space(' ')
for i in line:
	if(i[0]=='#'):
		i='200\n'
	inputline[z]=i[:-1].split()
	if(len(inputline[z])==0):
		inputline[z]=['200']
	z=z+1

inputline[len(line)]=line[len(line)-1].split()

# pc is program counter=>will keep number of next line to be executed.
# and cc is current counter=> will keep number of current line which is being executed.

pc=1
cc=0
while(cc<len(inputline)):
	cc=pc
	pc=pc+1
	line=inputline[cc]
	# print(line)

	# error if invalid command
	if line[0] not in commands:
		exit0('invalid command at line number '+str(cc))


	#print operation=> print A/B/C/D/E/F
	elif(commands[line[0]]=='print'):
		if(len(line)>2):
			exit0('too many arguments at line number '+str(cc))
		elif(line[1] not in registers):
			exit0('invalid argument at line number '+str(cc)+'. Please enter a register.')
		else:
			print(registers[line[1]])

	# nop operation=>skip the line
	elif(commands[line[0]]=='nop'):
		if(len(line)>1):
			exit0('too many arguments at line number '+str(cc))
		else:
			pass
			
	# hlt operation=> terminate the execution of program
	elif(commands[line[0]]=='hlt'):
		if(len(line)>1):
			exit0('too many arguments at line number '+str(cc))
		else:
			exit0('execution completer at line number '+str(cc))

	# mov operation, move value of a register into another register => mov A B => A=B
	elif(commands[line[0]]=='mov'):
		if(len(line)>3):
			exit0('too many arguments at line number '+str(cc))
		if('07' in line):
			memAddr=registers['05']*100+registers['06']
			if(memAddr>2000):
				exit0('memory address out of range. Error at line number '+str(cc))
			if(line[1]=='07' and line[2] in registers):
				memory[memAddr]=registers[line[2]]
			elif(line[1] in registers and line[2]=='07'):
				registers[line[1]]=memory[memAddr]
			else:
				exit0('invalid argument at line number '+str(cc)+'. Please enter a register.')
		elif(line[1] not in registers or line[2] not in registers):
			exit0('invalid argument at line number '+str(cc)+'. Please enter a register.')
		else:
			registers[line[1]]=registers[line[2]]

	# mvi operation, move value of a immediate into given register => mvi A 10 => A=10 
	elif(commands[line[0]]=='mvi'):
		if(len(line)>3):
			exit0('too many arguments at line number '+str(cc))
		if(line[1]=='07'):
			memAddr=registers['05']*100+registers['06']
			if(memAddr>2000):
				exit0('memory address out of range. Error at line number '+str(cc))
			else:
				memory[memAddr]=int(line[2])
		elif(line[1] not in registers):
			exit0('invalid argument at line number '+str(cc)+'. Please enter a register.')
		else:
			registers[line[1]]=int(line[2])
			

	# # mvm operation, move value stored at memory address into given register => mvm A 1000 => A=[1000]
	# elif(commands[line[0]]=='mvm'):
	# 	if(len(line)>3):
	# 		exit0('too many arguments at line number '+str(cc))
	# 	elif(line[1] not in registers):
	# 		exit0('invalid argument at line number '+str(cc)+'. Please enter a register.')
	# 	else:
	# 		registers[line[1]]=memory[int(line[2])]
			
	# sta operation, move value stored into given register at given memory address  => sta A 1000 => [1000]=A
	elif(commands[line[0]]=='sta'):
		if(len(line)>3):
			exit0('too many arguments at line number '+str(cc))
		elif(line[1] not in registers):
			exit0('invalid argument at line number '+str(cc)+'. Please enter a register.')
		else:
			memory[int(line[2])]=registers[line[1]]
			
	# add operation, add values of two registers and put into first one => add A B => A=A+B
	elif(commands[line[0]]=='add'):
		if(len(line)>3):
			exit0('too many arguments at line number '+str(cc))
		elif(line[1] not in registers or line[2] not in registers):
			exit0('invalid argument at line number '+str(cc)+'. Please enter a register.')
		else:
			registers[line[1]]+=registers[line[2]]

	# sub operation, subtract values of two registers and put into first one => sub A B => A=A-B
	elif(commands[line[0]]=='sub'):
		if(len(line)>3):
			exit0('too many arguments at line number '+str(cc))
		elif(line[1] not in registers or line[2] not in registers):
			exit0('invalid argument at line number '+str(cc)+'. Please enter a register.')
		else:
			registers[line[1]]-=registers[line[2]]

	# mul operation, multiply values of two registers and put into first one => mul A B => A=A*B
	elif(commands[line[0]]=='mul'):
		if(len(line)>3):
			exit0('too many arguments at line number '+str(cc))
		elif(line[1] not in registers or line[2] not in registers):
			exit0('invalid argument at line number '+str(cc)+'. Please enter a register.')
		else:
			registers[line[1]]*=registers[line[2]]

	# div operation, divide value of two registers and put into first one => add A B => A=A/B
	elif(commands[line[0]]=='div'):
		if(len(line)>3):
			exit0('too many arguments at line number '+str(cc))
		elif(line[1] not in registers or line[2] not in registers):
			exit0('invalid argument at line number '+str(cc)+'. Please enter a register.')
		elif(registers[line[2]]==0):
			exit0('division by zero not possible. Error at line number'+str(cc))
		else:
			registers[line[1]]=int(registers[line[1]]/registers[line[2]])

	# mod operation, get modulo of values of two registers and put into first one => mod A B => A=A%B
	elif(commands[line[0]]=='mod'):
		if(len(line)>3):
			exit0('too many arguments at line number '+str(cc))
		elif(line[1] not in registers or line[2] not in registers):
			exit0('invalid argument at line number '+str(cc)+'. Please enter a register.')
		else:
			registers[line[1]]%=registers[line[2]]

	# inc operation, increment the value of given register by 1 => inc A => A=A+1
	elif(commands[line[0]]=='inc'):
		if(len(line)>2):
			exit0('too many arguments at line number '+str(cc))
		elif(line[1] not in registers):
			exit0('invalid argument at line number '+str(cc)+'. Please enter a register.')
		else:
			registers[line[1]]+=1

	# dec operation, decrement the value of given register by 1 => dec A => A=A-1
	elif(commands[line[0]]=='dec'):
		if(len(line)>2):
			exit0('too many arguments at line number '+str(cc))
		elif(line[1] not in registers):
			exit0('invalid argument at line number '+str(cc)+'. Please enter a register.')
		else:
			registers[line[1]]-=1


	# band operation, bitwise and of two registers and store value in first one=> band A B => A=A&B
	elif(commands[line[0]]=='band'):
		if(len(line)>3):
			exit0('too many arguments at line number '+str(cc))
		elif(line[1] not in registers or line[2] not in registers):
			exit0('invalid argument at line number '+str(cc)+'. Please enter a register.')
		else:
			registers[line[1]]&=registers[line[2]]

	# bor operation, bitwise or of two registers and store value in first one=> bor A B => A=A|B
	elif(commands[line[0]]=='bor'):
		if(len(line)>3):
			exit0('too many arguments at line number '+str(cc))
		elif(line[1] not in registers or line[2] not in registers):
			exit0('invalid argument at line number '+str(cc)+'. Please enter a register.')
		else:
			registers[line[1]]|=registers[line[2]]

	# bxor operation, bitwise xor of two registers and store value in first one=> bxor A B => A=A^B
	elif(commands[line[0]]=='bxor'):
		if(len(line)>3):
			exit0('too many arguments at line number '+str(cc))
		elif(line[1] not in registers or line[2] not in registers):
			exit0('invalid argument at line number '+str(cc)+'. Please enter a register.')
		else:
			registers[line[1]]=registers[line[1]]^registers[line[2]]

	# and operation, logical and of two registers and value will reflect in flag only=> and A B => flag=A and B
	elif(commands[line[0]]=='and'):
		if(len(line)>3):
			exit0('too many arguments at line number '+str(cc))
		elif(line[1] not in registers or line[2] not in registers):
			exit0('invalid argument at line number '+str(cc)+'. Please enter a register.')
		else:
			registers[line[1]]=bool(registers[line[1]]) and bool(registers[line[2]])

	# or operation, logical or of two registers and value will reflect in flag only=> or A B => flag=A or B
	elif(commands[line[0]]=='or'):
		if(len(line)>3):
			exit0('too many arguments at line number '+str(cc))
		elif(line[1] not in registers or line[2] not in registers):
			exit0('invalid argument at line number '+str(cc)+'. Please enter a register.')
		else:
			registers[line[1]]=bool(registers[line[1]]) or bool(registers[line[2]])

	# cmp operation, compare values of two registers on basis of given relation and will affect flag only.
	elif(commands[line[0]]=='cmp'):
		# print(line)
		if(len(line)>4):
			exit0('too many arguments at line number '+str(cc))
		elif(line[1] not in registers or line[3] not in registers):
			exit0('invalid argument at line number '+str(cc)+'. Please enter a register.')
		elif(line[2] not in ['201', '202', '205', '206', '207', '208', '209']):
			exit0('invalid operator at line number '+str(cc))

		# equal operation
		elif(commands[line[2]]=='equal'):
			if(registers[line[1]]==registers[line[3]]):
				flag=1
			else:
				flag=0

		# greater than operation
		elif(commands[line[2]]=='gt'):
			if(registers[line[1]]>registers[line[3]]):
				flag=1
			else:
				flag=0

		# less than operation
		elif(commands[line[2]]=='lt'):
			if(registers[line[1]]<registers[line[3]]):
				flag=1
			else:
				flag=0

		# greater than or equal to operation
		elif(commands[line[2]]=='gte'):
			if(registers[line[1]]>=registers[line[3]]):
				flag=1
			else:
				flag=0

		# less than or equal to operation
		elif(commands[line[2]]=='lte'):
			if(registers[line[1]]<=registers[line[3]]):
				flag=1
			else:
				flag=0

		# logical and operation
		elif(commands[line[2]]=='and'):
			flag=bool(registers[line[1]]) and bool(registers[line[3]])

		# logical or operation
		elif(commands[line[2]]=='or'):
			flag=bool(registers[line[1]]) or bool(registers[line[3]])

	# unconditional jump operation=> jmp lineNumber=>pc=lineNumber
	elif(commands[line[0]]=='jmp'):
		if(len(line)>2):
			exit0('too many arguments at line number '+str(cc))
		elif(int(line[1])>len(inputline)):
			exit0('invalid argument at line number '+str(cc)+'. Please enter a valid line number to jump.')
		else:
			pc=int(line[1])

	# conditional jump operation => jump if flag is set => jt lineNumber => pc=lineNumber if flag=true
	elif(commands[line[0]]=='jt'):
		if(len(line)>2):
			exit0('too many arguments at line number '+str(cc))
		elif(int(line[1])>len(inputline)):
			exit0('invalid argument at line number '+str(cc)+'. Please enter a valid line number to jump.')
		elif(flag==1):
				pc=int(line[1])

	# conditional jump operation => jump if flag is reset => jf lineNumber => pc=lineNumber if flag=false
	elif(commands[line[0]]=='jf'):
		if(len(line)>2):
			exit0('too many arguments at line number '+str(cc))
		elif(int(line[1])>len(inputline)):
			exit0('invalid argument at line number '+str(cc)+'. Please enter a valid line number to jump.')
		elif(flag==0):
				pc=int(line[1])

	# input operation => replace value of given register by input value
	elif(commands[line[0]]=='inp'):
		if(len(line)>2):
			exit0('too many arguments at line number '+str(cc))
		elif(line[1] not in registers):
			exit0('invalid argument at line number '+str(cc)+'. Please enter a register.')
		else:
			registers[line[1]]=int(input())

	# push operation => pushes value of all registers and flag onto stack when called
	elif(commands[line[0]]=='push'):
		if(len(line)>1):
			exit0('too many arguments at line number '+str(cc))
		else:
			stack.append([registers['01'], registers['02'], registers['03'], registers['04'], registers['05'], registers['06'], flag])

	# pop operation => pops from stack all registers and flag
	elif(commands[line[0]]=='pop'):
		if(len(line)>1):
			exit0('too many arguments at line number '+str(cc))
		elif(len(stack)==0):
			exit0("can't pop anything as stack is empty. Error at line number "+str(cc))
		else:
			a = stack.pop()
			j=0
			for i in registers:
				registers[i]=a[j]
				j+=1
			flag=a[-1]

# if there is no hlt statement then generate error
exit0('no exit statement found. error in program. Please include hlt operation.')