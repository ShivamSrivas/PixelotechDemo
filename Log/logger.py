import logging as log

def logger_call(path, process_id, message=None, intention=None):
    print(path,process_id,message,intention)
    log.basicConfig(filename=path, level=log.DEBUG, format='Date --> %(asctime)s , ProcessId --> ' + str(process_id) + ' , Message --> %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    log_func = log.info if intention == 'Info' else (log.warning if intention == 'Warn' else log.error)
    log_func(message)
