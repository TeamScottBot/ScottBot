import asyncio
import json
import websockets
import sys
from datetime import datetime


class OrderListener:
    def __init__(self, websocket_uri: str):
        """
        Initialize the order listener.

        Args:
            websocket_uri: The URI of the Durable Object WebSocket endpoint
                          (e.g., "ws://localhost:8787/orders/{order_id}/ws")
        """
        self.websocket_uri = websocket_uri
        self.is_connected = False

    async def connect_and_listen(self):
        """Connect to the WebSocket and listen for order updates."""
        print(f"[{self._get_timestamp()}] Connecting to WebSocket: {self.websocket_uri}")

        try:
            async with websockets.connect(self.websocket_uri) as websocket:
                self.is_connected = True
                print(f"[{self._get_timestamp()}] Connected to order server")

                async for message in websocket:
                    await self._handle_order_message(message)

        except websockets.exceptions.ConnectionClosed:
            print(f"[{self._get_timestamp()}] Connection closed by server")
        except ConnectionRefusedError:
            print(f"[{self._get_timestamp()}] Failed to connect: Connection refused")
        except Exception as e:
            print(f"[{self._get_timestamp()}] Error: {e}")
        finally:
            self.is_connected = False

    async def _handle_order_message(self, message: str):
        """
        Handle an incoming order message.

        Args:
            message: JSON string containing order data
        """
        try:
            data = json.loads(message)
            await self._process_order(data)
        except json.JSONDecodeError:
            print(f"[{self._get_timestamp()}] ✗ Invalid JSON received: {message}")
        except Exception as e:
            print(f"[{self._get_timestamp()}] ✗ Error processing message: {e}")

    async def _process_order(self, order: dict):
        """
        Process an order and extract delivery locations.

        Args:
            order: Dictionary containing orderId, pickupLocation, dropoffLocation, and status
        """
        order_id = order.get("orderId", "unknown")
        pickup = order.get("pickupLocation", "unknown")
        dropoff = order.get("dropoffLocation", "unknown")
        status = order.get("status", "unknown")

        print(f"\n[{self._get_timestamp()}] New Order Received")
        print(f"  Order ID: {order_id}")
        print(f"  Status: {status}")
        print(f"  Pickup Location: {pickup}")
        print(f"  Dropoff Location: {dropoff}")

        await self._simulate_robot_action(order_id, pickup, dropoff)

    async def _simulate_robot_action(self, order_id: str, pickup: str, dropoff: str):
        """
        Simulate robot actions for delivery.
        Replace this with actual robot control logic.

        Args:
            order_id: The order identifier
            pickup: Pickup location
            dropoff: Dropoff location
        """
        print(f"Robot received order {order_id}")
        print(f"Preparing to navigate to pickup: {pickup}")

    @staticmethod
    def _get_timestamp() -> str:
        """Get current timestamp for logging."""
        return datetime.now().strftime("%H:%M:%S")


async def main():
    """Main entry point for the WebSocket listener."""

    if len(sys.argv) > 1:
        websocket_uri = sys.argv[1]
    else:
        websocket_uri = "ws://localhost:8787/orders/default/ws"

    print("=" * 60)
    print("ScottBot - Raspberry Pi Order Listener")
    print("=" * 60)
    print(f"Server URI: {websocket_uri}")
    print("Waiting for orders...\n")

    listener = OrderListener(websocket_uri)
    retry_count = 0
    max_retries = 5
    base_wait_time = 2

    while True:
        try:
            await listener.connect_and_listen()
            retry_count = 0  
        except Exception as e:
            retry_count += 1
            if retry_count > max_retries:
                print(
                    f"[{listener._get_timestamp()}] Max retries exceeded. Exiting."
                )
                break

            wait_time = base_wait_time * (2 ** (retry_count - 1))
            print(
                f"[{listener._get_timestamp()}] Reconnecting in {wait_time}s (attempt {retry_count}/{max_retries})"
            )
            await asyncio.sleep(wait_time)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[Ctrl+C] Shutting down")
        sys.exit(0)