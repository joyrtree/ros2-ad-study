ROS2 Advanced Summer Assignment #1
1. 과제 개요

본 과제에서는 ROS2 Humble 환경에서 Python 기반 패키지를 생성하고, Topic 통신 방식의 Publisher와 Subscriber를 구현하였다.

구현한 기능은 다음과 같다.

/topic으로 랜덤 정수 송신 및 구독
/topic2로 랜덤 정수가 포함된 문자열 송신 및 구독
하나의 agent 노드에서 두 Topic 동시 구독
launch 파일을 이용해 여러 노드 동시 실행

패키지 이름은 sub_pub_pkg, 작업공간 이름은 colcon_ws로 설정하였다.

1. 게념정리
   1. Workspace

Workspace는 ROS2 패키지를 저장하고 빌드하는 최상위 작업공간이다.

이번 과제에서는 다음 작업공간을 사용하였다.

~/colcon_ws

패키지는 Workspace 내부의 src 폴더에 생성하였다.

~/colcon_ws/src/sub_pub_pkg
2 Package

Package는 ROS2에서 관련 노드, 설정 파일, launch 파일 등을 하나로 묶어 관리하는 단위이다.

이번 과제에서는 ament_python 빌드 타입의 Python 패키지를 생성하였다.

sub_pub_pkg

3 Node

Node는 ROS2에서 독립적으로 실행되는 하나의 프로그램이다.

이번 과제에서는 다음 노드를 작성하였다.

talker
listener
talker2
listener2
agent

4 Topic

Topic은 Publisher와 Subscriber 사이에서 메시지를 전달하는 통신 채널이다.

이번 과제에서는 다음 두 Topic을 사용하였다.

/topic
/topic2
11.5 Publisher

Publisher는 특정 Topic으로 메시지를 보내는 역할을 한다.

talker.py  → /topic
talker2.py → /topic2
11.6 Subscriber

Subscriber는 특정 Topic에서 발행되는 메시지를 기다렸다가 수신한다.

listener.py  ← /topic
listener2.py ← /topic2
agent.py     ← /topic 및 /topic2
11.7 Message type

ROS2 통신에서는 Publisher와 Subscriber가 같은 메시지 타입을 사용해야 한다.

이번 과제에서 사용한 메시지 타입은 다음과 같다.

/topic  : std_msgs/msg/Int32
/topic2 : std_msgs/msg/String

Topic 이름이 같더라도 메시지 타입이 다르면 정상적으로 연결되지 않는다.

8 Callback 함수

Callback 함수는 Subscriber가 메시지를 수신했을 때 자동으로 실행되는 함수이다.

예를 들어 listener.py에서는 다음 함수가 콜백으로 등록되었다.

def listener_callback(self, msg):
    self.get_logger().info(
        f'Subscribed: {msg.data}'
    )

9 Timer

Timer는 지정한 시간 간격마다 특정 함수를 실행한다.

self.create_timer(
    1.0,
    self.timer_callback
)

위 코드는 1초마다 timer_callback()을 실행한다.

10 QoS Queue Depth

Publisher와 Subscriber 생성 시 마지막에 입력한 10은 Queue Depth이다.

self.create_publisher(
    Int32,
    '/topic',
    10
)

일시적으로 처리하지 못한 메시지를 최대 10개까지 보관하도록 설정한 것이다.

11 setup.py

Python 파일을 생성한 것만으로는 ros2 run으로 실행할 수 없다.

setup.py의 console_scripts에 노드를 등록하고 다시 빌드해야 한다.

11.12 colcon build

ROS2 패키지의 변경 내용을 실행 환경에 반영하기 위해 빌드를 수행한다.

cd ~/colcon_ws

colcon build \
    --symlink-install \
    --packages-select sub_pub_pkg
13 source

새 터미널에서는 ROS2와 작업공간 환경을 다시 불러와야 한다.

source /opt/ros/humble/setup.bash
source ~/colcon_ws/install/setup.bash

이를 수행하지 않으면 패키지나 실행 파일을 찾지 못할 수 있다.

14 Launch

Launch 파일은 여러 노드를 한 번에 실행하기 위한 파일이다.

이번 과제에서는 다음 세 노드를 동시에 실행하였다.

talker
talker2
agent

12. 발생한 오류 및 해결 과정
1 Package 'sub_pub_pkg' not found

원인

새 터미널에서 Workspace의 install/setup.bash를 source하지 않아 발생할 수 있다.

해결
source /opt/ros/humble/setup.bash
source ~/colcon_ws/install/setup.bash
12.2 No executable found

원인
setup.py의 console_scripts에 노드가 등록되지 않았거나, 등록 후 다시 빌드하지 않은 경우 발생한다.

해결

setup.py에 다음과 같이 노드를 등록하였다.

entry_points={
    'console_scripts': [
        'talker = sub_pub_pkg.talker:main',
        'listener = sub_pub_pkg.listener:main',
        'talker2 = sub_pub_pkg.talker2:main',
        'listener2 = sub_pub_pkg.listener2:main',
        'agent = sub_pub_pkg.agent:main',
    ],
},

그 후 다시 빌드하고 source하였다.

cd ~/colcon_ws

colcon build \
    --symlink-install \
    --packages-select sub_pub_pkg

source ~/colcon_ws/install/setup.bash


13. 최종 폴더 구조
sub_pub_pkg/
├── launch/
│   └── total.launch.py
│
├── resource/
│   └── sub_pub_pkg
│
├── sub_pub_pkg/
│   ├── __init__.py
│   ├── agent.py
│   ├── listener.py
│   ├── listener2.py
│   ├── talker.py
│   └── talker2.py
│
├── test/
├── package.xml
├── setup.cfg
└── setup.py
