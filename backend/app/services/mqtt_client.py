import paho.mqtt.client as mqtt
from flask import current_app
import json
import threading

class MQTTClient:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init_client()
        return cls._instance

    def _init_client(self):
        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

        # 从Flask配置加载MQTT参数
        self.client.username_pw_set(
            current_app.config.get('MQTT_USERNAME', ''),
            current_app.config.get('MQTT_PASSWORD', '')
        )

        self.client.connect(
            current_app.config.get('MQTT_BROKER', 'localhost'),
            current_app.config.get('MQTT_PORT', 1883),
            current_app.config.get('MQTT_KEEPALIVE', 60)
        )

        # 启动MQTT循环线程
        self.client.loop_start()

    def _on_connect(self, client, userdata, flags, rc):
        current_app.logger.info(f"MQTT Connected with result code {rc}")

    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            topic = msg.topic
            current_app.logger.info(f"MQTT Message received on {topic}: {payload}")

            # 这里可以添加消息处理逻辑
            # 例如触发事件或调用其他服务

        except Exception as e:
            current_app.logger.error(f"MQTT message processing error: {e}")

    def publish(self, topic, payload, qos=0, retain=False):
        """发布MQTT消息"""
        try:
            if not isinstance(payload, str):
                payload = json.dumps(payload)
            self.client.publish(topic, payload, qos=qos, retain=retain)
        except Exception as e:
            current_app.logger.error(f"MQTT publish error: {e}")

    def subscribe(self, topic, qos=0):
        """订阅MQTT主题"""
        self.client.subscribe(topic, qos=qos)

    def disconnect(self):
        """断开MQTT连接"""
        self.client.loop_stop()
        self.client.disconnect()

# 全局MQTT客户端实例
mqtt_client = MQTTClient()
