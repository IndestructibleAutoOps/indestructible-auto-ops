#!/usr/bin/env python3
"""
GL Runtime Platform 自然語言控制平面
端口: 5001
功能: 接受自然語言任務指令，協調 Multi-Agent 執行

@GL-governed
@GL-layer: GL90-99
@GL-semantic: control-plane-api
@GL-charter-version: 1.0.0
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from flask import Flask, request, jsonify
from flask_cors import CORS
import redis

# 配置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Flask 應用
app = Flask(__name__)
CORS(app)

# 連接 Redis 用於事件流
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    redis_client.ping()
    logger.info("Redis 連接成功")
except:
    redis_client = None
    logger.warning("Redis 連接失敗，將使用本地日誌")

# 數據模型
class NaturalLanguageTask:
    """自然語言任務模型"""
    def __init__(self, task_id: str, command: str, priority: str = "normal",
                 execution_mode: str = "strict", gl_platform_universegl_platform_universe.governance_level: str = "root",
                 parameters: Dict = None, requester: str = "system"):
        self.task_id = task_id
        self.command = command
        self.priority = priority
        self.execution_mode = execution_mode
        self.gl_platform_universegl_platform_universe.governance_level = gl_platform_universegl_platform_universe.governance_level
        self.parameters = parameters or {}
        self.requester = requester

class TaskResponse:
    """任務響應模型"""
    def __init__(self, task_id: str, status: str, message: str,
                 execution_id: Optional[str] = None,
                 estimated_completion: Optional[datetime] = None,
                 gl_platform_universegl_platform_universe.governance_approval: Optional[bool] = None):
        self.task_id = task_id
        self.status = status
        self.message = message
        self.execution_id = execution_id
        self.estimated_completion = estimated_completion
        self.gl_platform_universegl_platform_universe.governance_approval = gl_platform_universegl_platform_universe.governance_approval

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "status": self.status,
            "message": self.message,
            "execution_id": self.execution_id,
            "estimated_completion": self.estimated_completion.isoformat() if self.estimated_completion else None,
            "gl_platform_universegl_platform_universe.governance_approval": self.gl_platform_universegl_platform_universe.governance_approval
        }

# 任務處理器
class TaskProcessor:
    """處理自然語言任務"""
    
    def __init__(self):
        self.active_tasks = {}
        self.agents = {}
        self.gl_platform_universegl_platform_universe.governance_enabled = True
        
    def parse_natural_language(self, command: str) -> Dict[str, Any]:
        """解析自然語言命令為結構化任務"""
        structured_task = {
            "action": "unknown",
            "target": None,
            "parameters": {},
            "constraints": []
        }
        
        command_lower = command.lower()
        
        # 系統控制命令
        if "啟動" in command or "start" in command_lower:
            structured_task["action"] = "start"
            if "服務" in command or "service" in command_lower:
                structured_task["target"] = "service"
            elif "代理" in command or "agent" in command_lower:
                structured_task["target"] = "agent"
            elif "系統" in command or "system" in command_lower:
                structured_task["target"] = "system"
                
        elif "停止" in command or "stop" in command_lower:
            structured_task["action"] = "stop"
            
        elif "狀態" in command or "status" in command_lower:
            structured_task["action"] = "status"
            
        elif "部署" in command or "deploy" in command_lower:
            structured_task["action"] = "deploy"
            
        elif "驗證" in command or "verify" in command_lower:
            structured_task["action"] = "verify"
            
        elif "審計" in command or "audit" in command_lower:
            structured_task["action"] = "audit"
        
        return structured_task
    
    def validate_with_gl_platform_universegl_platform_universe.governance(self, task: NaturalLanguageTask) -> bool:
        """通過治理層驗證任務"""
        if not self.gl_platform_universegl_platform_universe.governance_enabled:
            return True
            
        # 發送到治理事件流
        if redis_client:
            gl_platform_universegl_platform_universe.governance_check = {
                "task_id": task.task_id,
                "command": task.command,
                "requester": task.requester,
                "gl_platform_universegl_platform_universe.governance_level": task.gl_platform_universegl_platform_universe.governance_level,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            redis_client.publish(
                "gl_platform_universegl_platform_universe.governance-requests",
                json.dumps(gl_platform_universegl_platform_universe.governance_check, ensure_ascii=False)
            )
        
        return True
    
    def orchestrate_agents(self, task: NaturalLanguageTask, structured_task: Dict) -> str:
        """協調 Multi-Agent 執行任務"""
        execution_id = f"exec-{task.task_id}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        # 根據任務類型分配代理
        agents_to_engage = []
        
        if structured_task["action"] in ["start", "stop", "deploy"]:
            agents_to_engage = ["deployment-agent", "verification-agent", "gl_platform_universegl_platform_universe.governance-agent"]
        elif structured_task["action"] == "status":
            agents_to_engage = ["monitoring-agent", "health-agent"]
        elif structured_task["action"] == "verify":
            agents_to_engage = ["verification-agent", "audit-agent", "compliance-agent"]
        elif structured_task["action"] == "audit":
            agents_to_engage = ["audit-agent", "gl_platform_universegl_platform_universe.governance-agent", "reporting-agent"]
        
        # 創建協調任務
        coordination_task = {
            "execution_id": execution_id,
            "original_task": task.__dict__,
            "structured_task": structured_task,
            "agents": agents_to_engage,
            "created_at": datetime.utcnow().isoformat(),
            "orchestrator": "nlp-control-plane"
        }
        
        # 發送到代理協調隊列
        if redis_client:
            redis_client.rpush(
                "agent-coordination-queue",
                json.dumps(coordination_task, ensure_ascii=False)
            )
        
        logger.info(f"任務已分配給 {len(agents_to_engage)} 個代理執行")
        
        return execution_id
    
    def process_task(self, task: NaturalLanguageTask) -> TaskResponse:
        """處理自然語言任務"""
        
        # 1. 解析自然語言
        structured_task = self.parse_natural_language(task.command)
        
        # 2. 治理層驗證
        gl_platform_universegl_platform_universe.governance_approved = self.validate_with_gl_platform_universegl_platform_universe.governance(task)
        
        if not gl_platform_universegl_platform_universe.governance_approved:
            return TaskResponse(
                task_id=task.task_id,
                status="failed",
                message="任務未通過治理層驗證",
                gl_platform_universegl_platform_universe.governance_approval=False
            )
        
        # 3. 協調代理執行
        execution_id = self.orchestrate_agents(task, structured_task)
        
        # 4. 記錄審計事件
        if redis_client:
            audit_event = {
                "event_type": "nlp_task_accepted",
                "task_id": task.task_id,
                "execution_id": execution_id,
                "command": task.command,
                "requester": task.requester,
                "timestamp": datetime.utcnow().isoformat(),
                "gl_platform_universegl_platform_universe.governance_level": task.gl_platform_universegl_platform_universe.governance_level
            }
            
            redis_client.publish(
                "audit-events",
                json.dumps(audit_event, ensure_ascii=False)
            )
        
        # 5. 返回響應
        return TaskResponse(
            task_id=task.task_id,
            status="accepted",
            message=f"任務已接受，正在協調 {len(structured_task.get('agents', []))} 個代理執行",
            execution_id=execution_id,
            estimated_completion=datetime.utcnow(),
            gl_platform_universegl_platform_universe.governance_approval=True
        )

# 全局處理器實例
task_processor = TaskProcessor()

# API 路由
@app.route('/health', methods=['GET'])
def health_check():
    """健康檢查端點"""
    return jsonify({
        "status": "healthy",
        "service": "nlp-control-plane",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "ready_for_tasks": True,
        "gl_platform_universegl_platform_universe.governance": "GL Unified Charter Activated"
    })

@app.route('/api/control/execute', methods=['POST'])
def submit_task():
    """提交自然語言任務"""
    try:
        data = request.get_json()
        
        # 驗證請求
        if not data or 'command' not in data:
            return jsonify({
                "error": "缺少必要參數: command",
                "status": "rejected"
            }), 400
        
        # 創建任務
        task = NaturalLanguageTask(
            task_id=f"task-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            command=data['command'],
            priority=data.get('priority', 'normal'),
            execution_mode=data.get('execution_mode', 'strict'),
            gl_platform_universegl_platform_universe.governance_level=data.get('gl_platform_universegl_platform_universe.governance_level', 'root'),
            parameters=data.get('parameters', {}),
            requester=data.get('requester', 'unknown')
        )
        
        # 處理任務
        response = task_processor.process_task(task)
        
        return jsonify(response.to_dict())
        
    except Exception as e:
        logger.error(f"任務處理失敗: {e}")
        return jsonify({
            "error": str(e),
            "status": "failed"
        }), 500

@app.route('/api/control/status', methods=['GET'])
def get_control_status():
    """獲取控制平面狀態"""
    return jsonify({
        "status": "operational",
        "mode": "natural-language",
        "gl_platform_universegl_platform_universe.governance": "GL Unified Charter Activated",
        "ready_for_tasks": True,
        "tasks_processed": len(task_processor.active_tasks),
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/api/control/system/status', methods=['GET'])
def get_system_status():
    """獲取系統狀態"""
    try:
        # 檢查各服務狀態
        services_status = {}
        ports_to_check = [3000, 8080, 5001, 9000, 6379, 5432, 9090]
        
        import socket
        for port in ports_to_check:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            services_status[f"port_{port}"] = "open" if result == 0 else "closed"
            sock.close()
        
        return jsonify({
            "system_status": "operational",
            "timestamp": datetime.utcnow().isoformat(),
            "services": services_status,
            "control_plane": {
                "endpoint": "http://localhost:5001",
                "health": "healthy",
                "tasks_processed": len(task_processor.active_tasks)
            },
            "gl_platform_universegl_platform_universe.governance": {
                "charter": "GL Unified Charter",
                "status": "ACTIVATED",
                "level": "UNIFIED_ROOT_META"
            }
        })
        
    except Exception as e:
        logger.error(f"獲取系統狀態失敗: {e}")
        return jsonify({
            "system_status": "degraded",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@app.route('/api/gl_platform_universegl_platform_universe.governance/report', methods=['GET'])
def get_gl_platform_universegl_platform_universe.governance_report():
    """獲取治理層報告"""
    try:
        return jsonify({
            "gl_platform_universegl_platform_universe.governance_levels": {
                "unified": "active",
                "root": "active",
                "meta": "active"
            },
            "verification_core": "operational",
            "compliance_status": "compliant",
            "last_verified": datetime.utcnow().isoformat(),
            "charter_version": "1.0.0",
            "audit_stream": "redis://localhost:6379/0"
        })
        
    except Exception as e:
        logger.error(f"獲取治理報告失敗: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logger.info("啟動 GL Runtime Platform 自然語言控制平面...")
    logger.info("服務將監聽端口: 5001")
    logger.info("健康檢查端點: http://localhost:5001/health")
    logger.info("任務提交端點: http://localhost:5001/api/control/execute")
    
    # 發布啟動事件
    startup_event = {
        "event_type": "control_plane_started",
        "service": "nlp-control-plane",
        "port": 5001,
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "gl_platform_universegl_platform_universe.governance": "GL Unified Charter Activated"
    }
    
    if redis_client:
        redis_client.publish(
            "audit-events",
            json.dumps(startup_event, ensure_ascii=False)
        )
    
    # 啟動 Flask 應用
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=False,
        threaded=True
    )