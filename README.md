# CraftBeerPi Event Bus (BETA)

This is an asyncio based event bus for Python 3.7. The bus is heart of [CraftBeerPI](http://www.craftbeerpi.com "CraftBeerPI") brewing controller.

# Highlight

* Topic based event subscription supporting wildcards (inspired by MQTT topic pattern)
* Subscription via decorator or register method
* Subscribe to listen once for an event

## Installation

`pip install -i https://test.pypi.org/simple/ cbpi-eventbus`

## Example
```python
import asyncio
from cbpi_eventbus.eventbus import CBPiEventBus, on_event

# Creact bus
bus = CBPiEventBus(asyncio.get_event_loop())

class Sample(object):

    @on_event("sensor/+/on")
    async def test(self, topic, param1, **kwargs):
        """
        This method listen on all sensor on topics. i.e: sensor/1/on sensor/2/on
        :param topic: the current event topic
        :param kwargs: just accept all other args
        :return: None
        """
        await asyncio.sleep(1)
        print("Sensor On", param1)

    @on_event("sensor/#")
    async def test2(self, topic, **kwargs):
        """
        This method listen on all sensor topics. i.e: sensor/1/on sensor/2/off sensor/somethingelse
        :param topic: the current event topic
        :param kwargs: just accept all other args
        :return: None
        """
        print("All Sensor Events")

    @on_event("sensor/+/off")
    async def test3(self, topic, **kwargs):
        """
        This method listen on all sensor on topics. i.e: sensor/1/off sensor/2/off
        :param topic: the current event topic
        :param kwargs: just accept all other args
        :return: None
        """
        await asyncio.sleep(3)
        print("Sensor Off")


async def some_method(topic, **kwargs):
    print("HELLO EVENT", topic)


async def listen_for_every_thing(topic, **kwargs):
    print("####### Log", topic)


async def main():
    t = Sample()
    # Register all method decorated with @on_event
    bus.register_object(t)

    # register a single method an listen only once for an event
    bus.register("sensor/+/on", some_method, once=True)
    bus.register("#", listen_for_every_thing)
    # lets fire some events
    await bus.fire("sensor/1/on", param1="Hello")
    await bus.fire("sensor/1/off", param1="Hello")
    await bus.fire("sensor/1/on", param1="Hello")

    # Unregister method
    bus.unregister(listen_for_every_thing)

    await bus.fire("sensor/1/on", param1="Hello")
    # wait for all events to be finished
    await bus.close()

asyncio.run(main())

```

## Topic

The topic concept is inspired by MQTT topic patters.

Example: `sensor/1/on

The topic consists of one or more topic levels. Each topic level is separated by a forward slash (topic level separator).

### Wildcards

You can subscribe to an exact topic or use wild cards to listen for multiple events.

#### Single Level +

The + (plus) is used for single level

Example: `sensor/+/on`

Will match

* `sensor/1/on`
* `sensor/2/on`

Will NOT match

* `sensor/2/test/on`
* `sensor/abc/on`

#### Multi Level \#

The \# (hash) is used for multi level

Example: `home/sensor/#`

Will match

* `home/sensor/on`
* `home/sensor/1/on`
* `home/sensor/2/on/abc`


Will NOT match

* `home/1/sensor/on`
* `home/sensor/`
