import os
import uuid
from paho.mqtt import client
from .message import Message
from .response import read_wifi_networks
from .timed import timed
from .topic import Topic

QOS_EXACTLY_ONCE = 2


class EeRouterClient(client.Client):
    ACTION_WIFI_ON = 1
    ACTION_WIFI_OFF = 0

    def __init__(self, admin_password: str, topic, action=ACTION_WIFI_OFF, logger=None):
        if action not in [EeRouterClient.ACTION_WIFI_OFF, EeRouterClient.ACTION_WIFI_ON]:
            raise Exception("unknown action: %d" % action)
        client_id = 'gui-' + str(uuid.uuid4())
        super().__init__(client.CallbackAPIVersion.VERSION2, transport='websockets', client_id=client_id)
        self.topic = topic
        self.action = action
        self.ws_set_options(path="/ws")
        self.username_pw_set('admin', admin_password)
        self.subscription_sent = {}
        self.networks = None
        self.logger = logger

    def on_connect(self, client, obj, flags, rc, props):
        # self.logger.debug("rc: "+str(rc))
        pass

    def on_message(self, client, obj, msg):
        # with open("msgs/" + msg.topic[msg.topic.rfind("/"):] + ".txt", "wb") as f:
        #     f.write(("QOS: %d, TOPIC: %s\n\n" % (msg.qos, msg.topic)).encode())
        #     f.write(msg.payload)

        if msg.topic == self.topic.get_subscribe_query():
            # self.logger.debug(dir(msg.payload))
            self.process_wifi_query_response(msg.payload)
        elif msg.topic == self.topic.get_subscribe_off():
            # self.logger.debug("WIFI OFF: " + msg.topic)
            self.disconnect()
        elif msg.topic == self.topic.get_subscribe_on():
            # self.logger.debug("WIFI ON: " + msg.topic)
            self.disconnect()
        else:
            if self.logger:
                self.logger.error("unknown topic: " + msg.topic)
            self.disconnect()

    def on_publish(self, client, obj, message_id, reason_code, properties):
        # self.logger.debug("mid: "+str(message_id))
        pass

    def on_subscribe(self, client, obj, message_id, reason_code_list, props):
        if message_id in self.subscription_sent:
            topic = self.subscription_sent[message_id]
            if topic == self.topic.get_subscribe_query():
                self.publish(self.topic.get_publish_query(),
                             Message.WIFI_QUERY, qos=QOS_EXACTLY_ONCE)
            elif topic == self.topic.get_subscribe_off():
                self.publish(self.topic.get_publish_off(), Message.get_wifi_off(
                    self.networks["guest_2G"]["ref"], self.networks["guest_2G"]["ref"]), qos=QOS_EXACTLY_ONCE)
            elif topic == self.topic.get_subscribe_on():
                self.publish(self.topic.get_publish_on(), Message.get_wifi_on(
                    self.networks["guest_2G"]["ref"], self.networks["guest_2G"]["ref"]), qos=QOS_EXACTLY_ONCE)

    def on_log(self, client, obj, level, log_str):
        # self.logger.debug(log_str)
        pass

    def process_wifi_query_response(self, response: bytes):
        if self.networks is None:
            ms, self.networks = read_wifi_networks(response)
            if self.logger:
                self.logger.debug("read_wifi_networks: %d ms" % ms)
        if "guest_2G" in self.networks and "guest_5G" in self.networks:
            if self.action == EeRouterClient.ACTION_WIFI_OFF:
                message_id = self.subscribe(self.topic.get_subscribe_off())[1]
                self.subscription_sent[message_id] = self.topic.get_subscribe_off(
                )
            elif self.action == EeRouterClient.ACTION_WIFI_ON:
                message_id = self.subscribe(self.topic.get_subscribe_on())[1]
                self.subscription_sent[message_id] = self.topic.get_subscribe_on(
                )
        else:
            if self.logger:
                self.logger.error("guest WiFi names not found")
            self.disconnect()

    @staticmethod
    @timed
    def process_wifi_action(action: int):
        if not ("EE_ROUTER_ADV_PASSWORD" in os.environ and "EE_ROUTER_IP" in os.environ):
            raise Exception("required enviroment variables not set")
        topic = Topic()
        ee_router = EeRouterClient(os.environ["EE_ROUTER_ADV_PASSWORD"], topic, action)
        ee_router.connect(os.environ["EE_ROUTER_IP"], os.getenv("EE_ROUTER_PORT", 80), 10)
        message_id = ee_router.subscribe(topic.get_subscribe_query())[1]
        ee_router.subscription_sent[message_id] = topic.get_subscribe_query()
        ee_router.loop_forever()
