# SPDX-FileCopyrightText: 2022 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import asyncio
import board
import digitalio
import pwmio


async def blink(pin, oninterval, offinterval):
    with digitalio.DigitalInOut(pin) as led:
        led.switch_to_output(value=False)
        while True:
            led.value = True
            await asyncio.sleep(oninterval)  # Don't forget the "await"!
            led.value = False
            await asyncio.sleep(offinterval)  # Don't forget the "await"!

async def fade(pin, interval):
    with pwmio.PWMOut(pin, frequency=5000, duty_cycle=0) as pwmled:
        while True:
            for i in range(100):
                # PWM LED up and down
                if i < 50:
                    pwmled.duty_cycle = int(i * 2 * 65535 / 100)  # Up
                else:
                    pwmled.duty_cycle = 65535 - int((i - 50) * 2 * 65535 / 100)  # Down
                await asyncio.sleep(interval)

async def main():
    led1_task = asyncio.create_task(blink(board.D12, 0.25))
    led2_task = asyncio.create_task(blink(board.A1, 0.5, 2))
    led3_task = asyncio.create_task(fade(board.A0, 0.025))

    await asyncio.gather(led1_task, led2_task, led3_task)  # Don't forget "await"!


asyncio.run(main())
