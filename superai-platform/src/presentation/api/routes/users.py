"""User management API routes."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field, EmailStr

router = APIRouter()


# --- Request/Response Schemas ---
class UserCreateRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$")
    email: str = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8, max_length=128)
    full_name: str = Field(default="", max_length=200)
    role: str = Field(default="viewer", pattern=r"^(admin|operator|scientist|developer|viewer)$")


class UserUpdateRequest(BaseModel):
    full_name: str | None = Field(None, max_length=200)
    role: str | None = Field(None, pattern=r"^(admin|operator|scientist|developer|viewer)$")


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    full_name: str
    role: str
    status: str
    created_at: str
    last_login_at: str | None = None


class UserListResponse(BaseModel):
    items: list[UserResponse]
    total: int
    skip: int
    limit: int


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


# --- Endpoints ---
@router.post("", response_model=UserResponse, status_code=201)
async def create_user(request: UserCreateRequest) -> dict[str, Any]:
    """Register a new user."""
    from src.application.use_cases.user_management import CreateUserUseCase
    use_case = CreateUserUseCase()
    result = await use_case.execute(
        username=request.username,
        email=request.email,
        password=request.password,
        full_name=request.full_name,
        role=request.role,
    )
    return result


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest) -> dict[str, Any]:
    """Authenticate user and return JWT tokens."""
    from src.application.use_cases.user_management import AuthenticateUserUseCase
    use_case = AuthenticateUserUseCase()
    result = await use_case.execute(username=request.username, password=request.password)
    return result


@router.get("", response_model=UserListResponse)
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: str | None = Query(None, max_length=100),
) -> dict[str, Any]:
    """List users with pagination and optional search."""
    from src.application.use_cases.user_management import ListUsersUseCase
    use_case = ListUsersUseCase()
    return await use_case.execute(skip=skip, limit=limit, search=search)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str) -> dict[str, Any]:
    """Get user by ID."""
    from src.application.use_cases.user_management import GetUserUseCase
    use_case = GetUserUseCase()
    return await use_case.execute(user_id=user_id)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, request: UserUpdateRequest) -> dict[str, Any]:
    """Update user profile."""
    from src.application.use_cases.user_management import UpdateUserUseCase
    use_case = UpdateUserUseCase()
    return await use_case.execute(user_id=user_id, **request.model_dump(exclude_none=True))


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: str) -> None:
    """Delete user (soft delete)."""
    from src.application.use_cases.user_management import DeleteUserUseCase
    use_case = DeleteUserUseCase()
    await use_case.execute(user_id=user_id)


@router.post("/{user_id}/activate", response_model=UserResponse)
async def activate_user(user_id: str) -> dict[str, Any]:
    """Activate a user account."""
    from src.application.use_cases.user_management import ActivateUserUseCase
    use_case = ActivateUserUseCase()
    return await use_case.execute(user_id=user_id)


@router.post("/{user_id}/suspend", response_model=UserResponse)
async def suspend_user(user_id: str, reason: str = Query("", max_length=500)) -> dict[str, Any]:
    """Suspend a user account."""
    from src.application.use_cases.user_management import SuspendUserUseCase
    use_case = SuspendUserUseCase()
    return await use_case.execute(user_id=user_id, reason=reason)