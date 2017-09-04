from HTTPSession import HTTPSession
from multiprocessing import Pool, Process, Queue
import json
import hashlib
import base64
import time

def post_hash(password, queue=None):
    """
    Function to submit POST request to hash endpoint.

    Args:
        password (str): Password to be hashed and ecoded.
        queue (obj): Multiprocessing queue object to hold response object

    Returns:
        res (obj): Response object from POST request
    """

    http_session = HTTPSession()
    endpoint = '/hash'
    params = {
        'password' : password
    }

    res = http_session.rs.post(http_session.baseurl + endpoint, json=params)

    if queue is not None:
        queue.put(res)
    else:
        return res

def get_hash(job_id):
    """
    Function to submit GET request to hash endpoint.

    Args:
        job_id (str): Job ID that links POST request to encoded password hash.

    Returns:
        res (obj): Response object from GET request
    """

    time.sleep(7)

    http_session = HTTPSession()
    endpoint = '/hash'

    res = http_session.rs.get(http_session.baseurl + endpoint + '/' + job_id)

    return res

def get_stats():
    """
    Function to submit GET request to stats endpoint.

    Args:

    Returns:
        res (obj): Response object from GET request
    """

    http_session = HTTPSession()
    endpoint = '/stats'

    res = http_session.rs.get(http_session.baseurl + endpoint)

    return res

def shutdown(queue=None):
    """
    Function to submit Shutdown request to hash endpoint.

    Args:
        queue (obj): Multiprocessing queue object to hold response object

    Returns:
        res (obj): Response object from POST request
    """

    http_session = HTTPSession()
    endpoint = '/hash'
    data = 'shutdown'

    res = http_session.rs.post(http_session.baseurl + endpoint, data=data)

    if queue is not None:
        queue.put(res)
    else:
        return res

def is_json(res):
    """
    Function to validate JSON for response object

    Args:
        res (obj): Response object from a request.

    Returns:
        bool: Returns True if response is valid JSON, else returns False.
    """
    try:
        json.loads(res.text)
    except ValueError as error:
        return False
    return True

def is_key(res, key):
    """
    Function to validate key in JSON for response object

    Args:
        res (obj): Response object from a request.
        key (str): Key to check for in response

    Returns:
            bool: Returns True if key exists, else returns False.
    """
    if is_json(res):
        json_contents = json.loads(res.text)
        if key in json_contents:
            return True
        else:
            return False
    else:
        return False

def is_shutdown_over():
    """
    Function to validate shutdown is over

    Args:

    Returns:
            bool: Returns True once shutdown is over.
    """
    shutdown_over = False
    while(not shutdown_over):
        res = get_stats()
        if (res.status_code < 300 and res.status_code >=200):
            shutdown_over = True
        else:
            time.sleep(300)
    return shutdown_over

def test_is_post_hash_successful(password):
    """
    Test to check that POST request to hash endpoint is successful

    Args:
        password (str): Password to be hashed and ecoded.

    Returns:
    """

    res = post_hash(password)

    if (res.status_code >= 300 or res.status_code < 200):
        print 'FAIL: test_is_post_hash_successful'
        print 'Expected Status Code: 2xx'
        print 'Actual Status Code: ' + str(res.status_code)
    else:
        print 'PASS: test_is_post_hash_successful'

def test_is_get_hash_successful(password):
    """
    Test to check that GET request to hash endpoint is successful

    Args:
        password (str): Password to be hashed and ecoded.

    Returns:
    """

    post_res = post_hash(password)
    get_res = get_hash(post_res.text)

    if (get_res.status_code >= 300 or get_res.status_code < 200):
        print 'FAIL: test_is_get_hash_successful'
        print 'Expected Status Code: 2xx'
        print 'Actual Error Code: ' + str(get_res.status_code)
    else:
        print 'PASS: test_is_get_hash_successful'

def test_is_get_stats_successful():
    """
    Test to check that GET request to stats endpoint is successful

    Args:

    Returns:
    """

    res = get_stats()

    if (res.status_code >= 300 or res.status_code < 200):
        print 'FAIL: test_is_get_stats_successful'
        print 'Expected Status Code: 2xx'
        print 'Actual Error Code: ' + str(res.status_code)
    else:
        print 'PASS: test_is_get_stats_successful'

def test_is_shutdown_successful():
    """
    Test to check that shutting down is successful

    Args:

    Returns:
    """

    res = shutdown()

    if (res.status_code >= 300 or res.status_code < 200):
        print 'FAIL: test_is_shutdown_successful'
        print 'Expected Status Code: 2xx'
        print 'Actual Status Code: ' + str(res.status_code)
    else:
        print 'PASS: test_is_shutdown_successful'

def test_is_job_identifier_returned(password):
    """
    Test to check that job identifier is returned when submitting POST request to hash endpoint

    Args:
        password (str): Password to be hashed and ecoded.

    Returns:
    """

    res = post_hash(password)

    if not res.text:
        print 'FAIL: test_is_job_identifier_returned'
        print 'Job identifier is expected to be returned'
        print 'No job identifier was returned'
    else:
        print 'PASS: test_is_job_identifier_returned'

def test_is_job_identifier_returned_immediately(password):
    """
    Test to check that job identifier is returned immediately when submitting POST request to hash endpoint

    Args:
        password (str): Password to be hashed and ecoded.

    Returns:
    """

    start = time.time()
    res = post_hash(password)
    round_trip = time.time() - start

    if round_trip > 2:
        print 'FAIL: test_is_job_identifier_returned_immediately'
        print 'Job identifier not returned immediately'
        print 'Job identifier took ' + str(round_trip) + ' seconds to return'
        print 'Job identifier expected to return in less than 2 seconds'
    else:
        print 'PASS: test_is_job_identifier_returned_immediately'

def test_is_get_hash_without_job_identifier_allowed():
    """
    Test to check that GET request to hash endpoint without a job identifier is not allowed

    Args:

    Returns:
    """

    http_session = HTTPSession()
    endpoint = '/hash'

    res = http_session.rs.get(http_session.baseurl + endpoint)

    if res.status_code >= 400:
        print 'PASS: test_is_get_hash_without_job_identifier_allowed'
    else:
        print 'FAIL: test_is_get_hash_without_job_identifier_allowed'
        print 'GET request to hash endpoint without a job identifier should not be allowed'

def test_is_password_encoded(password):
    """
    Test to check that password is hashed using SHA512 hashing algorithm and base64 econded.

    Args:
        password (str): Password to be hashed and ecoded.

    Returns:
    """

    post_res = post_hash(password)
    get_res = get_hash(post_res.text)

    expected_encode = base64.b64encode(hashlib.sha512(password).hexdigest())

    if get_res.text != expected_encode:
        print 'FAIL: test_is_password_encoded'
        print 'Expected Ecodeed Value: ' + expected_encode
        print 'Actual Encoded Value: ' + get_res.text
    else:
        print 'PASS: test_is_password_encoded'

def test_is_empty_string_allowed_as_password(password):
    """
    Test to check that an empty string cannot be passed as a password

    Args:
        password (str): Password to be hashed and ecoded.

    Returns:
    """

    res = post_hash(password)

    if (res.status_code < 300 and res.status_code >= 200):
        print 'FAIL: test_is_empty_string_allowed_as_password'
        print 'Empty string should not be allowed as a password'
    else:
        print 'PASS: test_is_empty_string_allowed_as_password'

def test_is_malformed_input_post_hash_allowed():
    """
    Test to check that malformed JSON cannot be passed in the POST request to hash endpoint

    Args:

    Returns:
    """

    http_session = HTTPSession()
    endpoint = '/hash'
    params = 'password'

    res = http_session.rs.post(http_session.baseurl + endpoint, json=params)

    if res.status_code >= 400:
        print 'PASS: test_is_malformed_input_post_hash_allowed'
    else:
        print 'FAIL: test_is_malformed_input_post_hash_allowed'
        print 'Malformed JSON should not be allowed in POST request to hash endpoint'

def test_is_different_key_post_hash_allowed(password):
    """
    Test to check that a key other than password cannot be passed in POST request to hash endpoint

    Args:
        password (str): Password to be hashed and ecoded.

    Returns:
    """
    http_session = HTTPSession()
    endpoint = '/hash'
    params = {
        'p' : password
    }

    res = http_session.rs.post(http_session.baseurl + endpoint, json=params)

    if res.status_code >= 400:
        print 'PASS: test_is_different_key_post_hash_allowed'
    else:
        print 'FAIL: test_is_different_key_post_hash_allowed'
        print 'password should be the only key allowed in POST request to hash endpoint'
        print 'Passed Key: p'

def test_is_passing_empty_json_allowed():
    """
    Test to check that empty JSON cannot be passed in POST request to hash endpoint

    Args:

    Returns:
    """

    http_session = HTTPSession()
    endpoint = '/hash'
    params = {}

    res = http_session.rs.post(http_session.baseurl + endpoint, json=params)

    if res.status_code >= 400:
        print 'PASS: test_is_passing_empty_json_allowed'
    else:
        print 'FAIL: test_is_passing_empty_json_allowed'
        print 'Empty JSON should not be allowed to be passed to the hash endpoint'

def test_is_stats_response_json():
    """
    Test to check that GET request to stats endpoint returns JSON response

    Args:

    Returns:
    """

    res = get_stats()
    if not is_json(res):
        print 'FAIL: test_is_stats_response_json'
        print 'Expected Response Should be valid JSON'
        print 'Actual Response: ' + res.text
    else:
        print 'PASS: test_is_stats_response_json'

def test_is_TotalRequests_key():
    """
    Test to check that TotalRequests is a Key in JSON Response from stats endpoint

    Args:

    Returns:
    """

    key = 'TotalRequests'
    res = get_stats()

    if not is_key(res, key):
        print 'FAIL: test_is_TotalRequests_key'
        print  key + ' should be Key in JSON response'
        print 'Actual Response: ' + res.text
    else:
        print 'PASS: test_is_TotalRequests_key'

def test_is_AverageTime_key():
    """
    Test to check that AverageTime is a Key in JSON Response from stats endpoint

    Args:

    Returns:
    """

    key = 'AverageTime'
    res = get_stats()

    if not is_key(res, key):
        print 'FAIL: test_is_AverageTime_key'
        print key + ' should be Key in JSON response'
        print 'Actual Response: ' + res.text
    else:
        print 'PASS: test_is_AverageTime_key'

def test_is_post_stats_allowed():
    """
    Test to check that the stats endpoint does not support POST

    Args:

    Returns:
    """

    http_session = HTTPSession()
    endpoint = '/stats'

    res = http_session.rs.post(http_session.baseurl + endpoint)

    if res.status_code >= 400:
        print 'PASS: test_is_post_stats_allowed'
    else:
        print 'FAIL: test_is_post_stats_allowed'
        print 'The stats endpoint should not support POST requests'

def test_is_params_in_get_stats_request_allowed():
    """
    Test to check that the stats endpoint does not support parameters on GET request

    Args:

    Returns:
    """

    http_session = HTTPSession()
    endpoint = '/stats'

    res = http_session.rs.get(http_session.baseurl + endpoint + '?name1=value1&name2=value2')

    if res.status_code >= 400:
        print 'PASS: test_is_params_in_get_stats_request_allowed'
    else:
        print 'FAIL: test_is_params_in_get_stats_request_allowed'
        print 'The stats endpoint should not support parameters in URL in GET request'

def test_is_TotalRequests_incremented_successfully(password):
    """
    Test to check that TotalRequests is incremented successfully

    Args:
        password (str): Password to be hashed and ecoded.

    Returns:
    """

    res = get_stats()
    data = res.json()
    preincrement_TotalRequests = data['TotalRequests']

    expected_TotalRequests = data['TotalRequests'] + 1

    post_hash(password)
    res = get_stats()
    data = res.json()
    actual_TotalRequests = data['TotalRequests']

    if actual_TotalRequests == expected_TotalRequests:
        print 'PASS: test_is_TotalRequests_incremented_successfully'
    else:
        print 'FAIL: test_is_AverageTime_calculated_correctly'
        print 'Expected Value: ' + str(expected_TotalRequests)
        print 'Actual Value: ' + str(actual_TotalRequests)

def test_is_simultaneous_post_hash_successful(passwords):
    """
    Test to check that simultaneous POST requests are supported for hash endpoint.

    Args:
        passwords (str list): Passwords to be hashed and ecoded.

    Returns:
    """
    success = True
    processes = Pool(processes=10)
    responses = processes.map_async(post_hash, passwords).get(999999)
    for res in responses:
        if (res.status_code >= 300 or res.status_code < 200):
            success = False
            break

    if not success:
        print 'FAIL: test_is_simultaneous_post_hash_successful'
        print 'Expected Status Code form: 2xx'
        print 'At least one process had a status code that was not of the form 2xx'
    else:
        print 'PASS: test_is_simultaneous_post_hash_successful'

def test_is_simultaneous_get_hash_successful(passwords):
    """
    Test to check that simultaneous GET requests are supported for hash endpoint.

    Args:
        passwords (str list): Passwords to be hashed and ecoded.

    Returns:
    """

    job_ids = []
    for password in passwords:
        post_res = post_hash(password)
        job_ids.append(post_res.text)

    success = True
    processes = Pool(processes=10)
    responses = processes.map_async(get_hash, job_ids).get(999999)

    for res in responses:
        if (res.status_code >= 300 or res.status_code < 200):
            success = False
            break

    if not success:
        print 'FAIL: test_is_simultaneous_get_hash_successful'
        print 'Expected Status Code form: 2xx'
        print 'At least one process had a status code that was not of the form 2xx'
    else:
        print 'PASS: test_is_simultaneous_get_hash_successful'

def test_is_remaining_password_hashing_allowed_to_complete(password):
    """
    Test to check that remaining password hashings are allowed to complete.

    Args:
        passwords (str): Password to be hashed and ecoded.

    Returns:
    """

    shutdown_over = False
    while (not shutdown_over):
        shutdown_over = is_shutdown_over()

    queue = Queue()
    p1 = Process(target=post_hash, args=(password,queue,))
    p1.start()
    p2 = Process(target=shutdown, args=(queue,))
    p2.start()

    shutdown_res = queue.get()

    if (shutdown_res.status_code >= 300 or shutdown_res.status_code < 200 or shutdown_res.text):
        print 'FAIL: test_is_remaining_password_hashing_allowed_to_complete'
        print 'Shutdown did not succeed or shutdown response did not come first'
        print 'Shutdown Response: ' + shutdown_res.text
    else:
        post_res = queue.get()
        if (post_res.status_code >= 300 or post_res.status_code < 200 or not post_res.text):
            print 'FAIL: test_is_remaining_password_hashing_allowed_to_complete'
            print 'POST to Hash did not succeed or response was empty'
            print 'POST Response: ' + post_res.text
        else:
            print 'PASS: test_is_remaining_password_hashing_allowed_to_complete'

def test_is_new_requests_rejected_during_shutdown(password):
    """
    Test to check that new requests are rejected during shutdown.

    Args:
        passwords (str): Password to be hashed and ecoded.

    Returns:
    """

    shutdown_over = False
    while (not shutdown_over):
        shutdown_over = is_shutdown_over()

    queue = Queue()

    p1 = Process(target=shutdown, args=(queue,))
    p1.start()

    p2 = Process(target=post_hash, args=(password,queue,))

    shutdown_res = queue.get()

    p2.start()

    if (shutdown_res.status_code >= 300 or shutdown_res.status_code < 200 or shutdown_res.text):
        print 'FAIL: test_is_new_requests_rejected_during_shutdown'
        print 'Shutdown did not succeed'
        print 'Shutdown Response: ' + shutdown_res.text
    else:
        post_res = queue.get()
        if (post_res.status_code < 300 and post_res.status_code >= 200):
            print 'FAIL: test_is_new_requests_rejected_during_shutdown'
            print 'POST to Hash succeeded'
            print 'POST Response: ' + post_res.text
        else:
            print 'PASS: test_is_new_requests_rejected_during_shutdown'

def test_is_AverageTime_calculated_correctly(passwords):
    """
    Test to check that AverageTime is calculated correctly.

    Args:
        passwords (str list): Passwords to be hashed and ecoded.

    Returns:
    """

    shutdown()

    shutdown_over = False
    while (not shutdown_over):
        shutdown_over = is_shutdown_over()

    total_time = 0
    for password in passwords:
        start = time.time()
        res = post_hash(password)
        round_trip = time.time() - start
        total_time = total_time + round_trip

    expected_AverageTime = str(int((total_time / len(passwords)) * 1000))[:5]

    res = get_stats()
    data = res.json()

    actual_AverageTime = data['AverageTime']

    if actual_AverageTime == expected_AverageTime:
        print 'PASS: test_is_AverageTime_calculated_correctly'
    else:
        print 'FAIL: test_is_AverageTime_calculated_correctly'
        print 'Expected Value: ' + str(expected_AverageTime)
        print 'Actual Value: ' + str(actual_AverageTime)

def test_is_get_hash_with_non_existent_job_identifier_allowed():
    """
    Test to check that GET request hash endpoint with a non existent job identifier is not supported.

    Args:

    Returns:
    """

    shutdown()

    shutdown_over = False
    while (not shutdown_over):
        shutdown_over = is_shutdown_over()

    non_existent_job_identifier = '999'
    res = get_hash(non_existent_job_identifier)

    if res.status_code >= 400:
        print 'PASS: test_is_get_hash_with_non_existent_job_identifier_allowed'
    else:
        print 'FAIL: test_is_get_hash_with_non_existent_job_identifier_allowed'
        print 'The hash endpoint should not support GET request with non existent job identifier'

def main():
    """
    Run through all tests for http://radiant-gorge-83016.herokuapp.com

    Returns:
    """

    password = 'angrymonkey'
    passwords = ['angry', 'monkey', 'almond', 'ham', 'sam', 'MILK','hfhf123', 'Ll', '1245', 'aB123']
    empty_string = ''

    test_is_post_hash_successful(password)
    test_is_get_hash_successful(password)
    test_is_get_stats_successful()
    test_is_job_identifier_returned(password)
    test_is_job_identifier_returned_immediately(password)
    test_is_get_hash_without_job_identifier_allowed()
    test_is_password_encoded(password)
    test_is_empty_string_allowed_as_password(empty_string)
    test_is_malformed_input_post_hash_allowed()
    test_is_different_key_post_hash_allowed(password)
    test_is_passing_empty_json_allowed()
    test_is_stats_response_json()
    test_is_TotalRequests_key()
    test_is_AverageTime_key()
    test_is_post_stats_allowed()
    test_is_params_in_get_stats_request_allowed()
    test_is_TotalRequests_incremented_successfully(password)
    test_is_simultaneous_post_hash_successful(passwords)
    test_is_simultaneous_get_hash_successful(passwords)
    test_is_shutdown_successful()
    test_is_remaining_password_hashing_allowed_to_complete(password)
    test_is_new_requests_rejected_during_shutdown(password)
    test_is_AverageTime_calculated_correctly(passwords)
    test_is_get_hash_with_non_existent_job_identifier_allowed()

if __name__ == '__main__':
    main()
