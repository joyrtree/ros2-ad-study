import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class Listener(Node):

    def __init__(self):
        # 노드 이름을 listener로 설정한다.
        super().__init__('listener')

        # /topic의 Int32 메시지를 구독하는 Subscriber를 생성한다.
        self.subscription = self.create_subscription(
            Int32,
            '/topic',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        # /topic에서 메시지를 받을 때마다 실행된다.
        self.get_logger().info(
            f'Subscribed: {msg.data}'
        )


def main(args=None):
    rclpy.init(args=args)

    node = Listener()

    try:
        # 메시지를 계속 기다리도록 노드를 실행한다.
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
