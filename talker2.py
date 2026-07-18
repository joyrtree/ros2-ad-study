import random

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Talker2(Node):

    def __init__(self):
        # 노드 이름을 talker2로 설정한다.
        super().__init__('talker2')

        # String 메시지를 /topic2로 발행하는 Publisher를 생성한다.
        self.publisher_ = self.create_publisher(
            String,
            '/topic2',
            10
        )

        # 1초마다 timer_callback 함수를 실행한다.
        self.timer = self.create_timer(
            1.0,
            self.timer_callback
        )

    def timer_callback(self):
        # 0 이상 100 이하의 랜덤 정수를 생성한다.
        number = random.randint(0, 100)

        # String 메시지 객체를 생성한다.
        msg = String()

        # 랜덤 정수를 포함한 문자열을 만든다.
        msg.data = f'Now data is {number}'

        # 문자열 메시지를 /topic2로 발행한다.
        self.publisher_.publish(msg)

        # 발행한 문자열을 출력한다.
        self.get_logger().info(
            f"Published: '{msg.data}'"
        )


def main(args=None):
    rclpy.init(args=args)

    node = Talker2()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
