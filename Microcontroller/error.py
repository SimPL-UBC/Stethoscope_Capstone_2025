import asyncio

class ErrorChecker:
    def __init__(self, led, interval=1):
        self.led = led
        self.interval = interval
        self.checks = []  # List of dicts with name, func, color, active
        self._monitor_task = None

    def add_check(self, name, check_coroutine, color):
        self.checks.append({
            "name": name,
            "func": check_coroutine,
            "color": color,
            "active": False
        })

    async def _blink(self, color):
        try:
            while True:
                self.led.fill(color)
                await asyncio.sleep(self.interval)
                self.led.fill((0, 0, 0))
                await asyncio.sleep(self.interval)
        except asyncio.CancelledError:
            self.led.fill((0, 0, 0))
            raise

    async def run(self):
        current_blink_task = None
        active_color = None

        while True:
            # Update check states
            for check in self.checks:
                check["active"] = await check["func"]()

            # Filter active errors
            active_errors = [c for c in self.checks if c["active"]]
            new_color = active_errors[0]["color"] if active_errors else None

            # Change blink color if needed
            if new_color != active_color:
                if current_blink_task:
                    current_blink_task.cancel()
                    try:
                        await current_blink_task
                    except asyncio.CancelledError:
                        pass

                active_color = new_color
                if new_color:
                    current_blink_task = asyncio.create_task(self._blink(new_color))
                else:
                    current_blink_task = None

            # If all errors cleared, exit
            if not active_errors:
                break

            await asyncio.sleep(0.1)

        # Clean up and exit
        if current_blink_task:
            current_blink_task.cancel()
            try:
                await current_blink_task
            except asyncio.CancelledError:
                pass
        self.led.fill((0, 0, 0))  # Ensure LED is off