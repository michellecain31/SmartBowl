import paho.mqtt.client as mqtt

broker = "mqtt.eclipseprojects.io"
port = 1883
topic_feed = "pet/feeder/feed"
topic_empty = "pet/feeder/empty"
topic_status = "pet/feeder/status"
topic_alert = "pet/feeder/alert"

client = mqtt.Client("FeederRelay")
client.connect(broker, port, 60)

bowl_level = 0  # שמירת מצב נוכחי

def on_message(client, userdata, msg):
    global bowl_level

    if msg.topic == topic_feed:
        try:
            new_level = int(msg.payload.decode())
        except ValueError:
            print("[!] Invalid feed amount")
            return

        # מגבלת מקסימום
        if new_level > 100:
            new_level = 100

        bowl_level = new_level  # 👈 כאן מחליפים את הערך, לא מוסיפים!

        client.publish(topic_status, bowl_level)
        print(f"[📥] Bowl level set to: {bowl_level}%")

    elif msg.topic == topic_empty:
        bowl_level = 0
        client.publish(topic_status, bowl_level)
        print("[🧹] Bowl emptied")

client.on_message = on_message
client.subscribe(topic_feed)
client.subscribe(topic_empty)

print("[✓] FeederRelay is running...")
client.loop_forever()
