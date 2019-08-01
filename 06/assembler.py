import sys
import re
from hackParser import HackParser
from pathlib import Path
from typing import List

# Assembly and binary code files
assPath = Path(sys.argv[1])
binPath = Path(sys.argv[1].split(".")[0] + ".hack")

myParser = HackParser()

def main():
	# we write the binary code to the file at binPath and read assembly code from assPath
	with open(binPath, "w+") as binFile, open(assPath, "r") as assFile:
		# some pre-emptive cleaning of our assembly code
		assCode: List[str] =  cleanAssembly(assFile.readlines())

		# first pass through the assembly code to create the symbol table of labels
		lineCount = 0  # how many lines of binary code have been produced
		for assLine in assCode:
			if producesCode(assLine):
				lineCount += 1
			else: 
				myParser.addSymbol(assLine[1:-1], lineCount)

		# second pass to create and write each line of binary code
		for assLine in assCode:
			if producesCode(assLine):
				binLine = myParser.parse(assLine)
				binFile.write(binLine + "\n")

# returns whether a given line of assembly code produces any binary machine code
def producesCode(assLine: str) -> bool:
	return not (assLine[0], assLine[-1]) == ("(", ")")

# removes whitespace, comments, and blank lines from our assmebly code
def cleanAssembly(assCode: List[str]) -> List[str]:
	# first we remove whitespace and comments from each line
	cleanedLines = map(
			lambda x: re.sub("\s", "", x).split("//")[0],
			assCode)
	# then we remove empty lines from the entire list
	return list(filter(lambda x: not x == "", cleanedLines))

if __name__ == "__main__":
	main()
