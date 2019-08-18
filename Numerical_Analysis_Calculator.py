#Name: Isaac Manjarres
#Term Project Name: Numerical Analysis Calculator

import Tkinter
from Tkinter import *
from math import *
from Tkinter import Button 
from Tkinter import Checkbutton
import string
import tkMessageBox

#creates the main calculator window where the user can determine if they would
#like to derive or integrate a function. 
class CalculatorWindow(object):

	def __init__(self, width = 700, height = 650):
		self.menuWidth = width
		self.menuHeight = height 
		self.functionNameOffset = self.variableLabelOffset = 150 
		self.explanationTextOffset = self.sectionTitleOffset = 5
		self.titleMargin = 50
		self.instructionTextY = self.titleMargin + 50
                
    #initializes necessary parameters to create the options for the title
    #screen 
	def initTitleScreen(self):
		self.titleScreenActive = True
		self.graphScreenActive = False
		self.mainScreenActive = False
		self.helpScreenActive = False 
		self.titleScreenOptionButton = CalculatorButton(self.root,self)
		self.titleScreenOptionButton.makeTitleButtons()

	def returnToMainScreenFromGraphScreen(self):
		self.mainScreenActive = True
		self.graphScreenActive = False
		self.eraseGraphInformation()
		#brings back all of the previous information that was available before
		#the screen was changed. 
		self.restoreMainScreenState()
		self.redrawAll()

	def restoreMainScreenState(self):
		self.mainScreenButtons.graphButton.place(x = 600, y = 600)
		self.mainScreenButtons.analyzeButton.place(x = 350, y = 40)
		self.mainScreenButtons.evaluateDerivativeButton.place(x = 340, y = 222)
		self.mainScreenButtons.evaluateIntegralButton.place(x = 430, y = 420)
		self.mainScreenButtons.findRootButton.place(x = 390, y = 580)
		self.mainScreenButtons.helpButton.place(x = 625, y = 40)
		self.mainScreenTextFields.equationField.place(x = 200, y = 40)
		self.mainScreenTextFields.derivativeAtPointField.place(x = 195, y = 225)
		self.mainScreenTextFields.upperLimitField.place(x = 275, y = 400)
		self.mainScreenTextFields.lowerLimitField.place(x = 275, y = 440)
		self.mainScreenTextFields.xInitialRootField.place(x = 195, y = 580)

    #gets rid of the graph buttons, fields, and labels so that the user can
    #transition back to the main screen. 
	def eraseGraphInformation(self):
		self.graph.inputText.xIncrement.destroy()
		self.graph.inputText.yIncrement.destroy()
		self.graph.checkButtons.derivativeToggle.destroy()
		self.graph.checkButtons.functionToggle.destroy()
		self.graph.checkButtons.integralToggle.destroy()
		self.graph.inputFields.xIncrementField.destroy()
		self.graph.inputFields.yIncrementField.destroy()
		self.graph.commandButtons.updateButton.destroy()
		self.graph.commandButtons.returnToMainScreenButton.destroy()

	def returnToInstructions(self):
		self.mainScreenActive = False
		self.titleScreenActive = True 
		self.hideMainScreenFieldsAndButtons()
		self.initTitleScreen()
		self.redrawAll()

    #this function evaluates the derivative at a point specified by the user.
	def evaluateDerivative(self):
		self.derivativeField = \
		                  self.mainScreenTextFields.derivativeAtPointField.get()
		if(self.workingFunction == ''):
			tkMessageBox.showerror(title = 'Missing Input', message = """Sorry,\
 you must first enter a function and analyze it before being able to evaluate\
 it.
""")
			return
		elif(self.verifyDerivativePoint() == False):
		    tkMessageBox.showerror(title = 'Syntax Error', message = """You\
 must enter a decimal or integer in order to evaluate the function.""")
		    return
		else: self.performDerivativeEvaluation()

	def performDerivativeEvaluation(self):
		derivative = self.parsedDerivative
		x = float(self.derivativeField)
		self.derivativeResult = eval(derivative)
		self.redrawAll()

	def findRoot(self):
		self.rootInput = self.mainScreenTextFields.xInitialRootField.get()
		errorMessage = 'Your input must be a decimal or an integer'
		missingInputMsg = "You must first input a function and analyze it."
		if(self.workingFunction == ''):
			tkMessageBox.showerror(title = 'Missing Function', 
				                   message = missingInputMsg)
			return
		elif(self.rootInput == ''):
			return
		elif(self.verifyRootInput() == False):
			tkMessageBox.showerror(title = 'Syntax Error', 
				                   message = errorMessage)
			return
		else:
			self.newtonsMethod()
			self.redrawAll()

	def verifyRootInput(self):
		try:
			float(self.rootInput)
		except:
			return False 

    #uses the Newton-Rhapson method to find an extremely close approximation to 
    #a root at a given value.
	def newtonsMethod(self):
		#optimal number of iterations to ensure convergence. However, method 
		#converges pretty fast.
		iterations = 1550
		x = float(self.rootInput)
		function = self.parsedFunction
		#this value must be initialized to compare for convergence later.
		penultimateValue = x
		if(eval(function) == 0.0):
			self.rootValue = str(x) 
			return 
		derivative = self.parsedDerivative
		for iteration in xrange(iterations):
			functionValue = eval(function)
			derivativeValue = eval(derivative)
			#this method is not viable if the derivative reaches at 0 because it
			#involves finding the x-intercept of the tangent line to a point on 
			#the graph iteratively, until both the function and its tangent line
			#touch the x-axis. However, the method can be used if that x value 
			#is decremented by a small amount in order to bypass the error.
			if(derivativeValue == 0.0):
				x -= 0.01
				functionValue = eval(function)
				derivativeValue = eval(derivative)
			#Newton-Rhapson iterative formula of approximation.	
			x = x - (functionValue/derivativeValue)
			#since xrange is non-inclusive, the penultimate value is iterations
			#-2. We store this value to test for convergence.
			if(iteration == iterations - 2):
				penultimateValue = x
		if(self.testConvergence(x, penultimateValue) == False):
			self.rootValue = 'There are no roots in this vicnity.'
			return 
		self.rootValue = str(x)

	def testConvergence(self, finalRoot, previousRoot):
		epsilon = 0.00000001
		return abs(finalRoot - previousRoot) <= epsilon

	def drawRootText(self):
		noRootsMessage = 'There are no roots in this vicnity.'
		if(self.rootValue != noRootsMessage):
		    rootDisplayText = "x = %s" % self.rootValue
		else:
			rootDisplayText = self.rootValue
		self.canvas.create_text(150, 625, text = rootDisplayText, 
			                    font = ('Cambria Math', 13, 'italic'), 
			                    anchor='w', fill = 'white')

	def drawDerivativeEvaluation(self):
		derivativeValue = self.derivativeResult
		evaluationPoint = self.derivativeField
		result = "f'(%s) = %.3f" % (evaluationPoint, derivativeValue)
		self.canvas.create_text(150,265, text = result, 
			               font = ("Cambria", 13, 'italic'), anchor = 'w', 
			               fill = 'white')

	def verifyDerivativePoint(self):
		try:
			float(self.derivativeField)
		except:
			return False

	def initMainScreen(self):
		self.derivative = ''
		self.integral = ''
		self.integralResult = ''
		self.workingFunction = ''
		self.derivativeResult = ''
		self.rootValue = ''
		self.titleScreenActive = False
		self.mainScreenActive = True 
		self.mainScreenTextFields = CalculatorInputField(self.root)
		self.mainScreenTextFields.makeMainScreenFields()
		self.mainScreenButtons = CalculatorButton(self.root, self)
		self.mainScreenButtons.makeMainScreenButtons()
		self.titleScreenOptionButton.continueButton.destroy()
		self.redrawAll()

	def getUserInput(self):
		self.userInput = self.mainScreenTextFields.equationField.get()
		if(self.userInput == ''):
			return
		#transforms the user input into an expression that will be checked for 
		#syntax error.	
		self.parseInput()

	def evaluateIntegral(self):
		if(self.integral == ''):
			tkMessageBox.showerror(title = 'Limit Error', 
				                   message = """You must first analyze the \
function before trying to take the integral over a boundary. \
Please try again.""")
			return 
		self.upperLimit = self.mainScreenTextFields.upperLimitField.get()
		self.lowerLimit = self.mainScreenTextFields.lowerLimitField.get()
		#detects any syntactical errors in the limit inputs that the user may 
		#have commited.
		if(self.verifyLimitInputs() == False):
			tkMessageBox.showerror(title = 'Missing Limit', 
				                   message = """You must enter both an upper \
limit and a lower limit in order to take the integral over a boundary. \
Please try again.""")
			return 
		else:
			self.definiteIntegration()

	def definiteIntegration(self):
		integral = self.parsedIntegral
		#uses the first fundamental theorem of calculus to evaluate a limit, 
		#which states that the definite integral of a function over a boundary 
		#is F(b) - F(a), where F is the integral, and a and b are the lower and
		#upper limits of the boundary respectively.
		x = float(self.upperLimit)
		upperEval = eval(integral)
		x = float(self.lowerLimit) 
		lowerEval = eval(integral)
		result = upperEval - lowerEval
		self.integralResult = str(result)
		self.redrawAll()

	def drawDefiniteIntegralResult(self):
		integralResult = self.integralResult
		self.canvas.create_text(260, 490, text = integralResult, anchor = 'w',
			                    font = ('Cambria Math', 13, 'italic'), 
			                    fill = 'white')

    #tests to ensure that the inputs at the limits is either an int or a float
    #and does not contain any string characters.
	def verifyLimitInputs(self):
		if(self.upperLimit == '' or self.lowerLimit == ''):
			return False
		try:
			float(self.upperLimit)
		except:
			return False
		return True

	def parseInput(self):
		self.input = ParsedExpression(self.userInput)
		result = self.input.parse()
		errorMessage = """Sorry, the equation that you have entered is not 
syntactically correct. Please try entering the equation again.
An Example: 3x^3 + 6x"""
        #if the expression entered is not correct, then an error will occur, and 
        #the user must enter the expression again.
		if(result == False):
			tkMessageBox.showerror(title = 'Syntax Error', 
				  message = errorMessage)
			return
		else:
			#creates a parsed function so that it can be graphed at a later time
			self.workingFunction, self.parsedFunction = result
			#create an instance of the function to take the derivative and
			#of integral of.
			self.deriveFunction()
			self.integrateFunction()
			self.graphInput = [self.parsedFunction, self.parsedDerivative, 
			                   self.parsedIntegral]

	def drawIntegralExpression(self):
		#the plus C is because of the constant that must be taken into account
		#when taking an indefinite integral. 
		integralExpression = self.integral + '+C'
		self.canvas.create_text(200, 325, text = integralExpression, 
			                    anchor = 'w', 
			                    font = ("Cambria Math", 13, 'italic'), 
			                    fill = 'white')

	def deriveFunction(self):
		self.functionInstance = PolynomialFunction(self.workingFunction)
		self.derivative = self.functionInstance.differentiate()
		self.parsingDerivative = ParsedExpression(self.derivative)
		#parses derivative so that it can be evaluated later by the graphing
		#tool. Result variable holds the symbolic derivative and parsed derivat
		#ive.
		result = self.parsingDerivative.parse()
		self.parsedDerivative = result[1]
		self.redrawAll() 

    #operates in the same fashion as the derive function.
	def integrateFunction(self):
		self.functionInstance = PolynomialFunction(self.workingFunction)
		self.integral = self.functionInstance.integrate()
		self.parsingIntegral = ParsedExpression(self.integral)
		result = self.parsingIntegral.parse()
		self.parsedIntegral = result[1]
		self.redrawAll()

    #hides the buttons and fields from the user's sight when transitioning to
    #the graph screen but doesn't destroy them so that when they are restored, 
    #they have the same information 
	def hideMainScreenFieldsAndButtons(self):
		self.mainScreenButtons.graphButton.place_forget()
		self.mainScreenButtons.analyzeButton.place_forget()
		self.mainScreenButtons.evaluateDerivativeButton.place_forget()
		self.mainScreenButtons.evaluateIntegralButton.place_forget()
		self.mainScreenButtons.findRootButton.place_forget()
		self.mainScreenButtons.helpButton.place_forget()
		self.mainScreenTextFields.equationField.place_forget()
		self.mainScreenTextFields.derivativeAtPointField.place_forget()
		self.mainScreenTextFields.upperLimitField.place_forget()
		self.mainScreenTextFields.lowerLimitField.place_forget()
		self.mainScreenTextFields.xInitialRootField.place_forget()

	def makeGraph(self):
		#does not allow the user to graph anything if they graph an empty string
		#or if they have not taken the derivative of the function.
		graphErrorMessage = """In order to graph the function its derivative,\
 and its integral, you must first input the function and analyze it. \
Please try again."""
		if(self.workingFunction == ''):
			tkMessageBox.showerror(title = 'Graphing Error', 
				                   message = graphErrorMessage)
			return
		else:
			self.graph = Graph(self.graphInput[0], self.graphInput[1], 
				               self.graphInput[2],self)
			self.mainScreenActive = False
			self.graphScreenActive = True 
			self.hideMainScreenFieldsAndButtons()
			self.graph.graphRun()
			self.redrawAll()
		
    #this function is what allows the user to see the symbolic derivative of the
    #polynomial that they input.
	def drawDerivativeExpression(self):
		derivativeExpression = self.derivative
		self.canvas.create_text(200, 150, text = derivativeExpression, 
			                    anchor = 'w', 
			                    font = ('Cambria Math', 13, 'italic'), 
			                    fill = 'white')

	def drawMainScreenLabels(self):
		self.drawFunctionLabels()
		self.drawVariableLabels()
		self.drawExplanationLabels()

	def drawFunctionLabels(self):
		#function names should be in line with each other, and so should the
		#titles of each section.
		functionNameOffset = self.functionNameOffset
		sectionTitleOffset = self.sectionTitleOffset
		self.canvas.create_text(functionNameOffset, 50, text = 'f(x) = ', 
			                    font = ('Cambria Math', 13, 'italic'), 
			                    anchor = 'w', fill = 'white')
		self.canvas.create_text(functionNameOffset, 325, text = 'F(x) = ', 
			                    font = ('Cambria Math', 13, 'italic'), 
			                    anchor = 'w', fill = 'white')
		self.canvas.create_text(functionNameOffset,150, text = "f'(x) = ", 
			                    font = ('Cambria Math', 13, 'italic'), 
			                    anchor = 'w', fill = 'white')
		self.canvas.create_text(sectionTitleOffset, 105, 
			                    text = 'Derivative: ', 
			                    font = ('Cambria Math', 13, 'italic'), 
			                    anchor = 'w', fill = 'white')
		self.canvas.create_text(sectionTitleOffset, 300, 
			                    text = 'Integral: ', 
			                    font = ('Cambria Math', 13, 'italic'), 
			                    anchor = 'w', fill = 'white')

	def drawVariableLabels(self):
		#the input values should be in line with each other as well.
		variableLabelOffset = self.variableLabelOffset
		self.canvas.create_text(variableLabelOffset, 590, text = 'x = ', 
			                    font = ('Cambria Math',13, 'italic'), 
			                    anchor = 'w', fill = 'white')
		self.canvas.create_text(variableLabelOffset, 410, 
			                    text = 'Upper Limit', 
			                    font = ('Cambria Math', 13, 'italic'),
			                    anchor = 'w', fill = 'white')
		self.canvas.create_text(variableLabelOffset, 450, 
			                    text = 'Lower Limit', 
			                    font = ('Cambria Math', 13, 'italic'),
			                    anchor = 'w', fill = 'white')
		self.canvas.create_text(variableLabelOffset, 235, text = 'x = ', 
			                    font = ('Cambria Math', 13, 'italic'), 
			                    anchor = 'w', fill = 'white')

	def drawExplanationLabels(self):
		beginningText = "Input the function that you would like to analyze: "
		evalDerivativeText = "Evaluate the derivative at a given x-value: "
		evalIntegralOverBound = "Evaluate the integral over a boundary: "
		evaluatedIntegralText = "The integral over the region is: "
		rootText = "Find the root of the function in the vicnity of a given x: "
		explanationTextOffset = self.explanationTextOffset
		self.canvas.create_text(explanationTextOffset,15, text = beginningText, 
        	                    font = ('Cambria Math', 13, 'italic'), 
        	                    anchor = 'w', fill = 'white')
		self.canvas.create_text(explanationTextOffset, 200, 
			                    text = evalDerivativeText, 
			                    font = ('Cambria Math', 13, 'italic'), 
			                    anchor = 'w', fill = 'white')
		self.canvas.create_text(explanationTextOffset, 375, 
			                    text = evalIntegralOverBound, 
			                    font = ('Cambria Math', 13, 'italic'), 
			                    anchor = 'w', fill = 'white')
		self.canvas.create_text(explanationTextOffset, 490, 
			                   text = evaluatedIntegralText, 
			                   font = ('Cambria Math', 13, 'italic'),anchor='w'
			                   , fill = 'white')
		self.canvas.create_text(explanationTextOffset, 550, text = rootText, 
			                   font = ('Cambria Math', 13, 'italic'),anchor='w',
			                   fill = 'white')

	def drawTitleScreen(self):
		welcomeTitle = "Numerical Analysis Calculator"
		welcomeText = """Welcome to the numerical analysis calculator. In \
order to use this program, you must 
enter an expanded polynomial that is a function of x that you would like to 
analyze, using the standard operators (+,-,^). For example: 3x^2 + 4, is a valid 
input. After you hit the analyze button, you will be able to: 

See the function's derivative, and integral expressions. 

Evaluate the derivative at a point, the integral over a boundary, and find a \
root in a 
given vicinity. 

Graph the function, its derivative, and integral on an interactive graph where
you can toggle the equations on and off, as well as change the x and y scales.
"""
                self.drawTitleScreenBackGround(welcomeTitle, welcomeText)
                
        def drawTitleScreenBackGround(self, welcomeTitle, welcomeText):
        	width, height = self.menuWidth, self.menuHeight
        	#idea for creating images as background obtained from: 
        	#http://pnk-python.chat.ru/doc/tkintro/PhotoImage.htm
        	self.backgroundImage = PhotoImage(
                	                         file = 'titleScreenBackGround.gif')
        	self.canvas.create_image(0,0, image = self.backgroundImage, 
                	                     anchor = 'nw')
        	self.canvas.create_text(width/2, 50, text = welcomeTitle, 
                	                    font = ('@Adobe Unicode MS', 20, "bold")
                	                    , fill = 'white')
        	self.canvas.create_text(5,100,text = welcomeText, 
                	                    font = ('@Adobe Unicode MS', 12, "bold")
                	                    ,justify = LEFT, anchor = 'nw')

        def drawMainScreenBackGround(self):
    	    width, height = self.menuWidth, self.menuHeight
    	    self.mainScreenBackGround = PhotoImage(
    	    	                              file = "mainScreenBackGround.gif")
    	    self.canvas.create_image(0,0,image = self.mainScreenBackGround, 
    	    	                     anchor = 'nw')
  
	def redrawAll(self):
		self.canvas.delete(ALL)
		if(self.titleScreenActive):
			self.drawTitleScreen()
		elif(self.graphScreenActive):
			self.graph.graphRedrawAll()
		elif self.mainScreenActive:
			self.drawMainScreenBackGround()
			self.drawMainScreenLabels()
			if(self.derivative != ''):
				self.drawDerivativeExpression()
				self.drawIntegralExpression()
			if(self.integralResult != ''):
				self.drawDefiniteIntegralResult()
			if(self.derivativeResult != ''):
				self.drawDerivativeEvaluation()
			if(self.rootValue != ''):
				self.drawRootText()

	def run(self):
		self.root = Tk()
		self.root.title('Numerical Analysis Calculator')
		self.root.resizable(width = 0, height = 0)
		self.canvas = Canvas(self.root, width = self.menuWidth, 
			                 height = self.menuHeight)
		self.canvas.pack()
		self.initTitleScreen()
		self.redrawAll()
		self.root.mainloop()
################################################################################
class CalculatorInputField(object):
	def __init__(self, window):
		self.window = window

	def makeMainScreenFields(self):
		self.equation = StringVar()
		self.upperLimitVal = StringVar()
		self.lowerLimitVal = StringVar()
		self.derivativePoint = StringVar()
		self.initialRoot = StringVar()
		self.equationField = Entry(self.window, textvariable = self.equation)
		self.equationField.place(x = 200, y = 40)
		self.upperLimitField = Entry(self.window, 
			                         textvariable = self.upperLimitVal)
		self.lowerLimitField = Entry(self.window, 
			                         textvariable = self.lowerLimitVal)
		self.upperLimitField.place(x = 275, y = 400)
		self.lowerLimitField.place(x = 275, y = 440)
		self.derivativeAtPointField = Entry(self.window,
			                                textvariable = self.derivativePoint)
		self.derivativeAtPointField.place(x = 195, y = 225)
		self.xInitialRootField = Entry(self.window, 
			                                    textvariable = self.initialRoot)
		self.xInitialRootField.place(x = 195, y = 580)
################################################################################
class CalculatorButton(object):
	def __init__(self, window, programInstance):
		self.window = window
		self.programInstance = programInstance

	def makeTitleButtons(self):
		self.continueButton = Button(self.window, text = "Continue",
			command = self.programInstance.initMainScreen)
		self.continueButton.place(x = 625, y = 600)

	def makeMainScreenButtons(self):
		self.analyzeButton = Button(self.window, text = "Analyze", 
			                        command = self.programInstance.getUserInput)
		self.analyzeButton.place(x = 350, y = 40)
		self.graphButton = Button(self.window, text = "Graph It", 
			                      command = self.programInstance.makeGraph)
		self.graphButton.place(x = 600, y = 600)
		self.evaluateIntegralButton = Button(self.window, 
			                                 text='Evaluate Integral', 
			         command = self.programInstance.evaluateIntegral)
		self.evaluateDerivativeButton = Button(self.window, 
			                                   text = "Evaluate Derivative",
			         command = self.programInstance.evaluateDerivative)
		self.evaluateDerivativeButton.place(x = 340, y = 222)
		self.evaluateIntegralButton.place(x = 430, y = 420)
		self.findRootButton = Button(self.window, text = "Find Root", 
			command = self.programInstance.findRoot)
		self.helpButton = Button(self.window, text = "Help", 
			                command = self.programInstance.returnToInstructions)
		self.helpButton.place(x = 625, y = 40)
		self.findRootButton.place(x = 350, y = 580)
################################################################################
class ParsedExpression(object):
	def __init__(self, function):
		self.function = function

	def parse(self):
		result = self.verificationAndParsing()
		if result == False:
			return False
		else:
			self.workingFunction, self.parsedFunction = result
			workingFunction, parsedFunction = (self.workingFunction,
				                               self.parsedFunction)
			return workingFunction, parsedFunction
		
	def verificationAndParsing(self):
		lowerCaseFunction = self.function.lower()
		spacelessFunction = self.removeWhiteSpace(lowerCaseFunction)
		if(self.validityCheck(spacelessFunction) == False):
			return False
		functionWithMultiplication =\
		                        self.addMultiplicationSymbols(spacelessFunction)
		parsedFunction = self.pythonExponentiation(functionWithMultiplication)
		return spacelessFunction, parsedFunction

	#removes whitespace in order to ensure that the output is not confusing for
	#python
	def removeWhiteSpace(self, function):
		spaceLessFunction = ""
		for char in function:
			if(char in string.whitespace):
				continue
			spaceLessFunction += char
		return spaceLessFunction

	def validityCheck(self, function):
		#set of possible operands that could be in the function.
		operands = set('+-^')
		impossibleOperands = set("""*!~`@#$%&={};:?,_()=[]{}\/",`~""")
		for impossibleOperand in impossibleOperands:
			if impossibleOperand in function:
				return False
		if('xx' in function): return False
		#if the last char is an operand then this is not a valid expression
		if(function[-1] in operands):
			return False
		#if the first char is a multiplication or exponent sign, not valid
		elif(function[0] is '*' or function[0] is '^'): return False 
		functionLength = len(function)
		for i in xrange(functionLength):
			char = function[i]
			if(char.isdigit()): continue
			#makes sure that x is the only variable in the equation
			if(char.isalpha() and char is not 'x'): return False
			#checks to make sure that there are no repeating operands
			elif(char in operands):
				if(function[i+1] in operands):return False
		return True 

	#adds multiplication symbols so that the function can be parsed and underst-
	#ood by python.
	def addMultiplicationSymbols(self, function):
		multiplicationAdded = ""
		functionLength = len(function)
		for i in xrange(functionLength):
			char = function[i]
			if(char.isdigit() and (i+1) < functionLength and 
				function[i+1] == 'x'):
				multiplicationAdded += char+'*'
			else:
				multiplicationAdded += char
		return multiplicationAdded

    #adds the correct exponentiation sign for when the parsed equation is used
    #since ^ is XOR. 
	def pythonExponentiation(self, function):
		exponentiatedFunction = function.replace('^', '**')
		return exponentiatedFunction
################################################################################
class PolynomialFunction(object):
	def __init__(self, function):
		self.function = function

	def differentiate(self):
		#checks if the function is a constant 
		if('x' not in self.function):
			return '0'
		seperatedFunction = self.addSeperators(self.function)
		functionCoeffs, functionPowers =\
		                self.powerAndCoeffExtraction(seperatedFunction)
		derivativeCoeffs, derivativePowers = self.derivative(functionCoeffs, 
			                                            functionPowers)
		return self.makeExpression(derivativeCoeffs, derivativePowers)

	def integrate(self):
		#checks if the function is simply a constant 
		if('x' not in self.function):
			return self.integrateConstants(self.function)
		seperatedFunction = self.addSeperators(self.function)
		functionCoeffs, functionPowers =\
		                self.powerAndCoeffExtraction(seperatedFunction)
		integralCoeffs, integralPowers = self.integral(functionCoeffs, 
			                                            functionPowers)
		return self.makeExpression(integralCoeffs, integralPowers)

	def integral(self, coefficients, powers):
		orderedCoeffs, orderedPowers = \
		                           self.orderCoeffAndPowers(coefficients,powers)
		numberOfTerms = len(orderedPowers)
		#uses integration rules for functions such that the integral of f(x) = 
		#(x^n+1)/(n+1)
		integralPowers = [orderedPowers[i] + 1 for i in xrange(numberOfTerms)]
		integralCoeffs = [orderedCoeffs[i]/float(integralPowers[i]) for i in \
		                  xrange(numberOfTerms)]
		finalIntegralCoeffs, finalIntegralPowers = \
		self.removeConstants(integralCoeffs, integralPowers)
		return finalIntegralCoeffs, finalIntegralPowers

	def integrateConstants(self, function):
		coefficient = function
		return '%sx' % coefficient

	#uses the '+' operand as a seperator in order to get a list of terms for the 
	#expression.
	def addSeperators(self, function):
		newFunction = ""
		functionLength = len(function)
		for i in xrange(functionLength):
			char = function[i]
			#to get the negative value to carry over, add a plus in front of it
			#so when it is split, it's still there.
			if(char == '-'):
				newFunction += '+'+char
			else:
				newFunction += char
		finalFunction = newFunction.strip('+')
		return finalFunction

	def powerAndCoeffExtraction(self, function):
		splitTerms = function.split('+')
		powers = []
		coefficients = []
		for term in splitTerms:
			#try to make an integer out of it. If not possible, then it must be 
			#a monomial. But if it is an integer, then its power is 0
			try:
				coefficient = float(term)
				coefficients.append(coefficient)
				powers.append(0)
			except:
				coeffientAndPower = self.monomialExtraction(term)
				coefficients.append(coeffientAndPower[0])
				powers.append(coeffientAndPower[1])			
		return (coefficients, powers)

	def monomialExtraction(self, term):
		termLength = len(term)
		for i in xrange(termLength):
			if(term[0] == '-' and term[1] == 'x'):
				coefficient = -1
				#if there are no carrots, its because the power is 1.
				if(term.count('^') == 0):
					power = 1
				else:
				    carrotLocation = term.index('^')
				    powerString = term[carrotLocation+1:]
				    power = int(powerString) 
			elif(term[0] == 'x'):
				coefficient = 1
				if(term.count('^') == 0):
					power = 1
				else:
				    carrotLocation = term.index('^')
				    #carrotLocation + 1 because slicing at the beginning is 
				    #inclusive. After the carrot, everything else is the power
				    powerString = term[carrotLocation+1:termLength]
				    power = int(powerString)
			elif(term.count('^') == 0):
				power = 1
				#everything until x must be part of the coefficient. 
				coefficient = float(term[:termLength-1])
			else:
				xLocation = term.index('x')
				carrotLocation = term.index('^')
				coefficient = float(term[:xLocation])
				power = int(term[carrotLocation+1:])
		return (coefficient, power)

	#code obtained from cs.cmu.edu/~112
	def reverseCmp(self, x, y):
		if(x > y):
			return -1
		if(x == y):
			return 0
		if(x < y):
		    return 1 

	#orders the powers in descending order along with the coefficients 
	#associated with them
	def orderCoeffAndPowers(self, coefficients, powers):
		matchedList = zip(powers, coefficients)
		#this allows for the terms to be sorted from greatest to smallest
		orderedMatches = sorted(matchedList, lambda a,b: self.reverseCmp(a,b))
		orderedPowers = [orderedMatch[0] for orderedMatch in orderedMatches]
		orderedCoeffs = [orderedMatch[1] for orderedMatch in orderedMatches]
		return orderedCoeffs, orderedPowers

	def derivative(self, coefficients, powers):
	    orderedCoeffs, orderedPowers = \
	                              self.orderCoeffAndPowers(coefficients, powers)
	    numberOfTerms = len(orderedPowers)
	    #using the derivative rules, f(x) = x^n, f'(x) = nx^n-1
	    derivativeCoeffs = [orderedPowers[i]*orderedCoeffs[i] 
	                        for i in xrange(numberOfTerms)]
	    derivativePowers = [orderedPowers[i] - 1 for i in xrange(numberOfTerms)]
	    finalDerivativeCoeffs, finalDerivativePowers = \
	    self.removeConstants(derivativeCoeffs, derivativePowers)
	    return finalDerivativeCoeffs, finalDerivativePowers

    #this is what creates the symbolic integral/derivative that is displayed 
    #at the user interface. 
	def makeExpression(self, coefficients, powers):
		derivativeExpression = ""
		numberOfTerms = len(coefficients)
		for i in xrange(numberOfTerms):
			if(coefficients[i] == 1 and powers[i] == 1):
				derivativeExpression += '+x'
			elif(coefficients[i] == -1 and powers[i] == 1):
				derivativeExpression += '-x'
			elif(coefficients[i] > 0 and powers[i] == 1):
				derivativeExpression += '+'+str(coefficients[i])+'x'
			elif(coefficients[i] < 0 and powers[i] == 1):
				derivativeExpression += str(coefficients[i])+'x'
			elif(powers[i] == 0):
				if(coefficients[i] > 0): 
					derivativeExpression += '+'+str(coefficients[i])
				else: derivativeExpression += str(coefficients[i])
			elif(coefficients[i] > 0):
				derivativeExpression += '+'+str(coefficients[i])+'x^'+\
				                        str(powers[i]) if powers[i] > 1 else\
	                                    '+'+str(coefficients[i])+'x'
			else:
				derivativeExpression += str(coefficients[i])+'x^'+\
				str(powers[i]) if powers[i] > 1 else str(coefficients[i])+'x'
		finalDerivativeExpression = derivativeExpression.strip('+')			
		return finalDerivativeExpression

	#removes the 0's from the derivative and omit the negative derivatives 
	#associated with them
	def removeConstants(self, derivativeCoeffs, derivativePowers):
		zeroCount = derivativeCoeffs.count(0)
		negativeCount = derivativePowers.count(-1)
		for times in xrange(zeroCount):
			derivativeCoeffs.remove(0)
		for times in xrange(negativeCount):
			derivativePowers.remove(-1)
		return derivativeCoeffs, derivativePowers
################################################################################
class Graph(object):
	def __init__(self, function, derivative, integral,mainProgramInstance,
		         width = 700, height = 650):
		self.canvasWidth, self.canvasHeight = width, height 
		self.gridWidth = self.canvasWidth
	    #in order to leave some space for the graph to be interactive for the 
	    #user to use
		self.gridHeight = 550
		self.gridBoxSize = 25
		#color codes obtained from rapidtables.com
		self.lineColor = self.rgbString(0, 0, 153)
		self.functions = [function, derivative, integral]
		(self.function, self.derivative, self.integral) = (function, 
			                                               derivative, integral) 
		self.mainProgramInstance = mainProgramInstance 

	def updateKeyedParameters(self):
		self.functionGenerator()
		self.derivativeGenerator()
		self.integralGenerator()
		self.graphRedrawAll()

	def updateToggleParameters(self):
		self.derivativeActive = self.checkButtons.derivativeStatus.get()
		self.functionActive = self.checkButtons.functionStatus.get()
		self.integralActive = self.checkButtons.integralStatus.get()
		if(self.derivativeActive == 0):
			self.derivativeActive = False
		else:
			self.derivativeActive = True
		if(self.functionActive == 0):
			self.functionActive = False
		else:
			self.functionActive = True
		if(self.integralActive == 0):
			self.integralActive = False 
		else:
			self.integralActive = True 
		self.graphRedrawAll() 

    #makes sure that the program doesn't crash the program by inputting any 
    #adverse inputs such as letters or a scale of 0.
	def getFactors(self):
		try:
			xFactor = float(self.inputFields.xIncrementField.get())
			yFactor = float(self.inputFields.yIncrementField.get())
			if(xFactor == 0.0 or xFactor == 0):
				xFactor = 1
			if(yFactor == 0.0 or yFactor == 0):
				yFactor = 1
		except:
		    (xFactor, yFactor) = (1, 1) 
		return (xFactor, yFactor)

	#code obtained from course website cs.cmu.edu/~112 from lecture notes about
	#graphics.
	def rgbString(self, red, green, blue):
	    return "#%02x%02x%02x" % (red, green, blue)

	#this function creates the x and y points for the lines that will create the
	#graph.
	def functionGenerator(self):
	    self.functionPoints = []
	    gridWidth, gridHeight = self.gridWidth,self.gridHeight
	    centerX, centerY = gridWidth/2, gridHeight/2
	    #gets the user-defined increments for the graph.
	    (userFactorX, userFactorY) = self.getFactors()
	    gridFactor = float(self.gridBoxSize)
	    #adjusts the value of the x and y increments on the graph such that 
	    #each box that is moved counts for 1 unit of the increment. So if the 
	    #user uses 4 as a factor, each box is worth 4.
	    scaleFactorX = float(self.gridBoxSize) * (1/userFactorX)
	    scaleFactorY = float(self.gridBoxSize) * (1/userFactorY)
	    #the range over which the graph loops over.
	    (negativeX, positiveX) = (int(-gridWidth), 
	    	                      int(gridWidth))
	    function = self.functions[0]
	    for i in xrange(negativeX, positiveX):
	    	#in case that the function is not defined at that value, 
	    	#then the graph bypasses that point 
	        try: 
	        	#makes the x factor by scaling it down to the grid I am 
	        	#using and evaluates the function at those points 
	    	    x = (i/gridFactor)*userFactorX
	    	    y = eval(function)
	    	    #allocates the (0,0) to the grid's center and then adds the 
	    	    #x as if it was on that (0,0) point. And it subtracts the y 
	    	    #to map it to the correct location 
	    	    firstPlottedPts = (centerX + x*scaleFactorX, 
	    	    	               centerY - y*scaleFactorY)
	    	    x = ((i+1)/gridFactor)*userFactorX
	    	    y = eval(function)
	    	    secondPlottedPts = (centerX + x*scaleFactorX, 
	    	    	                centerY - y*scaleFactorY)
	    	    self.functionPoints.append((firstPlottedPts, secondPlottedPts))
	    	except:
	    		pass

    #this function generates a plot of a function by creating a large 
	#number of line segments and joining them in the form of the curve to 
	#create the illusion of a smooth curve.
	def drawFunction(self):
		lineVertexPairs = self.functionPoints
		for vertexPair in lineVertexPairs:
			firstFunctionPoints = vertexPair[0]
			secondFunctionPoints = vertexPair[1]
			self.mainProgramInstance.canvas.create_line(firstFunctionPoints,
			secondFunctionPoints, fill = 'yellow', width = 3)

    #same process and logic as the function plotter. This just collects the 
    #derivative points
	def derivativeGenerator(self):
	    self.derivativePoints = []
	    gridWidth, gridHeight = self.gridWidth,self.gridHeight
	    centerX, centerY = gridWidth/2, gridHeight/2
	    (userFactorX, userFactorY) = self.getFactors()
	    gridFactor = float(self.gridBoxSize)
	    scaleFactorX = float(self.gridBoxSize) * (1/userFactorX)
	    scaleFactorY = float(self.gridBoxSize) * (1/userFactorY)
	    (negativeX, positiveX) = (int(-gridWidth), int(gridWidth))
	    derivative = self.functions[1]
	    for i in xrange(negativeX, positiveX):
	        try: 
	    	    x = (i/gridFactor)*userFactorX
	    	    y = eval(derivative)
	    	    firstPlottedPts = (centerX + x*scaleFactorX, 
	    	    	               centerY - y*scaleFactorY)
	    	    x = ((i+1)/gridFactor)*userFactorX
	    	    y = eval(derivative)
	    	    secondPlottedPts = (centerX + x*scaleFactorX, 
	    	    	                centerY - y*scaleFactorY)
	    	    self.derivativePoints.append((firstPlottedPts,secondPlottedPts))
	    	except:
	    		pass
    
	def integralGenerator(self):
	    self.integralPoints = []
	    gridWidth, gridHeight = self.gridWidth,self.gridHeight
	    centerX, centerY = gridWidth/2, gridHeight/2
	    (userFactorX, userFactorY) = self.getFactors()
	    gridFactor = float(self.gridBoxSize)
	    scaleFactorX = float(self.gridBoxSize) * (1/userFactorX)
	    scaleFactorY = float(self.gridBoxSize) * (1/userFactorY)
	    (negativeX, positiveX) = (int(-gridWidth), int(gridWidth))
	    derivative = self.functions[2]
	    for i in xrange(negativeX, positiveX):
	        try: 
	    	    x = (i/gridFactor)*userFactorX
	    	    y = eval(derivative)
	    	    firstPlottedPts = (centerX + x*scaleFactorX, 
	    	    	               centerY - y*scaleFactorY)
	    	    x = ((i+1)/gridFactor)*userFactorX
	    	    y = eval(derivative)
	    	    secondPlottedPts = (centerX + x*scaleFactorX, 
	    	    	                centerY - y*scaleFactorY)
	    	    self.integralPoints.append((firstPlottedPts,secondPlottedPts))
	    	except:
	    		pass

	def drawIntegral(self):
		vertexPairs = self.integralPoints
		for vertexPair in vertexPairs:
			firstPlottedPoints, secondPlottedPts = vertexPair[0], vertexPair[1]
			self.mainProgramInstance.canvas.create_line(firstPlottedPoints,
		    secondPlottedPts, fill = 'red', width = 3)


	def drawDerivative(self):
		vertexPairs = self.derivativePoints
		for vertexPair in vertexPairs:
			firstPlottedPoints, secondPlottedPts = vertexPair[0], vertexPair[1]
			self.mainProgramInstance.canvas.create_line(firstPlottedPoints,
		    secondPlottedPts, fill = 'green', width = 3)


	def makeInterface(self):
		gridHeight = self.gridHeight
		canvasWidth = self.canvasWidth
		canvasHeight = self.canvasHeight
		interfaceColor = self.lineColor
		self.mainProgramInstance.canvas.create_rectangle(0, gridHeight, 
			                           canvasWidth, canvasHeight, 
			                           fill = interfaceColor)

	def graphRedrawAll(self):
		self.mainProgramInstance.canvas.delete(ALL)
		self.drawGrid()
		self.drawLegend()
		if(self.functionActive):
		    self.drawFunction()
		if(self.derivativeActive):
			self.drawDerivative()
		if(self.integralActive):
		    self.drawIntegral()
		self.makeInterface()

	def drawGrid(self):
		gridWidth, gridHeight = self.gridWidth, self.gridHeight
		boxSize = self.gridBoxSize
		verticalLines = self.gridWidth/self.gridBoxSize
		horizontalLines = self.gridHeight/self.gridBoxSize
		lineColor = self.lineColor
		self.mainProgramInstance.canvas.create_rectangle(0,0, gridWidth, 
			                                         gridHeight, fill = 'black')
		for line in xrange(verticalLines):
			nextXCoord = line*boxSize
			self.mainProgramInstance.canvas.create_line(nextXCoord,0, 
				            nextXCoord, gridHeight, fill = lineColor, width = 2)
		for line in xrange(horizontalLines):
			nextYCoord = line*boxSize
			self.mainProgramInstance.canvas.create_line(0, nextYCoord, 
				             gridWidth, nextYCoord, fill = lineColor, width = 2)
		self.drawAxes()

	def graphRun(self):
		self.graphInit()

    #initializes necessary instances, such as the input fields and check buttons
    #also sets the derivative and functions to 'ON' since that is how they are
    #at the beginning.
	def graphInit(self):
		self.inputText = GraphInputText(self.mainProgramInstance.root, self)
		self.inputFields = GraphInputField(self.mainProgramInstance.root)
		self.checkButtons = GraphCheckButton(self.mainProgramInstance.root, 
			                self, self.mainProgramInstance)
		self.commandButtons = GraphButton(self.mainProgramInstance.root,
			                                 self, self.mainProgramInstance)
		self.functionActive, self.derivativeActive, self.integralActive = (True,
		                                                              True,True)
		self.makeGraphScreenElements()
		#sets all of the toggles to on because all functions are displayed 
		#initially.
		self.checkButtons.derivativeStatus.set(1)
		self.checkButtons.functionStatus.set(1)
		self.checkButtons.integralStatus.set(1)
		#sets the increments or scale factors to 1 initially.
		self.inputFields.xIncrementField.insert(1,1)
		self.inputFields.yIncrementField.insert(1,1)
		self.functionPoints = []
		self.derivativePoints = []
		self.integralPoints = []
		self.equationsGenerator()

	def makeGraphScreenElements(self):
		self.inputText.makeGraphText()
		self.inputFields.makeGraphTextFields()
		self.checkButtons.makeCheckBoxes()
		self.commandButtons.makeGraphUpdateButton()
 
    #creates all of the points necessary for plotting the functions.
	def equationsGenerator(self):
		self.functionGenerator()
		self.derivativeGenerator()
		self.integralGenerator()

    #draws text that shows which functions are being graphed in their respective
    #colors.
	def drawLegend(self):
		function = self.mainProgramInstance.workingFunction
		derivative = self.mainProgramInstance.derivative
		integral = self.mainProgramInstance.integral
		functionText = "Function: %s" % function 
		derivativeText = "Derivative: %s" % derivative 
		integralText = "Integral: %s" % integral 
		self.mainProgramInstance.canvas.create_text(5,10, text = functionText, 
			                                     anchor = 'w', fill = 'yellow',
			                              font = ('Cambria Math', 13, 'italic',
			                              	      'bold'))
		self.mainProgramInstance.canvas.create_text(5,40, text = derivativeText, 
			                                       anchor = 'w',fill = 'green',
			                              font = ('Cambria Math', 13, 'italic',
			                              	       'bold'))
		self.mainProgramInstance.canvas.create_text(5,70, text = integralText, 
			                                        anchor = 'w', fill = 'red',
			                              font = ('Cambria Math', 13, 'italic',
			                              	      'bold'))

	def drawAxes(self):
		gridWidth, gridHeight = self.gridWidth, self.gridHeight
		midX, midY = gridWidth/2, gridHeight/2
		axesColor = 'purple'
		#creates vertical axis
		self.mainProgramInstance.canvas.create_line(midX, 0, midX, gridHeight, 
			                    fill = axesColor, width = 5)
		#creates horizontal axis
		self.mainProgramInstance.canvas.create_line(0, midY, gridWidth, midY, 
			                    fill = axesColor, width = 5)
		self.mainProgramInstance.canvas.create_text(self.gridWidth, 
			self.gridHeight/2, text = 'X',fill = 'white', anchor = 'ne', 
			                    font = ("Arial", 15, 'italic'))
		self.mainProgramInstance.canvas.create_text(self.gridWidth/2+10, 0, 
			text = 'Y', fill = 'white', anchor = 'n', 
			font = ("Arial", 15, 'italic'))
################################################################################
#creates instructions for the user 
#learned how to create this and expanded from 
#http://www.tutorialspoint.com/python/tk_label.htm
class GraphInputText(object):
	def __init__(self, window, graphProgramInstance):
		self.window = window
		self.graphProgramInstance = graphProgramInstance
		self.interfaceColor = self.graphProgramInstance.lineColor

	def makeGraphText(self):
		self.xIncrement = Label(self.window, 
			               text = 'Please Enter the X-Scale: ', 
			               bg = self.interfaceColor, fg = 'white')
		self.yIncrement = Label(self.window, 
			                text = 'Please Enter the Y-Scale: ',
			                bg = self.interfaceColor, fg = 'white')
		self.xIncrement.place(x = 10, y = 560)
		self.yIncrement.place(x = 10, y = 590)
################################################################################
#creates input field for the user to input their x and y values.
#learned how to make this by using 
#http://www.tutorialspoint.com/python/tk_entry.htm 
class GraphInputField(object):
	def __init__(self, window):
		self.window = window

	def makeGraphTextFields(self):
		#used DoubleVar class instance in order to store the information of the
		#field, as well as to be able to hold floats. 
		self.xIncrementFieldInt = DoubleVar()
		self.yIncrementFieldInt = DoubleVar()
		self.xIncrementField = Entry(self.window, 
			                         textvariable = self.xIncrementFieldInt)
		self.yIncrementField = Entry(self.window, 
			                         textvariable = self.yIncrementFieldInt)
		self.xIncrementField.place(x = 200, y = 560, width = 50)
		self.yIncrementField.place(x = 200, y = 590, width = 50)
################################################################################
#creates the check buttons to toggle the derivative and function on and off.
#idea taken from cs.cmu.edu/~112 on how to create it. I expanded more on the 
#use of it through http://www.tutorialspoint.com/python/tk_checkbutton.htm		
class GraphCheckButton(object):
	def __init__(self, window, graphProgramInstance, mainProgramInstance):
		self.window = window
		self.mainProgramInstance = mainProgramInstance
		self.graphProgramInstance = graphProgramInstance
		self.interfaceColor = self.graphProgramInstance.lineColor

	def makeCheckBoxes(self):
		#this creates a 'status' for the check box. So if it is on, it's status
		#is 1. If it is off, then it is 0. The status stores these values 
		self.derivativeStatus = IntVar() 
		self.derivativeToggle = Checkbutton(self.window, 
			                           bg = self.interfaceColor, 
			                           text = 'Derivative (Green)', 
			                           variable = self.derivativeStatus, 
			                           onvalue = 1, offvalue = 0, 
			         command = self.graphProgramInstance.updateToggleParameters,
			         fg = 'red')
		self.functionStatus = IntVar()
		self.functionToggle = Checkbutton(self.window, bg = self.interfaceColor, 
			                         text = 'Function (Yellow)',
			                         variable = self.functionStatus, 
			                         onvalue = 1, offvalue = 0,
			         command = self.graphProgramInstance.updateToggleParameters,
			         fg = 'red')
		self.integralStatus = IntVar()
		self.integralToggle = Checkbutton(self.window, bg = self.interfaceColor, 
			                              text = 'Integral (Red)', 
			                              variable = self.integralStatus, 
			                              onvalue = 1, offvalue = 0, 
			         command = self.graphProgramInstance.updateToggleParameters,
			         fg = 'red')
		self.derivativeToggle.place(x = 450, y = 560)
		self.functionToggle.place(x = 450, y = 590)
		self.integralToggle.place(x = 450, y = 620)
################################################################################
class GraphButton(object):
	def __init__(self, window, graphProgramInstance, mainProgramInstance):
		self.window = window
		self.graphProgramInstance = graphProgramInstance
		self.mainProgramInstance = mainProgramInstance

	def makeGraphUpdateButton(self):
		self.updateButton = Button(self.window, text = 'Update X&Y Scale', 
		            command = self.graphProgramInstance.updateKeyedParameters)
		self.updateButton.place(x = 10, y = 620)
		self.returnToMainScreenButton = Button(self.window, 
			                                text = "Return to Analysis",
	 command = self.mainProgramInstance.returnToMainScreenFromGraphScreen)
		self.returnToMainScreenButton.place(x = 575, y = 620)

def termProjectRun():
	program = CalculatorWindow()
	program.run()

termProjectRun()
