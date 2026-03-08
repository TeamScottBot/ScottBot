import asyncio
import json
import websockets
import sys
from datetime import datetime


class OrderListener:
    def __init__(self, websocket_uri: str):
        self.websocket_uri = websocket_uri
        self.is_connected = False
        self.message_count = 0

    async def connect_and_listen(self):
        print(f"[{self._get_timestamp()}] Connecting to WebSocket: {self.websocket_uri}")

        try:
            async with websockets.connect(self.websocket_uri, ping_interval=20, close_timeout=10) as websocket:
                self.is_connected = True
                print(f"[{self._get_timestamp()}] Connected to order server")
                print(f"[{self._get_timestamp()}] Waiting for updates (send requests to the API)...\n")

                async for message in websocket:
                    self.message_count += 1
                    await self._handle_order_message(message)

        except websockets.exceptions.ConnectionClosed:
            if self.message_count == 0:
                print(f"[{self._get_timestamp()}] Connection closed - no messages received")
            else:
                print(f"[{self._get_timestamp()}] Connection closed by server after {self.message_count} messages")
        except ConnectionRefusedError:
            print(f"[{self._get_timestamp()}] Failed to connect: Connection refused")
            print(f"[{self._get_timestamp()}] Check if the API is running and the WebSocket URI is correct")
        except Exception as e:
            print(f"[{self._get_timestamp()}] Error: {type(e).__name__}: {e}")
        finally:
            self.is_connected = False

    async def _handle_order_message(self, message: str):
        try:
            data = json.loads(message)
            await self._process_order(data)
        except json.JSONDecodeError:
            print(f"[{self._get_timestamp()}] Invalid JSON received: {message}")
        except Exception as e:
            print(f"[{self._get_timestamp()}] Error processing message: {e}")

    async def _process_order(self, order: dict):
        if order.get("type") == "connected":
            print(f"\n[{self._get_timestamp()}] Message #{self.message_count} (server ready)")
            print(f"  {order.get('message', 'Connected')}\n")
            return

        if order.get("type") == "emergency_stop":
            print(f"\n[{self._get_timestamp()}] Message #{self.message_count} (EMERGENCY STOP)")
            print("  Robot should stop immediately.\n")
            await self._handle_emergency_stop()
            return

        order_id = order.get("orderId", "unknown")
        pickup = order.get("pickupLocation", "unknown")
        dropoff = order.get("dropoffLocation", "unknown")
        status = order.get("status", "unknown")

        print(f"\n[{self._get_timestamp()}] Message #{self.message_count}")
        print(f"  Order ID: {order_id}")
        print(f"  Status: {status}")
        print(f"  Pickup Location: {pickup}")
        print(f"  Dropoff Location: {dropoff}\n")

        await self._simulate_robot_action(order_id, pickup, dropoff)

    # Simulate robot actions for delivery. Replace this with actual robot control logic.
    async def _simulate_robot_action(self, order_id: str, pickup: str, dropoff: str):

        print(f"Robot received order {order_id}")
        print(f"Preparing to navigate to pickup: {pickup}")

    # Replace with actual robot stop logic (e.g. publish to ROS / stop motors).
    async def _handle_emergency_stop(self):
        print("Emergency stop received - robot should stop immediately.")

    @staticmethod
    def _get_timestamp() -> str:
        return datetime.now().strftime("%H:%M:%S")


async def main():
    if len(sys.argv) > 1:
        websocket_uri = sys.argv[1]
    else:
        websocket_uri = "wss://api.qhgill2.workers.dev/orders/default/ws"

    print("=" * 60)
    print("ScottBot - WebSocket Listener")
    print("=" * 60)
    print(f"WebSocket URI: {websocket_uri}")
    print(f"\nRun this script first, then send API requests to:")
    print(f"  POST /orders/default/start")
    print(f"  POST /orders/default/update")
    print(f"  POST /orders/default/emergency-stop")
    print(f"=" * 60 + "\n")

    listener = OrderListener(websocket_uri)
    await listener.connect_and_listen()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n[Interrupted] Shutting down")
        sys.exit(0)
