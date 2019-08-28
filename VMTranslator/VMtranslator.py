import sys
from pathlib import Path
from typing import List
from VMParser import VMParser
from VMCodeWriter import VMCodeWriter

def main():
	readPaths: List[Path]
	writePath: Path
	inputPath = Path(sys.argv[1])

	if inputPath.is_dir():
		readPaths = [p for p in inputPath.iterdir() if p.suffix == ".vm"]
		writePath = (inputPath / inputPath.stem).with_suffix(".asm")
	else:
		assert inputPath.suffix == ".vm", "Invalid input file: must have .vm extension"
		readPaths = [inputPath]
		writePath = inputPath.with_suffix(".asm")

	with open(writePath, "w+") as writeFile:
		writer = VMCodeWriter(writeFile)
		writer.writeInit()
		for p in readPaths:
			parser = VMParser(p, writer) # sets up the VMParser
			while parser.hasMoreCommands():
				parser.writeNextCommand()
		
if __name__ == "__main__":
	main()