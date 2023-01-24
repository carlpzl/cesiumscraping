import functools
from functools import wraps


def func_retry(func=None, max_attempts=3):
    """ DECORATOR Function Retry
    Use this as a decorator to retry a function that returns None/False on failure and a non-null/True on passing.
    :param (obj) func: Calling Function
    :param (int) max_attempts:
    :param (bool) all_pass: if True, all retries MUST pass, then test pass.
                            if False, as long as one of retry pass, then test pass.
    :return:
    """

    if func is None:
        return functools.partial(func_retry, max_attempts=max_attempts)

    @functools.wraps(func)
    def func_wrapper(*args, **kwargs):
        cnt = 0
        result = ''
        r = None
        while cnt <= max_attempts:

            print("FUNC {0} attempt: {1}".format(func.__name__, cnt))
            try:
                r = func(*args, **kwargs)
                break
            except Exception as e:
                cnt += 1
                print('Exception error: {}'.format(e))
                if cnt < 4:
                    print('next attempt...')

                else:
                    raise Exception('after 3 attempts something wrong')

        result = 'Pass' if cnt < 4 else 'Fail'
        print('Function {0} result is: {1}'.format(func.__name__, result))

        return r

    return func_wrapper
