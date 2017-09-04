# JumpCloud-QA-Assignment

## Application URL
http://radiant-gorge-83016.herokuapp.com/ 

## Details
The application has bugs, so develop a test plan to find them.

- When launched the application should wait for http connections
- It should support three endpoints
** A  POST  to  /hash  should accept a password; it should return a job identifier immediately; it should then wait 5 seconds and compute the password hash. The hashing algorithm should be SHA512.
** A  GET  to  /hash  should accept a job identifier; it should return the base64 encoded password hash for the corresponding  POST  request.
** A  GET  to  /stats   should accept no data; it should return a JSON data structure for the total hash requests since server start and the average time of a hash request in milliseconds
- The software should be able to process multiple connections simultaneously.
- The software should support a graceful shutdown request, it should allow any remaining password hashing to complete, reject any new requests, and shutdown

## Notes about Heroku
- After ~30 minutes of inactivity heroku automatically spins down the process, so initial requests may take up to 10 or 15 seconds for the process to boot
- All stats and hashes are stored in memory, so crashes, shutdowns, and the above process lifecycle will cause data loss (to be clear this is intended and not a bug)
- Since this is a hosted binary, you will have to detect shutdowns by checking if the previous data has been erased (Heroku will immediately restart the process after a shutdown)

## Example Curl Requests and Response
- curl -X POST -H "application/json" -d '{"password":"angrymonkey"}' http://radiant-gorge-83016.herokuapp.com/hash
> 42

- curl http://radiant-gorge-83016.herokuapp.com/hash/42
> NN0PAKtieayiTY8/Qd53AeMzHkbvZDdwYYiDnwtDdv/FIWvcy1sKCb7qi7Nu8Q8Cd/MqjQeyCI0pWKDGp74A1g==

- curl http://radiant-gorge-83016.herokuapp.com/stats
> {"TotalRequests":3,"AverageTime":93438}

- curl -X POST -d 'shutdown' http://radiant-gorge-83016.herokuapp.com/hash                       
> <200 Empty Response>

## Running the code
Install all necessary modules found in requirements.txt. Then, download the code and run the following:
```
python PasswordHashingTest.py
```
