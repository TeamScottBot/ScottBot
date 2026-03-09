# ScottBot API

This API is a Cloudflare Worker with OpenAPI 3.1 using [chanfana](https://github.com/cloudflare/chanfana) and [Hono](https://github.com/honojs/hono).

This is built on an example project made to be used as a quick start into building OpenAPI compliant Workers that generates the
`openapi.json` schema automatically from code and validates the incoming request to the defined parameters or request body.

## API Documentation

All routes are under the `/orders` base path.

### Init Robot

Method: `POST`

Route: `'/orders/'`

Body: none

Returns: Json with `robotId` as a string (e.g. `"default"`)

should be invoked to initialize the robot's order state before use

### Start Order

Method: `POST`

Route: `'/orders/:id/start'`

Body format:
```
{
  "pickupLocation": <string>,
  "dropoffLocation": <string>
}
```

Returns: Json with `orderId` as a string (UUID). Returns 400 if the robot is not idle.

should be invoked when starting an order for the given robot id; the order begins in status `moving_to_pickup`

### WebSocket (order updates)

Method: `GET`

Route: `'/orders/:id/ws'`

Headers: `Upgrade: websocket` required

Returns: WebSocket connection; server sends real-time order updates (e.g. status changes, emergency stop) as JSON messages

should be used when the client (e.g. Pi or frontend) needs to receive live order state and events

### Get Status

Method: `GET`

Route: `'/orders/:id/status'`

Returns: When idle: Json with `status` as `"idle"`. When an order is active: Json with `id`, `pickupLocation`, `dropoffLocation`, and `status`. Returns 404 if order not found.

should be invoked when checking an order's status from the frontend

### Update Status

Method: `POST`

Route: `'/orders/:id/update'`

Body format:
```
{
  "status": <"idle", "moving_to_pickup", "waiting_for_pickup", "moving_to_dropoff", "waiting_for_dropoff" or "delivered">
}
```

Returns: Json with `id`, `pickupLocation`, `dropoffLocation`, and `status`. Returns 404 if order not found.

should be invoked when updating an order's status

### Emergency Stop

Method: `POST`

Route: `'/orders/:id/emergency-stop'`

Body: none

Returns: Json with `ok: true`. Returns 502 if order service unavailable.

should be invoked when triggering an emergency stop for the robot

### Complete Order

Method: `DELETE`

Route: `'/orders/:id'`

Returns: Json with `ok: true` and `orderId`. Returns 404 if order not found.

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
