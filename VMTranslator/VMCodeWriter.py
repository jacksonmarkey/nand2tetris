import VMConstants
from pathlib import Path

class VMCodeWriter:
	def __init__(self, writeFile):
		self.writeFile = writeFile
		self.count = 0 # we use this number to distinguish between calls to subroutines
		self.currentFile = None

	def setFile(self, fileName: str):
		self.currentFile = fileName

	def writeInit(self):
		self.writeFile.write(
			"@256\n"
			"D=A\n"
			"@SP\n"
			"M=D\n")
		self.writeFunction("call", "Sys.init", "0")
		for l in open(Path("asmTemplate.txt")).readlines():
			self.writeFile.write(l)

	# each push and pop command has very similar assembly code, so we only distinguish
	# between the different segments when we get the specific string from popDict and pushDict
	def writePushPop(self, command, segment, index):
		assert index.isdigit(), "Index of command must be an integer"

		if command == "push":
			self.writeFile.write(
				"@PUSHD" + str(self.count) + "\n"
				"D=A\n"
				"@R15 // ROM[15] stores our eventual return address\n"
				"M=D\n")
			if segment in ["constant", "local", "argument", "this", "that", "temp", "pointer"]:
				self.writeFile.write(
					VMConstants.pushDict[segment].format(index))
			elif segment == "static": # we need infomarion about the current function for static
				self.writeFile.write( # so we need to format the string differently
					VMConstants.pushDict[segment].format(self.currentFile + "." + index))
			else:
				raise ValueError("Invalid segment value (first argument) for push command")
			self.writeFile.write(
				"@PUSHD\n"
				"0;JMP\n"
				"(PUSHD" + str(self.count) + ")\n")
			
		if command == "pop":
			self.writeFile.write(
				"@POPD" + str(self.count) + "\n"
				"D=A\n"
				"@R15 // ROM[15] stores our eventual return address\n"
				"M=D\n")
			if segment in ["local", "argument", "this", "that", "temp", "pointer"]:
				self.writeFile.write(
					VMConstants.popDict[segment].format(index))
			elif segment == "static":
				self.writeFile.write(
					VMConstants.popDict[segment].format(self.currentFile + "." + index))
			else:
				raise ValueError("Invalid segment value (first argument) for pop command")
			self.writeFile.write(
				"@R14 // ROM[14] stores the address to which we want to pop our value\n"
				"M=D\n"
				"@POPD\n"
				"0;JMP\n"
				"(POPD" + str(self.count) + ")\n")

		self.count += 1

	def writeArithmetic(self, command):
		if command in ["add", "sub", "neg", "and", "or", "not"]:
			self.writeFile.write(
				VMConstants.arithmeticDict[command])
		elif command in ["eq", "lt", "gt"]:
			self.writeFile.write(
				VMConstants.arithmeticDict[command].fomat(str(self.count)))
			self.count += 1
		else:
			raise ValueError("Invalid arithmetic command")

	def writeProgFlow(self, command, currentFunction, label):
		if command == "label":
			self.writeFile.write(
				"(" + currentFunction + "$" + label + ")\n")
		elif command == "goto":
			self.writeFile.write(
				"@" + currentFunction + "$" + label + "\n"
				"0;JMP\n")
		elif command == "if-goto":
			self.writeFile.write(
				"@SP\n"
				"AM=M-1\n"
				"D=M\n"
				"@" + currentFunction + "$" + label + "\n"
				"D;JNE\n")
		else:
			raise ValueError("Invalid program flow command")

	def writeFunction(self, command, funcName, numOfArgs):

		if command == "function":
			self.writeFile.write("(" + funcName + ")\n")
			for i in range(int(numOfArgs)):
				self.writePushPop("push", "constant", "0")

		elif command == "call":
			self.writeFile.write(
				"@" + funcName + "$" + str(self.count) + "$RETURNADDRESS\n"
				"D=A\n" # we can't use pushCallingArg because we want to push the address
				"@SP\n" # of RETURNADDRESS, not the thing stored there
				"A=M\n"
				"M=D\n"
				"@SP\n"
				"M=M+1\n")
			for field in ["LCL", "ARG", "THIS", "THAT"]: # pushes current addresses onto stack
				self.writeFile.write(VMConstants.pushCallingArg.format(field))
			self.writeFile.write(
				"@" + numOfArgs + "\n"
				"D=A\n"
				"@5\n"
				"D=D+A\n"
				"@SP\n"
				"D=M-D\n" # SP - numOfArgs - 5
				"@ARG\n"
				"M=D\n" #sets ARG to SP - numOfArgs - 5
				"@SP\n"
				"D=M\n"
				"@LCL\n"
				"M=D\n" # sets the start of the local variable section
				"@" + funcName + "\n"
				"0;JMP\n" # jumps to function execution
				"(" + funcName + "$" + str(self.count) + "$RETURNADDRESS)\n")
			self.count += 1

		else:
			raise ValueError("Invalid function call or definition")

	def writeReturn(self):
		self.writeFile.write(VMConstants.returnCode)

