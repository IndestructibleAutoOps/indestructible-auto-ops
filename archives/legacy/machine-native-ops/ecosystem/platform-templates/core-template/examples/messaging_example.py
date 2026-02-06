#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: platform-templates
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
Messaging Example
=================
示例：如何使用消息系統進行服務間通信
"""

import sys
import time
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from platform_manager import PlatformManager


def main():
    """消息系統示例"""
    print("\n=== Messaging Example ===\n")
    
    # 1. 創建平台管理器
    pm = PlatformManager('configs/platform-config.yaml')
    print(f"✓ Platform Manager initialized: {pm.platform_name}\n")
    
    # 2. 訂閱事件
    print("Setting up event subscribers...\n")
    
    received_events = []
    
    def event_handler(message):
        """事件處理器"""
        received_events.append(message)
        print(f"  📨 Event received: {message.event_type}")
        print(f"     Payload: {message.payload}")
    
    if pm.message_bus:
        # 訂閱平台事件
        sub_id = pm.subscribe_events('platform.events', event_handler)
        print(f"✓ Subscribed to platform.events: {sub_id}\n")
        
        time.sleep(0.1)  # 等待訂閱生效
        
        # 3. 發布事件
        print("Publishing events...\n")
        
        events = [
            {
                'topic': 'platform.events',
                'event_type': 'service.started',
                'payload': {
                    'service': 'compute-service',
                    'timestamp': time.time()
                }
            },
            {
                'topic': 'platform.events',
                'event_type': 'service.health_check',
                'payload': {
                    'service': 'storage-service',
                    'status': 'healthy'
                }
            },
            {
                'topic': 'platform.events',
                'event_type': 'data.synced',
                'payload': {
                    'dataset': 'config',
                    'items': 100
                }
            }
        ]
        
        for event in events:
            msg_id = pm.publish_event(**event)
            print(f"✓ Event published: {event['event_type']} (id: {msg_id})")
        
        # 等待事件處理
        time.sleep(0.5)
        
        # 4. 驗證結果
        print(f"\nEvents received: {len(received_events)}")
        
        # 5. 查看統計
        print("\nMessage Bus statistics:\n")
        stats = pm.message_bus.get_stats()
        print(f"  Published: {stats['published']}")
        print(f"  Delivered: {stats['delivered']}")
        print(f"  Topics: {stats['topics']}")
        print(f"  Subscriptions: {stats['subscriptions']}")
    else:
        print("Message Bus not available")
    
    print("\n✅ Example completed successfully!\n")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
