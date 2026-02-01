#!/usr/bin/env python3
"""
GL API Gateway Authenticator
=============================
認證器 - JWT、API Key 等認證機制

GL Governance Layer: GL10-29 (Operational Layer)
"""

import jwt
import hashlib
import time
from typing import Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging


@dataclass
class AuthToken:
    """認證令牌"""
    user_id: str
    username: str
    roles: list
    expires_at: float
    token_type: str = "Bearer"
    
    def is_expired(self) -> bool:
        """檢查令牌是否過期"""
        return time.time() > self.expires_at
    
    def has_role(self, role: str) -> bool:
        """檢查是否有指定角色"""
        return role in self.roles


class Authenticator:
    """API 網關認證器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化認證器
        
        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.logger = self._setup_logger()
        
        # JWT 配置
        self.jwt_enabled = self.config.get('authentication', {}).get('jwt', {}).get('enabled', True)
        self.jwt_secret = self.config.get('authentication', {}).get('jwt', {}).get('secret', 'default-secret')
        self.jwt_algorithm = self.config.get('authentication', {}).get('jwt', {}).get('algorithm', 'HS256')
        self.jwt_expiration = self.config.get('authentication', {}).get('jwt', {}).get('expiration', 3600)
        
        # API Key 配置
        self.api_key_enabled = self.config.get('authentication', {}).get('api_key', {}).get('enabled', True)
        self.api_key_header = self.config.get('authentication', {}).get('api_key', {}).get('header', 'X-API-Key')
        
        # API Keys 存儲 (實際應從數據庫或文件加載)
        self.api_keys: Dict[str, Dict[str, Any]] = {}
        
        self.logger.info("Authenticator initialized")
    
    def _setup_logger(self) -> logging.Logger:
        """設置日誌"""
        logger = logging.getLogger('Authenticator')
        level = self.config.get('logging', {}).get('level', 'INFO')
        logger.setLevel(getattr(logging, level))
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def authenticate(self, headers: Dict[str, str]) -> Optional[AuthToken]:
        """
        認證請求
        
        Args:
            headers: HTTP 請求頭
            
        Returns:
            認證令牌或None
        """
        # 嘗試 JWT 認證
        if self.jwt_enabled:
            auth_header = headers.get('Authorization', '')
            if auth_header.startswith('Bearer '):
                token = auth_header[7:]
                auth_token = self.verify_jwt(token)
                if auth_token:
                    return auth_token
        
        # 嘗試 API Key 認證
        if self.api_key_enabled:
            api_key = headers.get(self.api_key_header)
            if api_key:
                auth_token = self.verify_api_key(api_key)
                if auth_token:
                    return auth_token
        
        self.logger.debug("Authentication failed")
        return None
    
    def generate_jwt(self, user_id: str, username: str, roles: list) -> str:
        """
        生成 JWT 令牌
        
        Args:
            user_id: 用戶ID
            username: 用戶名
            roles: 角色列表
            
        Returns:
            JWT 令牌字符串
        """
        now = datetime.utcnow()
        expires_at = now + timedelta(seconds=self.jwt_expiration)
        
        payload = {
            'user_id': user_id,
            'username': username,
            'roles': roles,
            'iat': now.timestamp(),
            'exp': expires_at.timestamp()
        }
        
        token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
        
        self.logger.info(f"JWT token generated for user {username}")
        return token
    
    def verify_jwt(self, token: str) -> Optional[AuthToken]:
        """
        驗證 JWT 令牌
        
        Args:
            token: JWT 令牌
            
        Returns:
            認證令牌或None
        """
        try:
            payload = jwt.decode(
                token,
                self.jwt_secret,
                algorithms=[self.jwt_algorithm]
            )
            
            auth_token = AuthToken(
                user_id=payload['user_id'],
                username=payload['username'],
                roles=payload.get('roles', []),
                expires_at=payload['exp']
            )
            
            if auth_token.is_expired():
                self.logger.warning(f"JWT token expired for user {auth_token.username}")
                return None
            
            self.logger.debug(f"JWT token verified for user {auth_token.username}")
            return auth_token
            
        except jwt.ExpiredSignatureError:
            self.logger.warning("JWT token expired")
            return None
        except jwt.InvalidTokenError as e:
            self.logger.warning(f"Invalid JWT token: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error verifying JWT token: {e}")
            return None
    
    def generate_api_key(self, user_id: str, username: str, roles: list) -> str:
        """
        生成 API Key
        
        Args:
            user_id: 用戶ID
            username: 用戶名
            roles: 角色列表
            
        Returns:
            API Key
        """
        # 生成 API Key (簡單實現，實際應該更複雜)
        key_data = f"{user_id}-{username}-{time.time()}"
        api_key = hashlib.sha256(key_data.encode()).hexdigest()
        
        # 存儲 API Key
        self.api_keys[api_key] = {
            'user_id': user_id,
            'username': username,
            'roles': roles,
            'created_at': time.time()
        }
        
        self.logger.info(f"API Key generated for user {username}")
        return api_key
    
    def verify_api_key(self, api_key: str) -> Optional[AuthToken]:
        """
        驗證 API Key
        
        Args:
            api_key: API Key
            
        Returns:
            認證令牌或None
        """
        key_data = self.api_keys.get(api_key)
        if not key_data:
            self.logger.warning("Invalid API Key")
            return None
        
        # API Key 不過期 (可以根據需要添加過期邏輯)
        auth_token = AuthToken(
            user_id=key_data['user_id'],
            username=key_data['username'],
            roles=key_data.get('roles', []),
            expires_at=float('inf'),
            token_type="ApiKey"
        )
        
        self.logger.debug(f"API Key verified for user {auth_token.username}")
        return auth_token
    
    def revoke_api_key(self, api_key: str) -> bool:
        """
        撤銷 API Key
        
        Args:
            api_key: API Key
            
        Returns:
            成功返回True
        """
        if api_key in self.api_keys:
            del self.api_keys[api_key]
            self.logger.info("API Key revoked")
            return True
        
        self.logger.warning("API Key not found")
        return False
