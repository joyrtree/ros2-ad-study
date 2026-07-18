import random

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class Talker(Node):

    def __init__(self):
        # 부모 클래스인 Node를 초기화하고 노드 이름을 talker로 설정한다.
        super().__init__('talker')

        # Int32 메시지를 /topic으로 발행하는 Publisher를 생성한다.
        # 마지막 숫자 10은 QoS queue depth이다.
        self.publisher_ = self.create_publisher(
            Int32,
            '/topic',
            10
        )

        # 1초마다 timer_callback 함수를 실행하는 Timer를 생성한다.
        self.timer = self.create_timer(
            1.0,
            self.timer_callback
        )

    def timer_callback(self):
        # Int32 메시지 객체를 생성한다.
        msg = Int32()

        # 0 이상 100 이하의 랜덤 정수를 생성하여 data에 저장한다.
        msg.data = random.randint(0, 100)

        # 생성한 메시지를 /topic으로 발행한다.
        self.publisher_.publish(msg)

        # 터미널에 발행한 값을 출력한다.
        self.get_logger().info(
            f'Published: {msg.data}'
        )


def main(args=None):
    # ROS2 Python 통신 기능을 초기화한다.
    rclpy.init(args=args)

    # Talker 객체를 생성한다.
    node = Talker()

    try:
        # 노드가 종료되지 않고 계속 실행되도록 한다.
        rclpy.spin(node)

    except KeyboardInterrupt:
        # Ctrl+C가 입력되면 정상적으로 종료한다.
        pass

    finally:
        # 노드를 제거하고 ROS2 통신을 종료한다.
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
