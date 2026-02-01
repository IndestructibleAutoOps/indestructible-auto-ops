#!/usr/bin/env python3
"""
Communication System Tests
==========================
測試通信系統的核心功能
"""

import sys
import time
from pathlib import Path
from threading import Event

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from message_bus import MessageBus, Message
from event_dispatcher import EventDispatcher


def test_message_bus():
    """測試消息總線"""
    print("\n=== Test Message Bus ===")
    
    config = {
        'message_bus': {
            'max_queue_size': 100
        },
        'monitoring': {
            'logging': {
                'level': 'WARNING'
            }
        }
    }
    
    bus = MessageBus(config)
    bus.start()
    
    # 測試發布消息
    message_id = bus.publish(
        topic="test.topic",
        event_type="test.event",
        payload={"key": "value"},
        source="test"
    )
    
    assert message_id != "", "Message publishing failed"
    print(f"✓ Message published: {message_id}")
    
    # 測試訂閱
    received_messages = []
    
    def handler(message: Message):
        received_messages.append(message)
    
    sub_id = bus.subscribe("test.topic", handler)
    assert sub_id != "", "Subscription failed"
    print(f"✓ Subscribed: {sub_id}")
    
    time.sleep(0.5)  # 等待之前的消息處理完
    received_messages.clear()  # 清空之前的消息
    
    # 發布並等待接收
    bus.publish("test.topic", "test.event", {"data": "test"}, "test")
    time.sleep(0.5)  # 等待消息處理
    
    assert len(received_messages) == 1, f"Expected 1 message, got {len(received_messages)}"
    assert received_messages[0].event_type == "test.event", "Event type mismatch"
    print("✓ Message received by subscriber")
    
    # 測試過濾器
    filtered_messages = []
    
    def filter_func(message: Message) -> bool:
        return message.payload.get("important") == True
    
    def filtered_handler(message: Message):
        filtered_messages.append(message)
    
    bus.subscribe("test.topic", filtered_handler, filter_func)
    
    # 發布兩條消息，只有一條應該被過濾器通過
    bus.publish("test.topic", "filtered", {"important": True})
    bus.publish("test.topic", "filtered", {"important": False})
    time.sleep(0.5)
    
    assert len(filtered_messages) == 1, f"Filter failed, got {len(filtered_messages)} messages"
    print("✓ Message filtering works")
    
    # 測試取消訂閱
    assert bus.unsubscribe(sub_id), "Unsubscribe failed"
    print("✓ Unsubscribed")
    
    # 測試統計
    stats = bus.get_stats()
    assert stats['published'] >= 3, "Published count incorrect"
    assert stats['topics'] >= 1, "Topics count incorrect"
    print(f"✓ Stats: {stats}")
    
    # 清理
    bus.stop()
    
    print("✅ Message Bus tests passed")


def test_event_dispatcher():
    """測試事件分發器"""
    print("\n=== Test Event Dispatcher ===")
    
    config = {
        'monitoring': {
            'logging': {
                'level': 'ERROR'
            }
        }
    }
    
    bus = MessageBus(config)
    bus.start()
    
    dispatcher = EventDispatcher(bus, config)
    
    # 測試註冊處理器
    handled_events = []
    
    def handler(message: Message):
        handled_events.append(message)
    
    handler_id = dispatcher.register_handler("user.created", handler, priority=10)
    assert handler_id != "", "Handler registration failed"
    print(f"✓ Handler registered: {handler_id}")
    
    # 訂閱事件
    dispatcher.subscribe_to_events("user.events", ["user.created"])
    time.sleep(0.1)  # 等待訂閱生效
    
    # 分發事件
    event_id = dispatcher.dispatch_event(
        topic="user.events",
        event_type="user.created",
        payload={"user_id": "123", "username": "testuser"},
        source="user-service"
    )
    
    time.sleep(0.5)  # 等待事件處理
    
    assert len(handled_events) == 1, f"Expected 1 event, got {len(handled_events)}"
    assert handled_events[0].payload["user_id"] == "123", "Payload mismatch"
    print("✓ Event dispatched and handled")
    
    # 測試優先級
    execution_order = []
    
    def high_priority_handler(message: Message):
        execution_order.append("high")
    
    def low_priority_handler(message: Message):
        execution_order.append("low")
    
    dispatcher.register_handler("priority.test", high_priority_handler, priority=100)
    dispatcher.register_handler("priority.test", low_priority_handler, priority=1)
    dispatcher.subscribe_to_events("priority.topic", ["priority.test"])
    time.sleep(0.1)
    
    dispatcher.dispatch_event(
        "priority.topic",
        "priority.test",
        {}
    )
    time.sleep(0.5)
    
    assert execution_order == ["high", "low"], f"Priority order incorrect: {execution_order}"
    print("✓ Priority handling works")
    
    # 測試統計
    stats = dispatcher.get_stats()
    assert stats['events_processed'] >= 2, "Events processed count incorrect"
    print(f"✓ Stats: {stats}")
    
    # 清理
    bus.stop()
    
    print("✅ Event Dispatcher tests passed")


def test_integration():
    """集成測試"""
    print("\n=== Integration Test ===")
    
    config = {
        'monitoring': {
            'logging': {
                'level': 'ERROR'
            }
        }
    }
    
    # 創建系統
    bus = MessageBus(config)
    bus.start()
    dispatcher = EventDispatcher(bus, config)
    
    # 模擬多個服務通信
    service_a_messages = []
    service_b_messages = []
    
    def service_a_handler(message: Message):
        service_a_messages.append(message)
        # Service A 響應
        if message.event_type == "request.data":
            dispatcher.dispatch_event(
                "responses",
                "response.data",
                {"data": "response from A"},
                "service-a"
            )
    
    def service_b_handler(message: Message):
        service_b_messages.append(message)
    
    # 註冊處理器
    dispatcher.register_handler("request.data", service_a_handler)
    dispatcher.register_handler("response.data", service_b_handler)
    
    # 訂閱主題
    dispatcher.subscribe_to_events("requests", ["request.data"])
    dispatcher.subscribe_to_events("responses", ["response.data"])
    time.sleep(0.1)
    
    # Service B 發送請求
    dispatcher.dispatch_event(
        "requests",
        "request.data",
        {"query": "get_data"},
        "service-b"
    )
    
    time.sleep(0.5)  # 等待消息傳遞
    
    # 驗證
    assert len(service_a_messages) == 1, "Service A should receive 1 message"
    assert service_a_messages[0].event_type == "request.data", "Wrong event type for Service A"
    
    assert len(service_b_messages) == 1, "Service B should receive 1 response"
    assert service_b_messages[0].event_type == "response.data", "Wrong event type for Service B"
    assert service_b_messages[0].payload["data"] == "response from A", "Wrong response data"
    
    print("✓ Service-to-service communication works")
    
    # 測試廣播
    broadcast_receivers = []
    
    def broadcast_handler(message: Message):
        broadcast_receivers.append(message.source)
    
    # 多個訂閱者
    bus.subscribe("broadcast", broadcast_handler)
    bus.subscribe("broadcast", broadcast_handler)
    bus.subscribe("broadcast", broadcast_handler)
    
    bus.publish("broadcast", "announcement", {"msg": "test"}, "broadcaster")
    time.sleep(0.5)
    
    assert len(broadcast_receivers) == 3, f"Expected 3 receivers, got {len(broadcast_receivers)}"
    print(f"✓ Broadcast to {len(broadcast_receivers)} subscribers works")
    
    # 獲取整體統計
    bus_stats = bus.get_stats()
    dispatcher_stats = dispatcher.get_stats()
    
    print(f"✓ Final stats:")
    print(f"  - Bus: {bus_stats}")
    print(f"  - Dispatcher: {dispatcher_stats}")
    
    # 清理
    bus.stop()
    
    print("✅ Integration test passed")


def main():
    """運行所有測試"""
    print("\n" + "="*60)
    print("Communication System - Test Suite")
    print("="*60)
    
    try:
        test_message_bus()
        test_event_dispatcher()
        test_integration()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED")
        print("="*60 + "\n")
        
        return 0
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
