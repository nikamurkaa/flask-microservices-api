# Architecture

This project contains two independent Flask services.

## user-service

Responsibilities:

- create users;
- validate user input;
- return user data by ID;
- expose a health check.

The service stores data in memory because the goal of the project is to demonstrate service boundaries, HTTP communication and testing strategy rather than database modeling.

## order-service

Responsibilities:

- create orders;
- validate order input;
- call `user-service` to check that `user_id` exists;
- enrich created orders with `user_name` and `user_email`;
- handle dependency failures gracefully.

## Service-to-service flow

```text
1. Client sends POST /orders to order-service.
2. order-service validates request body.
3. order-service sends GET /users/{user_id} to user-service.
4. user-service returns user data or 404.
5. order-service creates an order only if the user exists.
6. order-service returns created order with user fields.
```

## Failure handling

| Scenario | Response from order-service |
| --- | --- |
| Invalid order payload | `400 Bad Request` |
| User does not exist | `400 Bad Request` |
| user-service unavailable | `503 Service Unavailable` |
| user-service invalid response | `502 Bad Gateway` |

## Why this is useful

The project demonstrates practical backend skills:

- REST API design;
- input validation;
- JSON error responses;
- service-to-service HTTP integration;
- dependency failure handling;
- Docker Compose setup;
- unit/integration-style tests;
- Postman and OpenAPI documentation.
