import logging

log = logging.getLogger('top')

import time
from javax.swing import JOptionPane
from javax.swing import JFrame

from robot.libraries.BuiltIn import BuiltIn, register_run_keyword
from robot.utils import timestr_to_secs


class CheckFailed(RuntimeError):
    ROBOT_CONTINUE_ON_FAILURE = True


class RobotChecks:
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self):
        pass

    @staticmethod
    def __isKeyword(keywordCandidate):
        try:
            BuiltIn().keyword_should_exist(keywordCandidate)
        except AssertionError, error:
            if hasattr(error, 'message') and "multiple keywords" in error.message.lower():
                # The same AssertionError exception is raised when no keyword exists and when
                # multiple keywords with the same name exist. Therefore the text message is checked
                # as well.
                return True
            else:
                return False
        else:
            return True

    def check_precondition(self, *args):
        """
        Identical to 'check that' but for use in precondition checks.

        Precondition checks are used to validate assumptions made at the start of a test case or
        keyword. When a precondition check fails it indicates that the test case did not reach the
        point where it was able to check the requirement it was testing for.
        """
        return RobotChecks.__execute_check("Precondition", *args)

    def check_postcondition(self, *args):
        """
        Identical to 'check that' but for use in postcondition checks

        Postcondition checks are typically used in reusable keywords. They are added to assert that
        the expected result of the action was achieved succesfully. A failing postcondition check
        causes the test case to fail, but indicates that the requirement it was testing for was not
        the cause of failure.
        """
        return RobotChecks.__execute_check("Postcondition", *args)

    def check_that(self, *args):
        """
        Check that is used to validate data or state from the system under test.

        Check that takes values and/or robot keywords as input and evaluates the results. If the
        check fails it causes the test case to fail. Check that has two basic forms.
        1) A single keyword (with its arguments) can be evaluated to a truth value
        2) Two values or keywords (with their arguments) can be evaluated using an operator. It will
        than have the form Check that <keyword or value> <operator> <keyword or value>.

        Example: Check that | Two times | 9 | equals | 18
        'Two times' in this example is assumed to be defined as a Robot keyword that takes one
        argument and multiplies it by 2. Check that will pass if the evaluated result of Two times 9
        equals the fixed expected value 18.

        Operator can be any Robot keyword taking exactly two values (left and right operands) as
        input. For a number of predefined operators on numeric, string and list types refer to
        library CheckOperator.

        Adding timing constraints:
                Any check can be extended with an additional timing constraint by adding 'within'
                e.g. Check that | condition becomes true | within | 1 minute 30 seconds
                This will cause the condition to be reevaluated until it becomes true, or until
                the specified time has passed. In the latter case the test case will fail.
        """

        Arguments = list(args)

        ############################################################################################
        # check for time argument
        TimeOutInSeconds = 0
        StartTime = time.clock()
        TimeRemaining = True
        s_TimeConstraint = ""
        if len(Arguments) >= 2 and Arguments[-2].lower() == 'within':
            EvaluatedTimeArg = RobotChecks.__evaluateOperand([Arguments[-1]])[0]
            TimeOutInSeconds = timestr_to_secs(EvaluatedTimeArg[0])
            s_TimeConstraint = Arguments[-1]
            Arguments = Arguments[:-2]

        print(TimeOutInSeconds)
        print(s_TimeConstraint)
        return RobotChecks.__execute_check("Requirement", *args)

    def check_manual(self, checkRequestText=""):
        """
        Suspends test execution to perform a manual or visual check.

        When used without arguments test execution is suspended until the tester clicks 'Ok'.
        Optionally a question can be passed as argument that will be prompted for answering by the
        tester during test execution. Answering 'No' will cause the test case to fail.
        There is no timeout. Test execution is suspended indefinitely.
        """
        dummyFrame = JFrame("Always On Top Frame")
        dummyFrame.setLocation(100, 100)
        dummyFrame.setAlwaysOnTop(True)
        if checkRequestText:
            TesterVerdict = JOptionPane.showConfirmDialog(dummyFrame,
                                                          "Robot test execution suspended for manual check.\n\n%s" % checkRequestText,
                                                          "Check manual", JOptionPane.YES_NO_OPTION)
            ReportString = "Manual check on '%s' [%s]" % (checkRequestText, TesterVerdict)
            if TesterVerdict == 0:
                BuiltIn().log(ReportString)
            else:
                raise CheckFailed(ReportString)

        else:
            JOptionPane.showConfirmDialog(dummyFrame, "Robot test execution suspended. Press OK to continue",
                                          "Check manual", JOptionPane.DEFAULT_OPTION)
        # Dispose resources used by dummyFrame
        dummyFrame.dispose()

    @staticmethod
    def __execute_check(checkType, *args):
        """
        Parse arguments for check keyword to determine its operands, evaluate them and execute the
        check.
        """
        Arguments = list(args)

        ############################################################################################
        # check for time argument
        TimeOutInSeconds = 0
        StartTime = time.clock()
        TimeRemaining = True
        s_TimeConstraint = ""
        if len(Arguments) >= 2 and Arguments[-2].lower() == 'within':
            EvaluatedTimeArg = RobotChecks.__evaluateOperand([Arguments[-1]])[0]
            TimeOutInSeconds = timestr_to_secs(EvaluatedTimeArg[0])
            s_TimeConstraint = Arguments[-1]
            Arguments = Arguments[:-2]

        if not len(Arguments):
            BuiltIn().fail("%s check failed. There was nothing to check." % checkType)

        ############################################################################################
        # Build expression
        LeftOperand = list()
        OperatorKeyword = None
        RightOperand = list()

        # Single argument or the first argument is a keyword AND No other arguments are keywords
        if len(Arguments) == 1 or \
                        RobotChecks.__isKeyword(Arguments[0]) and not filter(RobotChecks.__isKeyword, Arguments[1:]):
            # Interpret as single boolean expression
            LeftOperand = Arguments

        else:  # Interpret as expression
            LeftOperand.append(Arguments.pop(0))

            NextArgument = Arguments.pop(0)
            while not RobotChecks.__isKeyword(NextArgument):
                LeftOperand.append(NextArgument)

                # Prepare next loop
                if not len(Arguments):
                    BuiltIn().fail("Missing operator in check keyword")
                NextArgument = Arguments.pop(0)

            OperatorKeyword = NextArgument
            RightOperand = list(Arguments)

        ########################################################################################
        # Evaluate expression
        EvaluatedResult = None
        TimeLeft = TimeOutInSeconds
        while EvaluatedResult != "passed" and TimeRemaining:
            EvaluationStartTime = time.clock()
            if OperatorKeyword is None:
                # Evaluate boolean expression
                lValues, s_LeftOperand = RobotChecks.__evaluateOperand(LeftOperand)
                EvaluatedResult = "failed" if unicode(lValues[0]).lower() != "true" else "passed"

            else:
                lValues, s_LeftOperand = RobotChecks.__evaluateOperand(LeftOperand)

                if RightOperand:
                    rValues, s_RightOperand = RobotChecks.__evaluateOperand(RightOperand)
                    BuiltIn().log("Evaluating '%s' %s '%s'" % (s_LeftOperand, OperatorKeyword, s_RightOperand))
                    EvaluatedResult = BuiltIn().run_keyword(OperatorKeyword, *(lValues + rValues))

                else:
                    BuiltIn().log("Evaluating '%s' '%s'" % (OperatorKeyword, s_LeftOperand))
                    EvaluatedResult = BuiltIn().run_keyword(OperatorKeyword, *lValues)

                EvaluatedResult = "failed" if unicode(EvaluatedResult).lower() != "true" else "passed"
            EvaluationDuration = EvaluationStartTime - time.clock()

            # Optimise timing
            TimeLeft = (StartTime + TimeOutInSeconds) - time.clock()
            TimeRemaining = TimeLeft > 0
            if EvaluatedResult != "passed" and TimeRemaining:
                if TimeOutInSeconds > 60:
                    if TimeLeft < 25 or TimeOutInSeconds - TimeLeft < 20:
                        # Speed up check cycle during the first and last parts of the waiting time
                        # During these periods the expectation of completing the action is highest
                        time.sleep(5)
                    else:
                        # Use a fixed delay time taking the actual processing time into account
                        # taking samples at fixed intervals regardless of performance
                        time.sleep(max(20 - EvaluationDuration, 0))

                elif TimeOutInSeconds > 15:
                    time.sleep(5) if TimeLeft > 7 else time.sleep(2)
                else:
                    time.sleep(1) if TimeLeft > 2 else time.sleep(.2)

        # Do reporting
        if OperatorKeyword is None:
            ReportString = "%s check on '%s'" % (checkType, s_LeftOperand)
        elif not RightOperand:
            ReportString = "%s check on '%s %s'" % (checkType, OperatorKeyword, s_LeftOperand)
        else:
            ReportString = "%s check on '%s %s %s'" % (checkType, s_LeftOperand, OperatorKeyword, s_RightOperand)

        if s_TimeConstraint:
            if EvaluatedResult == "passed":
                ReportString += " after %d seconds" % (TimeOutInSeconds - TimeLeft)
            else:
                ReportString += " after %s" % s_TimeConstraint

        if EvaluatedResult == "passed":
            BuiltIn().log(ReportString)
        else:
            raise CheckFailed(ReportString)

    @staticmethod
    def __evaluateOperand(operand):
        # Create string variant of operands for reporting purposes
        s_Operand = " ".join([unicode(elm) for elm in operand])
        MultipleItems = False

        if RobotChecks.__isKeyword(operand[0]):
            Value = BuiltIn().run_keyword(*operand)
            BuiltIn().log("'%s' is '%s'" % (s_Operand, Value))

        else:
            if len(operand) == 1:
                Value = BuiltIn().replace_variables(operand[0])
                if Value == operand[0]:
                    BuiltIn().log("Interpreting '%s' as fixed value" % s_Operand)
                else:
                    BuiltIn().log(
                        "Interpreting '%s' as fixed value '%s'" % (s_Operand, RobotChecks.__toShortString(Value)))

            else:
                MultipleItems = True
                Value = list()
                for item in operand:
                    Value.append(BuiltIn().replace_variables(item))
                BuiltIn().log(
                    "Interpreting '%s' as multiple arguments '%s'" % (s_Operand, RobotChecks.__toShortString(Value)))

        if Value != operand[0]:
            # Add eveluated result for logging
            s_Operand += " [%s]" % RobotChecks.__toShortString(Value)

        return (Value, s_Operand) if MultipleItems else ([Value], s_Operand)

    @staticmethod
    def __toShortString(arg):
        s_Value = unicode(arg)
        if s_Value:
            if len(s_Value) > 33:
                s_Value = s_Value[:15] + "..." + s_Value[-15:]
        return s_Value


register_run_keyword('RobotChecks', RobotChecks.check_that)
register_run_keyword('RobotChecks', RobotChecks.check_precondition)
register_run_keyword('RobotChecks', RobotChecks.check_postcondition)
