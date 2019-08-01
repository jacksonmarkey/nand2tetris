"""Parser

	Contains methods useful for parsing Hack assebly code into binary.
	Used in assembler.py
"""
from typing import List
import translator


class HackParser():

	nextFree: int = 16  # starting address for storing variables

	def parse(self, assLine: str) -> str:
		if (assLine[0] == "@"):
			return self.aInstruction(assLine)
		else:
			return self.cInstruction(assLine)

	def aInstruction(self, assLine: str) -> str:
		address = assLine[1:]

		if not address[0].isdigit():  # address is a variable
			if address in translator.SYMBOLS:  # if we have previously encoutered this variable
				address = translator.SYMBOLS[address]
			else:  # if this is the first time encoutnering a variable
				# assigns the next free register to the new variable
				self.addSymbol(address, self.nextFree)
				address = self.nextFree  # reassigns the local address variable to that free register address
				self.nextFree += 1

		binary: str = bin(int(address))[2:]  # removes the leading "0b"
		# processes the string to ensure it has a 15 bit representation,
		# in addition to the extra 0 in front to denote the A-instruction
		charDifference: int = 15 - len(binary)
		if (charDifference >= 0):
			for i in range(charDifference + 1):  # extra 0 in front
				binary = "0" + binary
		if (charDifference < 0):
			raise ValueError(
				"Integer in assembly code is too large for 15 bits.")
		return binary

	def cInstruction(self, assLine: str) -> str:
		splitLine: List[str] = self.splitCInst(assLine)
		assert len(splitLine) == 3, "Malformed C-instruction line."
		lhs = splitLine[0]
		rhs = splitLine[1]
		jumpText = splitLine[2]

		# tell if it's a command with A or M
		MorA = self.MorAComp(rhs)
		# binary input of computation for the Hack ALU
		comp = self.aluInput(rhs)
		# destination
		dest = self.destination(lhs)
		# determine the jump specification
		jump = self.jumpComp(jumpText)

		return ("111" + MorA + comp + dest + jump)


	# splits a C-instruction line into its three components

	def splitCInst(self, text: str) -> List[str]:
		if ("=" in text and ";" in text):
			return re.split("[;=]", text)
		elif ("=" in text):
			return text.split("=") + [""]
		elif (";" in text):
			return [""] + text.split(";")
		else:
			return ["", text, ""]

	# given the RHS of an equation, determines whether it operates on A or M
	# note that a well-defined computation should only ever operate on one of these

	def MorAComp(self, rhs: str) -> str:
		if ("A" in rhs and "M" in rhs):
			raise ValueError(
				"C-instruction uses both M and A in the same computation.")
		elif ("M" in rhs):
			return "1"
		else:
			return "0"  # we default to the value 0 if neither appear in the RHS

	# given the RHS of an equation, returns the 6-bit ALU input for that calculation

	def aluInput(self, text: str) -> str:
		if text in translator.ALU_INPUTS:
			return translator.ALU_INPUTS[text]
		else:
			raise ValueError("Malformed input to dcomputation specification in C-instruction.")

	# takes in the lhs of an equation and returns its 3-bit binary representation

	def destination(self, lhs: str) -> str:
		if lhs in translator.DEST:
			return translator.DEST[lhs]
		else:
			raise ValueError(
				"Malformed input to dest section of a C-instruction.")

	# takes in a string representing some jump specification
	# and returns the 3bit binary representation

	def jumpComp(self, x: str) -> str:
		if x in translator.JUMP:
			return translator.JUMP[x]
		else:
			raise ValueError(
				"Malformed input to jump section of a C-instruction.")

	# adds a given variable to our translator dictionary
	def addSymbol(self, varName, value):
		translator.SYMBOLS[varName] = value