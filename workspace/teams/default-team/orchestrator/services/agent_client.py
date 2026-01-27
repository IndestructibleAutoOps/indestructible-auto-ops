#!/usr/bin/env python3
"""
Agent Communication Client for SuperAgent

Provides HTTP client for communicating with other agents:
- Message sending
- Health checks
- Circuit breaker integration
- Retry handling
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

import aiohttp

from ..config import settings
from ..models.messages import MessageEnvelope, MessageType, Urgency


@dataclass
class AgentInfo:
    """Information about a registered agent."""

    agent_id: str
    url: str
    agent_type: str
    status: str = "unknown"
    last_seen: str | None = None
    capabilities: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class AgentRegistry:
    """Registry of known agents and their status."""

    def __init__(self):
        self._agents: dict[str, AgentInfo] = {}
        self._lock = asyncio.Lock()

        # Pre-register known agents from config
        self._initialize_agents()

    def _initialize_agents(self) -> None:
        """Initialize known agents from configuration."""
        known_agents = [
            ("monitoring-agent", settings.monitoring_agent_url, ["observe", "alert"]),
            (
                "problem-solver-agent",
                settings.problem_solver_agent_url,
                ["rca", "propose"],
            ),
            ("qa-agent", settings.qa_agent_url, ["verify", "validate"]),
            (
                "maintenance-agent",
                settings.maintenance_agent_url,
                ["execute", "rollback"],
            ),
            ("learning-agent", settings.learning_agent_url, ["learn", "knowledge"]),
        ]

        for agent_id, url, capabilities in known_agents:
            self._agents[agent_id] = AgentInfo(
                agent_id=agent_id,
                url=url,
                agent_type=agent_id.replace("-agent", ""),
                capabilities=capabilities,
            )

    async def register(
        self,
        agent_id: str,
        url: str,
        agent_type: str,
        capabilities: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> AgentInfo:
        """Register an agent."""
        async with self._lock:
            info = AgentInfo(
                agent_id=agent_id,
                url=url,
                agent_type=agent_type,
                status="registered",
                last_seen=datetime.now().isoformat(),
                capabilities=capabilities or [],
                metadata=metadata or {},
            )
            self._agents[agent_id] = info
            return info

    async def deregister(self, agent_id: str) -> bool:
        """Deregister an agent."""
        async with self._lock:
            if agent_id in self._agents:
                del self._agents[agent_id]
                return True
            return False

    async def get(self, agent_id: str) -> AgentInfo | None:
        """Get agent info."""
        async with self._lock:
            return self._agents.get(agent_id)

    async def list_agents(self, status: str | None = None) -> list[AgentInfo]:
        """List all registered agents."""
        async with self._lock:
            agents = list(self._agents.values())

        if status:
            agents = [a for a in agents if a.status == status]

        return agents

    async def update_status(self, agent_id: str, status: str) -> bool:
        """Update agent status."""
        async with self._lock:
            if agent_id in self._agents:
                self._agents[agent_id].status = status
                self._agents[agent_id].last_seen = datetime.now().isoformat()
                return True
            return False


class AgentClient:
    """
    HTTP client for agent-to-agent communication.

    Provides:
    - Async message sending
    - Health checks
    - Automatic retries
    - Timeout handling
    """

    def __init__(
        self,
        registry: AgentRegistry | None = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        self._registry = registry or AgentRegistry()
        self._timeout = timeout
        self._max_retries = max_retries
        self._retry_delay = retry_delay
        self._session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session."""
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self._timeout)
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session

    async def send_message(
        self,
        target_agent: str,
        message: MessageEnvelope,
        retry: bool = True,
    ) -> dict[str, Any]:
        """
        Send a message to another agent.

        Returns response dict or error dict.
        """
        agent = await self._registry.get(target_agent)
        if not agent:
            return {"status": "error", "error": f"Unknown agent: {target_agent}"}

        url = f"{agent.url}/message"
        attempts = self._max_retries if retry else 1

        for attempt in range(attempts):
            try:
                session = await self._get_session()
                async with session.post(
                    url,
                    json=message.model_dump(),
                    headers={"Content-Type": "application/json"},
                ) as response:
                    if response.status == 200:
                        await self._registry.update_status(target_agent, "healthy")
                        return await response.json()
                    else:
                        text = await response.text()
                        if attempt < attempts - 1:
                            await asyncio.sleep(self._retry_delay * (attempt + 1))
                            continue
                        return {
                            "status": "error",
                            "error": f"HTTP {response.status}: {text}",
                        }
            except TimeoutError:
                await self._registry.update_status(target_agent, "timeout")
                if attempt < attempts - 1:
                    await asyncio.sleep(self._retry_delay * (attempt + 1))
                    continue
                return {"status": "error", "error": "Request timeout"}
            except aiohttp.ClientError as e:
                await self._registry.update_status(target_agent, "error")
                if attempt < attempts - 1:
                    await asyncio.sleep(self._retry_delay * (attempt + 1))
                    continue
                return {"status": "error", "error": str(e)}

        return {"status": "error", "error": "Max retries exceeded"}

    async def check_health(self, agent_id: str) -> dict[str, Any]:
        """Check health of an agent."""
        agent = await self._registry.get(agent_id)
        if not agent:
            return {"status": "unknown", "error": f"Unknown agent: {agent_id}"}

        url = f"{agent.url}/health"

        try:
            session = await self._get_session()
            async with session.get(url) as response:
                if response.status == 200:
                    await self._registry.update_status(agent_id, "healthy")
                    data = await response.json()
                    return {"status": "healthy", "data": data}
                else:
                    await self._registry.update_status(agent_id, "unhealthy")
                    return {"status": "unhealthy", "code": response.status}
        except TimeoutError:
            await self._registry.update_status(agent_id, "timeout")
            return {"status": "timeout"}
        except aiohttp.ClientError as e:
            await self._registry.update_status(agent_id, "error")
            return {"status": "error", "error": str(e)}

    async def check_all_health(self) -> dict[str, dict[str, Any]]:
        """Check health of all registered agents."""
        agents = await self._registry.list_agents()
        results = {}

        tasks = [self.check_health(agent.agent_id) for agent in agents]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        for agent, response in zip(agents, responses, strict=False):
            if isinstance(response, Exception):
                results[agent.agent_id] = {"status": "error", "error": str(response)}
            else:
                results[agent.agent_id] = response

        return results

    async def broadcast_message(
        self,
        message: MessageEnvelope,
        agents: list[str] | None = None,
    ) -> dict[str, dict[str, Any]]:
        """
        Broadcast a message to multiple agents.

        Returns dict of agent_id -> response.
        """
        if agents is None:
            all_agents = await self._registry.list_agents()
            agents = [a.agent_id for a in all_agents]

        results = {}
        tasks = []

        for agent_id in agents:
            # Create copy with updated target
            msg_copy = MessageEnvelope(
                meta={**message.meta, "target_agent": agent_id},
                context=message.context,
                payload=message.payload,
            )
            tasks.append(self.send_message(agent_id, msg_copy))

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        for agent_id, response in zip(agents, responses, strict=False):
            if isinstance(response, Exception):
                results[agent_id] = {"status": "error", "error": str(response)}
            else:
                results[agent_id] = response

        return results

    async def send_incident_signal(
        self,
        target_agent: str,
        trace_id: str,
        incident_type: str,
        severity: str,
        affected_resources: list[str],
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Helper to send incident signal."""
        message = MessageEnvelope.create(
            message_type=MessageType.INCIDENT_SIGNAL,
            payload={
                "incident_type": incident_type,
                "severity": severity,
                "affected_resources": affected_resources,
                "metadata": metadata or {},
            },
            source_agent="super-agent",
            target_agent=target_agent,
            trace_id=trace_id,
            urgency=Urgency.P1 if severity == "critical" else Urgency.P2,
        )
        return await self.send_message(target_agent, message)

    async def request_rca(
        self,
        trace_id: str,
        incident_id: str,
        incident_type: str,
        affected_resources: list[str],
    ) -> dict[str, Any]:
        """Request RCA from problem-solver-agent."""
        message = MessageEnvelope.create(
            message_type=MessageType.INCIDENT_SIGNAL,
            payload={
                "action": "perform_rca",
                "incident_id": incident_id,
                "incident_type": incident_type,
                "affected_resources": affected_resources,
            },
            source_agent="super-agent",
            target_agent="problem-solver-agent",
            trace_id=trace_id,
        )
        return await self.send_message("problem-solver-agent", message)

    async def request_verification(
        self,
        trace_id: str,
        incident_id: str,
        proposal_id: str,
        proposal: dict[str, Any],
    ) -> dict[str, Any]:
        """Request verification from qa-agent."""
        message = MessageEnvelope.create(
            message_type=MessageType.FIX_PROPOSAL,
            payload={
                "action": "verify",
                "incident_id": incident_id,
                "proposal_id": proposal_id,
                "proposal": proposal,
            },
            source_agent="super-agent",
            target_agent="qa-agent",
            trace_id=trace_id,
        )
        return await self.send_message("qa-agent", message)

    async def request_execution(
        self,
        trace_id: str,
        incident_id: str,
        proposal_id: str,
        execution_plan: dict[str, Any],
    ) -> dict[str, Any]:
        """Request execution from maintenance-agent."""
        message = MessageEnvelope.create(
            message_type=MessageType.EXECUTION_ORDER,
            payload={
                "incident_id": incident_id,
                "proposal_id": proposal_id,
                "execution_plan": execution_plan,
            },
            source_agent="super-agent",
            target_agent="maintenance-agent",
            trace_id=trace_id,
        )
        return await self.send_message("maintenance-agent", message)

    async def close(self) -> None:
        """Close the client session."""
        if self._session and not self._session.closed:
            await self._session.close()

    @property
    def registry(self) -> AgentRegistry:
        """Get the agent registry."""
        return self._registry
