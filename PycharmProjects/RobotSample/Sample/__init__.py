from Sample.LoggerUtil import LoggerUtil

log = LoggerUtil.logging
logLevel = LoggerUtil().LoggingLevel().DEBUG


@log(logLevel)
def fNametest_run(fname):
    assert(fname=="Anurag")," <Expected = Anurag> but <Actual="+fname+">"
