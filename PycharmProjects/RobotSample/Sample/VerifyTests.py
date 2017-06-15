from Sample.LoggerUtil import LoggerUtil

log = LoggerUtil.logging
logLevel = LoggerUtil().LoggingLevel().DEBUG

@log(logLevel)
def lNametest_run(lname):
    assert(lname=="Mala")," <Expected = Mala> but <Actual="+lname+">"
