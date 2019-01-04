import asyncio


from cbpi_eventbus.eventbus import CBPiEventBus, on_event

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
