# Average Calculator Microservice

A Django-based microservice that calculates the average of unique numbers received from a third-party API.

## Features

- RESTful API that accepts qualified number IDs ('p' for prime, 'f' for Fibonacci, 'e' for even, and 'r' for random)
- Fetches numbers from a third-party server and stores them
- Ensures stored numbers are unique, discarding duplicates
- Ignores responses taking longer than 500ms or encountering errors
- Calculates the average of stored numbers within a configured window size
- Responds with the numbers stored before and after the latest API call, along with the average

## Installation

1. Clone the repository
2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```
   python manage.py migrate
   ```
4. Start the development server:
   ```
   python manage.py runserver 0.0.0.0:8000
   ```

## API Usage

### Endpoint

```
GET /numbers/{numberid}
```

Where `{numberid}` can be:
- `p` for prime numbers
- `f` for Fibonacci numbers
- `e` for even numbers
- `r` for random numbers

### Sample Request

```
GET http://localhost:8000/numbers/e
```

### Sample Response

```json
{
   "windowPrevState": [],
   "windowCurrState": [2, 4, 6, 8],
   "numbers": [2, 4, 6, 8],
   "avg": 5.00
}
```

## Configuration

The window size for the average calculation is configured in `settings.py` as `NUMBER_WINDOW_SIZE`. The default is 10.

## External APIs

The service integrates with the following third-party APIs:

- Prime Numbers API: `http://20.244.56.144/evaluation-service/primes`
- Fibonacci Numbers API: `http://20.244.56.144/evaluation-service/fibo`
- Even Numbers API: `http://20.244.56.144/evaluation-service/even`
- Random Numbers API: `http://20.244.56.144/evaluation-service/rand` 