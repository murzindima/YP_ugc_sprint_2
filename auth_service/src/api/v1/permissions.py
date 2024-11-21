from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.requests import Request

from src.core.messages import PERMISSION_NOT_FOUND
from src.schemas.permission import Permission as PermissionSchema
from src.schemas.permission import PermissionCreate as PermissionCreateSchema
from src.schemas.permission import PermissionUpdate as PermissionUpdateSchema
from src.services.permission import PermissionService, get_permission_service
from src.services.utils import requires_admin

router = APIRouter()


@router.get("", response_model=list[PermissionSchema], status_code=status.HTTP_200_OK)
@requires_admin
async def get_permissions(
    request: Request,
    permission_service: PermissionService = Depends(get_permission_service),
) -> list[PermissionSchema]:
    """Returns multiple permissions."""
    permissions = await permission_service.get_all_models()
    return permissions


@router.get(
    "/{permission_id}", response_model=PermissionSchema, status_code=status.HTTP_200_OK
)
@requires_admin
async def get_permission(
    request: Request,
    permission_id: UUID,
    permission_service: PermissionService = Depends(get_permission_service),
) -> PermissionSchema:
    """Returns a permission by identifier."""
    permission = await permission_service.get_model_by_id(permission_id)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=PERMISSION_NOT_FOUND
        )

    return permission


@router.post("", response_model=PermissionSchema, status_code=status.HTTP_201_CREATED)
@requires_admin
async def create_permission(
    permission_data: PermissionCreateSchema,
    request: Request,
    permission_service: PermissionService = Depends(get_permission_service),
) -> PermissionSchema:
    """Creates a new permission."""
    permission = await permission_service.create_model(permission_data)
    return permission


@router.delete("/{permission_id}", response_model=PermissionSchema)
@requires_admin
async def delete_permission(
    request: Request,
    permission_id: UUID,
    permission_service: PermissionService = Depends(get_permission_service),
) -> PermissionSchema:
    """Deletes a permission by identifier."""
    permission = await permission_service.delete_model(permission_id)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=PERMISSION_NOT_FOUND
        )

    return permission


@router.patch("/{permission_id}", response_model=PermissionSchema)
@requires_admin
async def update_permission(
    request: Request,
    permission_id: UUID,
    new_data: PermissionUpdateSchema,
    permission_service: PermissionService = Depends(get_permission_service),
) -> PermissionSchema:
    """Updates a permission by identifier."""
    permission = await permission_service.update_model(permission_id, new_data)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=PERMISSION_NOT_FOUND
        )

    return permission
