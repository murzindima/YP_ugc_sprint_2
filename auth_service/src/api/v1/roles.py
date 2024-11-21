from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.requests import Request

from src.core.messages import ROLE_NOT_FOUND
from src.schemas.role import Role as RoleSchema
from src.schemas.role import RoleCreate as RoleCreateSchema
from src.schemas.role import RoleUpdate as RoleUpdateSchema
from src.services.role import RoleService, get_role_service
from src.services.utils import requires_admin

router = APIRouter()


@router.get("", response_model=list[RoleSchema], status_code=status.HTTP_200_OK)
@requires_admin
async def get_roles(
    request: Request,
    role_service: RoleService = Depends(get_role_service),
) -> list[RoleSchema]:
    """Returns multiple roles."""
    roles = await role_service.get_all_models()
    return roles


@router.get("/{role_id}", response_model=RoleSchema, status_code=status.HTTP_200_OK)
@requires_admin
async def get_role(
    request: Request,
    role_id: UUID,
    role_service: RoleService = Depends(get_role_service),
) -> RoleSchema:
    """Returns a role by identifier."""
    role = await role_service.get_model_by_id(role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ROLE_NOT_FOUND
        )

    return role


@router.post("", response_model=RoleSchema, status_code=status.HTTP_201_CREATED)
@requires_admin
async def create_role(
    role_data: RoleCreateSchema,
    request: Request,
    role_service: RoleService = Depends(get_role_service),
) -> RoleSchema:
    """Creates a new role."""
    role = await role_service.create_model(role_data)
    return role


@router.delete("/{role_id}", response_model=RoleSchema)
@requires_admin
async def delete_role(
    request: Request,
    role_id: UUID,
    role_service: RoleService = Depends(get_role_service),
) -> RoleSchema:
    """Deletes a role by identifier."""
    try:
        role = await role_service.delete_model(role_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Cannot delete role.",
        )
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ROLE_NOT_FOUND
        )

    return role


@router.patch("/{role_id}", response_model=RoleSchema)
@requires_admin
async def update_role(
    request: Request,
    role_id: UUID,
    new_data: RoleUpdateSchema,
    role_service: RoleService = Depends(get_role_service),
) -> RoleSchema:
    """Updates a role by identifier."""
    role = await role_service.update_model(role_id, new_data)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ROLE_NOT_FOUND
        )

    return role
