# ==============================================================================
# 團隊協作平台 - 高階開發者工具
# Team Collaboration Platform - Advanced Developer Tool
# ==============================================================================

import json
import logging
import os
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from typing import Any

import aiohttp
import redis
import yaml
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from github import Github


class MessageType(Enum):
    """消息類型"""

    CODE_REVIEW = "code_review"
    DEPLOYMENT_NOTIFICATION = "deployment_notification"
    ALERT = "alert"
    STATUS_UPDATE = "status_update"
    DISCUSSION = "discussion"
    MENTION = "mention"


class UserStatus(Enum):
    """用戶狀態"""

    ONLINE = "online"
    AWAY = "away"
    BUSY = "busy"
    OFFLINE = "offline"


class NotificationLevel(Enum):
    """通知級別"""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"


@dataclass
class User:
    """用戶信息"""

    id: str
    username: str
    email: str
    role: str
    avatar_url: str | None
    status: UserStatus
    last_seen: datetime
    specialties: list[str]


@dataclass
class Message:
    """消息"""

    id: str
    sender_id: str
    channel_id: str
    message_type: MessageType
    content: str
    timestamp: datetime
    metadata: dict[str, Any]
    mentions: list[str]
    reactions: dict[str, list[str]]


@dataclass
class Channel:
    """頻道"""

    id: str
    name: str
    description: str
    type: str  # 'general', 'deployment', 'code_review', 'alert'
    members: list[str]
    created_at: datetime
    last_activity: datetime


@dataclass
class Notification:
    """通知"""

    id: str
    user_id: str
    title: str
    message: str
    level: NotificationLevel
    timestamp: datetime
    read: bool
    action_url: str | None


class CollaborationHub:
    """協作中心核心類"""

    def __init__(self, config_path: str = "config/collaboration-config.yaml"):
        self.config = self._load_config(config_path)
        self.logger = self._setup_logger()
        self.redis_client = self._init_redis_client()
        self.github_client = self._init_github_client()
        self.users = {}
        self.channels = {}
        self.messages = {}
        self.notifications = {}
        self.connected_websockets = {}

        # 初始化 FastAPI 應用
        self.app = FastAPI(title="Team Collaboration Platform")
        self._setup_routes()
        self._setup_websocket_manager()

    def _load_config(self, config_path: str) -> dict[str, Any]:
        """載入配置文件"""
        try:
            with open(config_path, encoding="utf-8") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            # 默認配置
            return {
                "server": {"host": "127.0.0.1", "port": 8080, "debug": True},  # nosec B104
                "redis": {
                    "host": os.getenv("REDIS_HOST", "localhost"),
                    "port": int(os.getenv("REDIS_PORT", 6379)),
                    "db": int(os.getenv("REDIS_DB", 0)),
                },
                "github": {
                    "token": os.getenv("GITHUB_TOKEN"),
                    "repo": os.getenv(
                        "GITHUB_REPO", "MachineNativeOps/MachineNativeOps"
                    ),
                },
                "notifications": {
                    "email_enabled": False,
                    "slack_webhook": os.getenv("SLACK_WEBHOOK_URL"),
                    "teams_webhook": os.getenv("TEAMS_WEBHOOK_URL"),
                },
                "features": {
                    "real_time_collaboration": True,
                    "code_review_integration": True,
                    "deployment_notifications": True,
                    "alert_system": True,
                },
            }

    def _setup_logger(self) -> logging.Logger:
        """設置日誌記錄器"""
        logger = logging.getLogger("CollaborationHub")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _init_redis_client(self) -> redis.Redis:
        """初始化 Redis 客戶端"""
        try:
            redis_config = self.config["redis"]
            return redis.Redis(
                host=redis_config["host"],
                port=redis_config["port"],
                db=redis_config["db"],
                decode_responses=True,
            )
        except Exception as e:
            self.logger.warning(f"Redis 連接失敗: {e}")
            return None

    def _init_github_client(self) -> Github:
        """初始化 GitHub 客戶端"""
        token = self.config["github"]["token"]
        if token:
            return Github(token)
        return Github()

    def _setup_routes(self):
        """設置 API 路由"""

        @self.app.get("/", response_class=HTMLResponse)
        async def root():
            return """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Team Collaboration Platform</title>
                <script src="https://cdn.jsdelivr.net/npm/vue@3"></script>
                <script src="https://cdn.tailwindcss.com"></script>
            </head>
            <body>
                <div id="app">
                    <h1>🚀 Team Collaboration Platform</h1>
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <h2>頻道</h2>
                            <div v-for="channel in channels" :key="channel.id">
                                {{ channel.name }}
                            </div>
                        </div>
                        <div>
                            <h2>消息</h2>
                            <div v-for="message in messages" :key="message.id">
                                <strong>{{ message.sender }}:</strong> {{ message.content }}
                            </div>
                        </div>
                    </div>
                    <div>
                        <input v-model="newMessage" @keyup.enter="sendMessage"
                               placeholder="輸入消息..." class="border rounded p-2">
                        <button @click="sendMessage" class="bg-blue-500 text-white px-4 py-2 rounded">
                            發送
                        </button>
                    </div>
                </div>

                <script>
                    const { createApp } = Vue;

                    createApp({
                        data() {
                            return {
                                channels: [],
                                messages: [],
                                newMessage: '',
                                ws: null
                            }
                        },
                        mounted() {
                            this.connectWebSocket();
                        },
                        methods: {
                            connectWebSocket() {
                                this.ws = new WebSocket('ws://localhost:8080/ws');

                                this.ws.onmessage = (event) => {
                                    const data = JSON.parse(event.data);
                                    if (data.type === 'message') {
                                        this.messages.push(data.message);
                                    }
                                };
                            },
                            sendMessage() {
                                if (this.newMessage.trim() && this.ws) {
                                    this.ws.send(JSON.stringify({
                                        type: 'message',
                                        content: this.newMessage
                                    }));
                                    this.newMessage = '';
                                }
                            }
                        }
                    }).mount('#app');
                </script>
            </body>
            </html>
            """

        @self.app.post("/api/users")
        async def create_user(user_data: dict):
            """創建用戶"""
            user = User(
                id=user_data["id"],
                username=user_data["username"],
                email=user_data["email"],
                role=user_data["role"],
                avatar_url=user_data.get("avatar_url"),
                status=UserStatus.ONLINE,
                last_seen=datetime.now(),
                specialties=user_data.get("specialties", []),
            )

            self.users[user.id] = user
            await self._broadcast_user_status(user.id, UserStatus.ONLINE)

            return {"status": "success", "user_id": user.id}

        @self.app.get("/api/users/{user_id}")
        async def get_user(user_id: str):
            """獲取用戶信息"""
            user = self.users.get(user_id)
            if not user:
                return {"error": "User not found"}
            return asdict(user)

        @self.app.post("/api/channels")
        async def create_channel(channel_data: dict):
            """創建頻道"""
            channel = Channel(
                id=channel_data["id"],
                name=channel_data["name"],
                description=channel_data["description"],
                type=channel_data["type"],
                members=channel_data.get("members", []),
                created_at=datetime.now(),
                last_activity=datetime.now(),
            )

            self.channels[channel.id] = channel
            await self._broadcast_channel_update(channel)

            return {"status": "success", "channel_id": channel.id}

    def _setup_websocket_manager(self):
        """設置 WebSocket 管理器"""

        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            user_id = f"user_{int(time.time())}"
            self.connected_websockets[user_id] = websocket

            try:
                while True:
                    data = await websocket.receive_text()
                    message_data = json.loads(data)
                    await self._handle_websocket_message(user_id, message_data)
            except WebSocketDisconnect:
                del self.connected_websockets[user_id]
                await self._update_user_status(user_id, UserStatus.OFFLINE)

    async def _handle_websocket_message(self, user_id: str, data: dict):
        """處理 WebSocket 消息"""
        if data["type"] == "message":
            message = Message(
                id=f"msg_{int(time.time())}",
                sender_id=user_id,
                channel_id=data.get("channel_id", "general"),
                message_type=MessageType.DISCUSSION,
                content=data["content"],
                timestamp=datetime.now(),
                metadata={},
                mentions=[],
                reactions={},
            )
            await self._broadcast_message(message)

    async def _broadcast_message(self, message: Message):
        """廣播消息"""
        data = {"type": "message", "message": asdict(message)}
        await self._broadcast_to_all(data)

    async def _broadcast_user_status(self, user_id: str, status: UserStatus):
        """廣播用戶狀態"""
        data = {"type": "user_status", "user_id": user_id, "status": status.value}
        await self._broadcast_to_all(data)

    async def _broadcast_channel_update(self, channel: Channel):
        """廣播頻道更新"""
        channel_data = {"type": "channel_update", "channel": asdict(channel)}
        await self._broadcast_to_all(channel_data)

    async def _broadcast_typing_status(self, user_id: str, channel_id: str):
        """廣播輸入狀態"""
        typing_data = {"type": "typing", "user_id": user_id, "channel_id": channel_id}
        await self._broadcast_to_all(typing_data)

    async def _broadcast_to_all(self, data: dict):
        """向所有連接的用戶廣播消息"""
        for websocket in self.connected_websockets.values():
            try:
                await websocket.send_text(json.dumps(data, default=str))
            except Exception as e:
                self.logger.error(f"廣播消息失敗: {e}")

    async def _update_user_status(self, user_id: str, status: UserStatus):
        """更新用戶狀態"""
        if user_id in self.users:
            self.users[user_id].status = status
            self.users[user_id].last_seen = datetime.now()

            # 保存到 Redis（如果可用）
            if self.redis_client:
                self.redis_client.hset(
                    f"user:{user_id}",
                    mapping={
                        "status": status.value,
                        "last_seen": datetime.now().isoformat(),
                    },
                )

            await self._broadcast_user_status(user_id, status)

    async def _send_notification(self, notification: Notification):
        """發送通知"""
        # 發送給在線用戶
        websocket = self.connected_websockets.get(notification.user_id)
        if websocket:
            try:
                notification_data = {
                    "type": "notification",
                    "notification": asdict(notification),
                }
                await websocket.send_text(json.dumps(notification_data, default=str))
            except Exception as e:
                self.logger.error(f"發送通知失敗: {e}")

        # 發送外部通知
        await self._send_external_notification(notification)

    async def _send_external_notification(self, notification: Notification):
        """發送外部通知（Slack, Teams, Email）"""
        # Slack 通知
        slack_webhook = self.config["notifications"]["slack_webhook"]
        if slack_webhook:
            await self._send_slack_notification(notification, slack_webhook)

        # Teams 通知
        teams_webhook = self.config["notifications"]["teams_webhook"]
        if teams_webhook:
            await self._send_teams_notification(notification, teams_webhook)

    async def _send_slack_notification(
        self, notification: Notification, webhook_url: str
    ):
        """發送 Slack 通知"""
        async with aiohttp.ClientSession() as session:
            payload = {
                "text": f"*{notification.title}*",
                "attachments": [
                    {
                        "text": notification.message,
                        "color": self._get_slack_color(notification.level),
                    }
                ],
            }

            try:
                async with session.post(webhook_url, json=payload) as response:
                    if response.status != 200:
                        self.logger.error(f"Slack 通知發送失敗: {response.status}")
            except Exception as e:
                self.logger.error(f"Slack 通知發送異常: {e}")

    async def _send_teams_notification(
        self, notification: Notification, webhook_url: str
    ):
        """發送 Teams 通知"""
        async with aiohttp.ClientSession() as session:
            payload = {
                "@type": "MessageCard",
                "@context": "http://schema.org/extensions",
                "themeColor": self._get_teams_color(notification.level),
                "summary": notification.title,
                "sections": [
                    {
                        "activityTitle": notification.title,
                        "activitySubtitle": notification.message,
                        "markdown": True,
                    }
                ],
            }

            try:
                async with session.post(webhook_url, json=payload) as response:
                    if response.status != 200:
                        self.logger.error(f"Teams 通知發送失敗: {response.status}")
            except Exception as e:
                self.logger.error(f"Teams 通知發送異常: {e}")

    def _get_slack_color(self, level: NotificationLevel) -> str:
        """獲取 Slack 顏色"""
        colors = {
            NotificationLevel.INFO: "#36a64f",
            NotificationLevel.WARNING: "#ff9500",
            NotificationLevel.ERROR: "#ff0000",
            NotificationLevel.SUCCESS: "#36a64f",
        }
        return colors.get(level, "#36a64f")

    def _get_teams_color(self, level: NotificationLevel) -> str:
        """獲取 Teams 顏色"""
        colors = {
            NotificationLevel.INFO: "00FF00",
            NotificationLevel.WARNING: "FFFF00",
            NotificationLevel.ERROR: "FF0000",
            NotificationLevel.SUCCESS: "00FF00",
        }
        return colors.get(level, "00FF00")

    # GitHub 集成方法
    async def sync_github_collaborators(self):
        """同步 GitHub 協作者"""
        try:
            repo = self.github_client.get_repo(self.config["github"]["repo"])
            collaborators = repo.get_collaborators()

            for collaborator in collaborators:
                if collaborator.login not in self.users:
                    user = User(
                        id=collaborator.login,
                        username=collaborator.login,
                        email=collaborator.email or f"{collaborator.login}@github.com",
                        role=collaborator.permissions.admin and "admin" or "developer",
                        avatar_url=collaborator.avatar_url,
                        status=UserStatus.OFFLINE,
                        last_seen=datetime.now(),
                        specialties=[],
                    )

                    self.users[user.id] = user
                    self.logger.info(f"同步 GitHub 用戶: {collaborator.login}")

        except Exception as e:
            self.logger.error(f"同步 GitHub 協作者失敗: {e}")

    # 部署通知集成
    async def send_deployment_notification(
        self, environment: str, status: str, commit_sha: str, deployed_by: str
    ):
        """發送部署通知"""
        channel_id = "deployments"

        # 確保部署頻道存在
        if channel_id not in self.channels:
            channel = Channel(
                id=channel_id,
                name="部署通知",
                description="系統部署相關通知",
                type="deployment",
                members=list(self.users.keys()),
                created_at=datetime.now(),
                last_activity=datetime.now(),
            )
            self.channels[channel_id] = channel

        # 創建部署通知消息
        message = Message(
            id=f"deploy_{int(time.time())}",
            sender_id="system",
            channel_id=channel_id,
            message_type=MessageType.DEPLOYMENT_NOTIFICATION,
            content=f"🚀 部署更新 - 環境: {environment}, 狀態: {status}, 提交: {commit_sha[:8]}, 操作者: {deployed_by}",
            timestamp=datetime.now(),
            metadata={
                "environment": environment,
                "status": status,
                "commit_sha": commit_sha,
                "deployed_by": deployed_by,
            },
            mentions=[],
            reactions={},
        )

        # 保存並廣播消息
        if channel_id not in self.messages:
            self.messages[channel_id] = []
        self.messages[channel_id].append(message)

        await self._broadcast_message(message)

        # 發送高優先級通知
        if status.lower() in ["failed", "error"]:
            for user_id in self.users:
                notification = Notification(
                    id=f"deploy_alert_{int(time.time())}_{user_id}",
                    user_id=user_id,
                    title="🚨 部署失敗通知",
                    message=f"環境 {environment} 部署失敗，請立即檢查！",
                    level=NotificationLevel.ERROR,
                    timestamp=datetime.now(),
                    read=False,
                    action_url="/deployments",
                )

                self.notifications[notification.id] = notification
                await self._send_notification(notification)

    def run_server(self):
        """運行服務器"""
        import uvicorn

        uvicorn.run(
            self.app,
            host=self.config["server"]["host"],
            port=self.config["server"]["port"],
            debug=self.config["server"]["debug"],
        )


# 使用示例
if __name__ == "__main__":
    # 初始化協作平台
    hub = CollaborationHub()

    # 運行服務器
    hub.run_server()
