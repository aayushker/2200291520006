# Stock Price Aggregation Microservice

A Django-based microservice for stock price analysis that provides average price calculations and correlation between stocks.

## Features

- RESTful API for retrieving average stock prices with historical data
- API for calculating the correlation between two stocks' price movements
- Efficient caching to minimize external API calls
- Calculation of Pearson's correlation coefficient for stock price analysis

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

### Average Stock Price API

Get the average price of a stock in the last m minutes.

```
GET /stocks/:ticker?minutes=m&aggregation=average
```

#### Parameters:
- `ticker`: The stock ticker symbol (e.g., NVDA, AAPL)
- `minutes`: Time window in minutes
- `aggregation`: Set to 'average' for average calculation

#### Example:
```
GET /stocks/NVDA?minutes=50&aggregation=average
```

#### Response:
```json
{
    "averageStockPrice": 453.569744,
    "priceHistory": [
        {
            "price": 231.95296,
            "lastUpdatedAt": "2025-05-08T04:26:27.4658491Z"
        },
        {
            "price": 124.95156,
            "lastUpdatedAt": "2025-05-08T04:30:23.465940341Z"
        },
        ...
    ]
}
```

### Stock Correlation API

Calculate the correlation between two stocks in the last m minutes.

```
GET /stockcorrelation?minutes=m&ticker={TICKER1}&ticker={TICKER2}
```

#### Parameters:
- `minutes`: Time window in minutes
- `ticker`: Two stock ticker symbols (repeated parameter)

#### Example:
```
GET /stockcorrelation?minutes=50&ticker=NVDA&ticker=PYPL
```

#### Response:
```json
{
    "correlation": -0.9367,
    "stocks": {
        "NVDA": {
            "averagePrice": 204.000025,
            "priceHistory": [
                {
                    "price": 231.95296,
                    "lastUpdatedAt": "2025-05-08T04:26:27.4658491Z"
                },
                ...
            ]
        },
        "PYPL": {
            "averagePrice": 458.606756,
            "priceHistory": [
                {
                    "price": 680.59766,
                    "lastUpdatedAt": "2025-05-09T02:04:27.464908465Z"
                },
                ...
            ]
        }
    }
}
```

## Note on API Usage

The system implements efficient caching to minimize external API calls, which are rate-limited and incur costs. When data is requested, the system first checks if it has recent cached data before making an external API call. 