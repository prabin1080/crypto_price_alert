### Building and running application

Build Docker Container
```bash
docker compose build
```
Migrate DB:
```bash
docker compose run server ./manage.py migrate
```
Create Superuser:
```bash
docker compose run server ./manage.py createsuperuser
```
Run:
```bash
docker compose up
```


### API Details

#### Getting JWT Token:
```bash
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "prabin", "password": "password"}' \
  http://localhost:8000/auth/token/
```
```json
{
  "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwOTA3MzU4MSwiaWF0IjoxNzA4OTg3MTgxLCJqdGkiOiIyMDI2NzY1ZjZlNjE0NWNlYTg0MTFlOWEwMzE1NDFiNCIsInVzZXJfaWQiOjF9.MA4gRYbr7BqVbsVZRDXqdz-nysi7H4gndYUeyIn9Pzo",
  "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA4OTg3NDgxLCJpYXQiOjE3MDg5ODcxODEsImp0aSI6IjFmNDJlY2U1NGE5MTQyYjZiZmU2OTAzZDBjNmM1OGMyIiwidXNlcl9pZCI6MX0.rZDL97JIYTgRKDze0Hn-d27XhPOYMCYAdvC8tI0kbM4"
}
```

#### Refresh JWT Token
```bash
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwOTA3MzU4MSwiaWF0IjoxNzA4OTg3MTgxLCJqdGkiOiIyMDI2NzY1ZjZlNjE0NWNlYTg0MTFlOWEwMzE1NDFiNCIsInVzZXJfaWQiOjF9.MA4gRYbr7BqVbsVZRDXqdz-nysi7H4gndYUeyIn9Pzo"}' \
  http://localhost:8000/auth/token/refresh/
```
```json
{
  "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA4OTg4MDYzLCJpYXQiOjE3MDg5ODcxODEsImp0aSI6Ijk1YjRmODIxMDdmNTQyZDJhYjNkNmNjMDNmMjNjMjg5IiwidXNlcl9pZCI6MX0.9gUcG-h7OeZSzFzM8by7tkO-qxCgDlXB0Lu69YaDn50"
}
```

#### Alert Create Api
```bash
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA5MDIwMjc0LCJpYXQiOjE3MDkwMTY2NzQsImp0aSI6ImFlMzJlNTMzOWM3OTQxYTY5ZmM1NmIyOGQ5MjExMmIxIiwidXNlcl9pZCI6MX0.J3Au9f-MBV68tlzAiOyGBl-6A2kWhJoF5571N-F9klo" \
  -d '{"asset": "BTCUSDT", "price": 60000}' \
  http://127.0.0.1:8000/alert/
```
```json
{
  "id":6,
  "asset":"BTCUSDT",
  "price":60000.0,
  "status":"CREATED",
  "created":"2024-02-27T06:02:21.990852Z"
}
```

#### Alert List Api
Query params
* status (CREATED/DELETED/TRIGGERED)
* page_size (defaults=10)
* page (defaults=1)

```bash
curl \
  -X GET \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA5MDIwMjc0LCJpYXQiOjE3MDkwMTY2NzQsImp0aSI6ImFlMzJlNTMzOWM3OTQxYTY5ZmM1NmIyOGQ5MjExMmIxIiwidXNlcl9pZCI6MX0.J3Au9f-MBV68tlzAiOyGBl-6A2kWhJoF5571N-F9klo" \
  "http://127.0.0.1:8000/alert/?status=CREATED&page_size=2"
```
```json
{
  "count":3,
  "next":"http://127.0.0.1:8000/alert/?page=2&page_size=2&status=CREATED",
  "previous":null,
  "results":[
    {
      "id":4,
      "asset":"BTCUSDT",
      "price":1001.0,
      "status":"CREATED",
      "created":"2024-02-26T19:53:08.593833Z"},
    {
      "id":3,
      "asset":"ETHUSDT",
      "price":4000.0,
      "status":"CREATED",
      "created":"2024-02-26T19:52:48.754738Z"
    }
  ]
}
```

#### Alert Retrieve Api
```bash
curl \
  -X GET \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA5MDIwMjc0LCJpYXQiOjE3MDkwMTY2NzQsImp0aSI6ImFlMzJlNTMzOWM3OTQxYTY5ZmM1NmIyOGQ5MjExMmIxIiwidXNlcl9pZCI6MX0.J3Au9f-MBV68tlzAiOyGBl-6A2kWhJoF5571N-F9klo" \
  http://127.0.0.1:8000/alert/6/
```
```json
{
  "id":6,
  "asset":"BTCUSDT",
  "price":70000.0,
  "status":"CREATED",
  "created":"2024-02-27T06:02:21.990852Z"
}
```
#### Alert Update Api
```bash
curl \
  -X PUT \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA5MDIwMjc0LCJpYXQiOjE3MDkwMTY2NzQsImp0aSI6ImFlMzJlNTMzOWM3OTQxYTY5ZmM1NmIyOGQ5MjExMmIxIiwidXNlcl9pZCI6MX0.J3Au9f-MBV68tlzAiOyGBl-6A2kWhJoF5571N-F9klo" \
  -d '{"asset": "BTCUSDT", "price": 70000}' \
  http://127.0.0.1:8000/alert/6/
```
```json
{
  "id":6,
  "asset":"BTCUSDT",
  "price":70000.0,
  "status":"CREATED",
  "created":"2024-02-27T06:02:21.990852Z"
}
```

#### Alert Delete Api
```bash
curl \
  -X DELETE \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA5MDIwMjc0LCJpYXQiOjE3MDkwMTY2NzQsImp0aSI6ImFlMzJlNTMzOWM3OTQxYTY5ZmM1NmIyOGQ5MjExMmIxIiwidXNlcl9pZCI6MX0.J3Au9f-MBV68tlzAiOyGBl-6A2kWhJoF5571N-F9klo" \
  http://127.0.0.1:8000/alert/6/
```
```json
{
  "id":6,
  "asset":"BTCUSDT",
  "price":70000.0,
  "status":"DELETED",
  "created":"2024-02-27T06:02:21.990852Z"
}
```
### Solution
* Subscribed to Binance websocket in [alert/fetch_prices.py](alert/fetch_prices.py) which runs as a separate service
* Crypto assets can be listed at [ASSETS](crypto_price_alert/constants.py)
* [alert/process_prices.py](alert/process_prices.py) collects all the data in a local variable and put in use every [DB_ALERT_CHECK_INTERVAL](crypto_price_alert/constants.py) to create tasks
* When a user creates an Alert, it has an automatic flag [track_type](alert/models.py) assigned to it dependig on the current market price to look for either up or low, handled by [Alert.objects.set_track_type](alert/models.py)
* [Alert.objects.get_alert_eligible_queryset]((alert/models.py)) returns all the eligible records ready to notify
* Records are processed in [tasks](alert/tasks.py)