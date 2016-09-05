# import smtplib
# from email.mime.multipart import MIMEMultipart
# from smtplib import SMTP
#
# mail_message = MIMEMultipart()
# mail_message['Subject'] = "Sample Mail from python2"
#
# sender_email = "anurag.mala@4cinsights.com"
# recipients="anurag.mala@4cinsights.com"
# password = "Voxa3179"
# server_name = "smtp.office365.com"
# port = 587
# encryption = "TLS"
#
# # with SMTP(host=server_name, port=port) as mail_server:
# mail_server = smtplib.SMTP(host=server_name, port=port)
# mail_server.starttls()
# mail_server.login(sender_email, password)
# mail_server.sendmail(sender_email, recipients, mail_message.as_string())
# mail_server.quit()
#

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
    EvaluatedResult = None

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


            # Do reporting
    if OperatorKeyword is None:
        ReportString = "%s check on '%s'" % (checkType, s_LeftOperand)
    elif not RightOperand:
        ReportString = "%s check on '%s %s'" % (checkType, OperatorKeyword, s_LeftOperand)
    else:
        ReportString = "%s check on '%s %s %s'" % (checkType, s_LeftOperand, OperatorKeyword, s_RightOperand)



    if EvaluatedResult == "passed":
        BuiltIn().log(ReportString)
    else:
        raise CheckFailed(ReportString)
