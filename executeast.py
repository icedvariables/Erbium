class ExecuteAst:
    def __init__(self, ast):
        self.ast = ast
        self.statements = {
            "assign": self.statementAssign
        }
        self.expressions = {
            "int": self.expressionInt
        }
        self.variablesByScope = {"global":{}}
        self.currentScope = "global"

    def execute(self):
        for statement in self.ast:
            self.executeStatement(statement)

        return self.variablesByScope

    def executeStatement(self, statement):
        name = statement[0]
        args = statement[1:]
        statementFunction = self.statements.get(name, self.error)

        print "Executing statement '" + name + "' with args: " + str(args)

        statementFunction(*args)

    def executeExpression(self, expression):
        name = expression[0]
        args = expression[1:]
        expressionFunction = self.expressions.get(name, self.error)

        print "Evaluating expression '" + name + "' with args: " + str(args)

        return expressionFunction(*args)

    def statementAssign(self, name, value):
        scope = self.variablesByScope[self.currentScope]
        scope[name] = self.executeExpression(value)

    def expressionInt(self, value):
        return int(value)

    def error(*args):
        print "ERROR"
