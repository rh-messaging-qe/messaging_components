import logging
import time

LOGGER = logging.getLogger(__name__)

class Utils:

    @staticmethod
    def retry(funct, expected_result, max_count=3, max_duration=None,
              result_funct=None, expected_exception=None, check_funct=None):
        """ retry method allowing repetitive calls (retries) and checking
        for expected value Useful for getting data from async methods,
         or for unstable results.

        Graphical representation:

        max_count =3
        max_duration = 10

        1st              2nd              3rd
        v   <- wait ->   v   <- wait ->   v
        +----------------------------------+
        0s                                 10s


        :type funct: types.FunctionType, function
        :param funct: function to be tested

        :type expected_result: any
        :param expected_result: expected result

        :type max_count: int
        :param max_count: maximum number of trials / tests

        :type max_duration: int, None
        :param max_duration maximum duration in seconds for trials / tests

        :type result_funct: types.FunctionType, function
        :param result_funct: optional result function instead of in_funct,
            in_funct will be executed as well, but not used for result

        :type expected_exception: exception, NoneType
        :param expected_exception: expected exception on funct or result_funct,
            other exceptions will re-raise the exception, expected not

        :type check_funct: types.FunctionType, function
        :param check_funct: function to compare/check function result
            and expected result, it has to accept 2 params,
            default "lambda a,b: a==b"

        :rtype: tuple
        :return: (<overall-result>, <last-function-execution-result>,
            <number-of-trials>, <total-time-wasted>)

        .. note:: Special case if in_retry_max_count==0,
            one trial/test is performed regardless of in_retry_max_duration
        """
        time_start = time.time()

        retry_result = False  # result for whole retry function
        funct_result = None  # result of called function

        if not check_funct:
            check_funct = lambda a, b: a == b

        elapsed = 0  # time measurement scoped outside of loop

        if not max_duration:
            max_duration = 0

        # wait between trials / rounds
        # -1 one compensates for last trial is at the end time
        if max_count <= 1:  # division by zero prevention
            round_wait_time = 0
        else:
            round_wait_time = float(max_duration) / (max_count - 1)
        LOGGER.debug("round_wait_time: %s" % round_wait_time)

        # special case, count==0 -> try once without waiting count=1,duration=0
        # this will ensure that even with count=0
        # the retry will check at least once
        if max_count == 0:
            max_count = 1
            max_duration = 0

        i = 1  # round counter scoped outside of loop
        for i in range(1, max_count + 1):
            # main loop
            act_exception = None
            result_exception = None

            # actuator function call, with exception catching
            try:
                funct_result = funct()
            except Exception as exc:
                act_exception = exc
                funct_result = None
                if (expected_exception is None
                        or not isinstance(exc, expected_exception)):
                    raise exc

            # result function call with exception catching, if exists
            if result_funct:
                try:
                    funct_result = result_funct()
                except Exception as exc:
                    result_exception = exc
                    funct_result = None
                    if (expected_exception is None
                            or not isinstance(exc, expected_exception)):
                        raise exc

            # main results checking
            if check_funct(funct_result, expected_result):
                retry_result = True

            # time criteria
            elapsed = time.time() - time_start
            LOGGER.info(
                "retry: round=%d/%s, elapsed=%.2f/%s, result=%s"
                % (i, max_count, elapsed, max_duration, retry_result)
            )

            if retry_result:
                # expected criteria met - exiting
                break

            # wait between rounds if enabled
            if max_duration > 0:
                if elapsed >= max_duration:
                    # total retry duration exceeded
                    break

            # if waiting is even enabled
            if round_wait_time > 0:
                sleep_time = i * round_wait_time - elapsed
                # if sleep is needed, maybe function takes lot of time to process
                if sleep_time > 0:
                    time.sleep(sleep_time)

        return retry_result, funct_result, i, elapsed