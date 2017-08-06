class ExecuteAst:
    def __init__(self, ast):
        self.ast = ast
        self.instructions = {
            "assign": self.statementAssign
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
        statementFunction = self.instructions.get(name, self.error)

        print "Executing '" + name + "' with args: " + str(args)

        statementFunction(*args)

    def statementAssign(self, name, value):
        scope = self.variablesByScope[self.currentScope]
        scope[name] = value

    def error(*args):
        print "ERROR"
