# ScottBot API

This API is a Cloudflare Worker with OpenAPI 3.1 using [chanfana](https://github.com/cloudflare/chanfana) and [Hono](https://github.com/honojs/hono).

This is built on an example project made to be used as a quick start into building OpenAPI compliant Workers that generates the
`openapi.json` schema automatically from code and validates the incoming request to the defined parameters or request body.

## API Documentation

### Start Order

Method: `POST`

Route: `'/'`

Body format:
```
{
  "status": <"test", "moving_to_pickup", "waiting_for_pickup", "moving_to_dropoff", "waiting_for_dropoff" or "delivered">
}
```

Returns: Json with order id as a string

should be invoked when starting an order, body will eventually contain pickup and dropoff location when we determine format the robot needs for that information

### Get Status

Method: `GET`

Route: `'/:id/status'`

Returns: Json with status as a string

should be invoked when checking an order's status from the frontend

### Update Status

Method: `POST`

Route: `'/:id/update'`

Body format:
```
{
  "status": <"test", "moving_to_pickup", "waiting_for_pickup", "moving_to_dropoff", "waiting_for_dropoff" or "delivered">
}
```

Returns: nothing

should be invoked when updating an order's status

### Complete Order

Method: `DELETE`

Route: `'/:id'`

Returns: nothing

should be invoked when an order is complete and can be deleted




## Get started

1. Sign up for [Cloudflare Workers](https://workers.dev). The free tier is more than enough for most use cases.
2. Clone this project and install dependencies with `npm install`
3. Run `wrangler login` to login to your Cloudflare account in wrangler
4. Run `wrangler deploy` to publish the API to Cloudflare Workers

## Project structure

1. Your main router is defined in `src/index.ts`.
2. Each endpoint has its own file in `src/endpoints/`.
3. For more information read the [chanfana documentation](https://chanfana.pages.dev/) and [Hono documentation](https://hono.dev/docs).

## Development

1. Run `wrangler dev` to start a local instance of the API.
2. Open `http://localhost:8787/` in your browser to see the Swagger interface where you can try the endpoints.
3. Changes made in the `src/` folder will automatically trigger the server to reload, you only need to refresh the Swagger interface.
