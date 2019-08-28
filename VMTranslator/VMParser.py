from pathlib import Path
from VMCodeWriter import VMCodeWriter

class VMParser:
	def __init__(self, readFile: Path, writer: VMCodeWriter):
		with open(readFile, "r") as reader:
			temp = map(lambda s: s.split("//")[0], reader.readlines())
			self.VMCode = list(filter(lambda x: not (x.isspace() or x == ""), temp))
			writer.setFile(readFile.stem)
			self.writer = writer
			self.currentLine = 0
			self.fileName = readFile.stem
			self.currentFunction = None

	def hasMoreCommands(self) -> bool:
		return self.currentLine < len(self.VMCode)

	def writeNextCommand(self):
		VMLine = self.VMCode[self.currentLine]
		self.currentLine += 1
		VMArgs = VMLine.split()
		commandType = VMArgs[0]

		if (commandType in ["add", "sub", "neg", "eq", "lt", "gt", "and", "or", "not"]):
			assert len(VMArgs) == 1, "Arithmetic command does not take any arguments"
			self.writer.writeArithmetic(commandType)
		elif (commandType in ["push", "pop"]):
			assert len(VMArgs) == 3, "Push pop command takes two arguments"
			self.writer.writePushPop(commandType, VMArgs[1], VMArgs[2])
		elif (commandType in ["label", "goto", "if-goto"]):
			assert len(VMArgs) == 2, "Program flow command takes one argument"
			self.writer.writeProgFlow(commandType, self.currentFunction, VMArgs[1])
		elif (commandType in ["function", "call"]):
			assert len(VMArgs) == 3, "Program flow command takes two arguments"
			if commandType == "function": self.currentFunction = VMArgs[1]
			self.writer.writeFunction(commandType, VMArgs[1], VMArgs[2])
		elif (commandType == "return"):
			assert len(VMArgs) == 1, "return command takes no arguments"
			self.writer.writeReturn()
		else:
			raise ValueError("invalid command word in line " + str(currentLine) + ": " + commandType)