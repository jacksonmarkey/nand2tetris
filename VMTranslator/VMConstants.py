pushDict = {
	"constant" : ("@{}\n" # index in place of {}
					"D=A\n"),

	"local" : ("@{}\n" # index in place of {}
				"D=A\n"
				"@1\n" # holds the base address for LCL
				"A=D+M\n"
				"D=M\n"),

	"argument" : ("@{}\n" # index in place of {}
					"D=A\n"
					"@2\n" # holds the base address for ARG
					"A=D+M\n"
					"D=M\n"),

	"this" : ("@{}\n" # index in place of {}
				"D=A\n"
				"@3\n" # holds the base address for THIS
				"A=D+M\n"
				"D=M\n"),

	"that" : ("@{}\n" # index in place of {}
				"D=A\n"
				"@4\n" # holds the base address for THAT
				"A=D+M\n"
				"D=M\n"),

	"temp" : ("@{}\n" # index in place of {}
				"D=A\n"
				"@5\n" # the start of the TEMP segment is 5
				"A=A+D"
				"D=M\n"),

	"pointer" : ("@{}\n" # index in place of {}
					"D=A\n"
					"@3\n" #either modifies register 3 or 4
					"A=A+D\n"
					"D=M\n"),

	"static" : ("@{}\n" # functionName.index in place of {}
				"D=M\n")
}


popDict = {
	"local" : ("@{}\n" #increment by the index
				"D=A\n"
				"@1\n"  # the base address of LCL
				"D=M+D\n"),

	"argument" : ("@{}\n" # increment by the index
					"D=A\n"
					"@2\n" # the base address of ARG
					"D=M+D\n"),

	"this" : ("@{}\n" # increment by the index
				"D=A\n"
				"@3\n" #the base address of THIS
				"D=M+D\n"),

	"that" : ("@{}\n" # increment by the index
				"D=A\n"
				"@4\n" #the base address of THAT
				"D=M+D\n"),

	"temp" : ("@{}\n" # increment by the index
				"D=A\n"
				"@5\n" # start of TEMP segment
				"D=A+D\n"),

	"pointer" : ("@{}\n" # increment by the index
				"D=A\n"
				"@3\n" # start of pointer segment
				"D=A+D\n"),

	"static" : ("@{}\n"
				"D=A\n")
}

arithmeticDict = {
	"add" : ("@SP\n"
				"AM=M-1\n"
				"D=M\n"
				"A=A-1\n"
				"M=M+D\n"),

	"sub" : ("@SP\n"
				"AM=M-1\n"
				"D=M\n"
				"A=A-1\n"
				"M=M-D\n"),

	"neg" : ("@SP\n"
				"A=M-1\n"
				"M=-M\n"),

	"eq" : ("@EQ{}\n" # count goes here
			"D=A\n"
			"@R15\n"
			"M=D\n"
			"@EQ\n"
			"0;JMP\n"
			"(EQ{})\n"), # count goes here

	"lt" : ("@LT{}\n" # count goes here
			"D=A\n"
			"@R15\n"
			"M=D\n"
			"@LT\n"
			"0;JMP\n"
			"(LT{})\n"), # count goes here

	"gt" : ("@GT{}\n" # count goes here
			"D=A\n"
			"@R15\n"
			"M=D\n"
			"@GT\n"
			"0;JMP\n"
			"(GT{})\n"), # count goes here

	"and" : ("@SP\n"
				"AM=M-1\n"
				"D=M\n"
				"A=A-1\n"
				"M=D&M\n"),

	"or" : ("@SP\n"
			"AM=M-1\n"
			"D=M\n"
			"A=A-1\n"
			"M=D|M\n"),

	"not" : ("@SP\n"
				"A=M-1\n"
				"M=!M\n")
}

pushCallingArg = ("@{}\n" # either LCL, ARG, THIS, or THAT
					"D=M\n"
					"@SP\n"
					"A=M\n"
					"M=D\n"
					"@SP\n"
					"M=M+1\n")

returnCode = ("@LCL\n"
				"D=M\n"
				"@15 // ROM[15] stores the FRAME variable\n" # ROM[15] stores the FRAME variable
				"M=D\n" # stores the address of LCL in a temp variable
				"@5\n"
				"A=D-A\n"
				"D=M\n"
				"@14 // ROM14 stores the RETURNADDRESS temp variable\n" # ROM14 stores the RETURNADDRESS temp variable
				"M=D\n" # stores the return address in a temp variable
				"@SP\n"
				"A=M-1\n"
				"D=M\n"
				"@ARG\n"
				"A=M\n"
				"M=D\n" #stores the return value at the top of the new stack
				"D=A+1\n"
				"@SP\n"
				"M=D\n" # resets SP to be in front of the return value on the stack

				"@15\n"
				"A=M-1\n"
				"D=M\n"
				"@THAT\n"
				"M=D\n" # restores the value of THAT from the calling function

				"@15\n"
				"A=M-1\n"
				"A=A-1\n"
				"D=M\n"
				"@THIS\n"
				"M=D\n" # restores the value of THIS from the calling function

				"@15\n"
				"A=M-1\n"
				"A=A-1\n"
				"A=A-1\n"
				"D=M\n"
				"@ARG\n"
				"M=D\n" # restores the value of ARG from the calling function

				"@15\n"
				"A=M-1\n"
				"A=A-1\n"
				"A=A-1\n"
				"A=A-1\n"
				"D=M\n"
				"@LCL\n"
				"M=D\n" # restores the value of LCL from the calling function

				"@14\n"
				"A=M\n"
				"0;JMP\n")