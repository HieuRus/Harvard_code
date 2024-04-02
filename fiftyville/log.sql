-- Keep a log of any SQL queries you execute as you solve the mystery.

--Examine description of crime scene report in details
SELECT street, description
FROM crime_scene_reports
WHERE year = 2021 AND month = 7 AND day = 28 AND street = "Humphrey Street";


--Examine the transcript of three witnesses mentioned about the crime scene on that day
SELECT name, transcript
FROM interviews
WHERE year = 2021 AND month = 7 AND day = 28 AND transcript like "%bakery%";


--Examine the license plate of people left the bakery parking lot on July28, 2021 at time frame 10:15am [base on FIRST interviewee]
SELECT license_plate
FROM bakery_security_logs
WHERE year = 2021 AND month = 7 AND day = 28 AND hour > 10 AND activity = "exit";


--Examine account number, amount of money which people withdrew at ATM machine on Leggett Street on July28, 2021 [based on SECOND interviewee]
SELECT account_number, amount
FROM atm_transactions
WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street"
ORDER BY amount DESC;


--Examine the caller, receiver occured on July28, 2021 with duration less than a minute [based on THIRD interviewee]
SELECT caller, receiver
FROM phone_calls
WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60;


-- Find ealiest fligh from "Fiftyville" on Jul 29, 2021
SELECT flights.id, origin_airport_id, destination_airport_id, full_name, city, hour, minute
FROM airports
JOIN flights ON airports.id = flights.origin_airport_id
WHERE year = 2021 AND month = 7 AND day = 29 AND city = "Fiftyville"
ORDER BY hour, minute;


--Examine people left Fiftyville city tomorrow [July29, 2021] around that time [based on THIRD interviewee]
SELECT name, p.passport_number, a1.city as left_city, a2.city as destination_city
FROM passengers as psenger
JOIN people as p ON psenger.passport_number = p.passport_number
JOIN flights ON flights.id= psenger.flight_id
JOIN airports as a1 ON a1.id = flights.origin_airport_id
JOIN airports as a2 ON a2.id = flights.destination_airport_id
WHERE year = 2021 AND month = 7 AND day = 29 AND a1.city = "Fiftyville" and hour > 10
ORDER BY name;


--QUERY TO FIND OUT who is the theft, city the theft escaped to, and accomplice
SELECT theft.name as theft, a2.city as destination_city, accomplice.name as accomplice
FROM people as theft
JOIN bank_accounts as ba ON theft.id = ba.person_id
JOIN atm_transactions as t ON ba.account_number = t.account_number AND t.year = 2021 AND t.month = 7 AND t.day = 28 AND t.atm_location = "Leggett Street"
JOIN phone_calls as pc ON theft.phone_number = pc.caller AND pc.year = 2021 AND pc.month = 7 AND pc.day = 28 AND pc.duration < 60
JOIN bakery_security_logs as sl ON theft.license_plate = sl.license_plate AND sl.year = 2021 AND sl.month = 7 AND sl.day = 28 AND sl.hour >= 10 AND sl.minute > 15 AND sl.minute < 25 AND sl.activity = "exit"
JOIN passengers as psenger ON theft.passport_number = psenger.passport_number
JOIN flights as f ON f.id = psenger.flight_id AND f.year = 2021 AND f.month = 7 AND f.day = 29 AND f.id = 36
JOIN airports as a1 on a1.id = f.origin_airport_id  AND a1.city = "Fiftyville"
JOIN airports as a2 on a2.id = f.destination_airport_id 
JOIN people AS accomplice ON pc.receiver = accomplice.phone_number;
