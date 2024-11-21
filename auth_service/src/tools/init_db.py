import asyncio

import typer
from sqlalchemy import select

from src.db.postgres import async_session
from src.models.permission import Permission
from src.models.role import Role, RoleType
from src.models.role_permission import RolePermission
from src.models.user import User

app = typer.Typer()

VIEW_OTHER_USER = "VIEW OTHER USER"
VIEW_OWN_USER = "VIEW OWN USER"
VIEW_OTHER_LOGIN_HISTORY = "VIEW OTHER LOGIN_HISTORY"
VIEW_OWN_LOGIN_HISTORY = "VIEW OWN LOGIN_HISTORY"
EDIT_OTHER_USER = "EDIT OTHER USER"
EDIT_OWN_USER = "EDIT OWN USER"


async def _create_permissions():
    possible_permissions = [
        VIEW_OTHER_USER,
        VIEW_OWN_USER,
        VIEW_OTHER_LOGIN_HISTORY,
        VIEW_OWN_LOGIN_HISTORY,
        EDIT_OTHER_USER,
        EDIT_OWN_USER,
    ]
    async with async_session() as session:
        for permission in possible_permissions:
            exists = (
                await session.execute(
                    select(Permission).where(Permission.name == permission)
                )
            ).scalar_one_or_none()
            if not exists:
                new_permission = Permission(name=permission)
                session.add(new_permission)
                await session.commit()


async def _create_roles():
    async with async_session() as session:
        for role in RoleType:
            exists = (
                (await session.execute(select(Role).where(Role.name == role.value)))
                .unique()
                .scalar_one_or_none()
            )
            if not exists:
                new_role = Role(name=role.value)
                session.add(new_role)
                await session.commit()


async def _assign_permissions_to_roles():
    role_permissions = {
        RoleType.ADMIN: [
            VIEW_OWN_USER,
            VIEW_OTHER_USER,
            EDIT_OWN_USER,
            EDIT_OTHER_USER,
            VIEW_OWN_LOGIN_HISTORY,
            VIEW_OTHER_LOGIN_HISTORY,
        ],
        RoleType.MODERATOR: [
            VIEW_OWN_USER,
            VIEW_OTHER_USER,
            VIEW_OWN_LOGIN_HISTORY,
            VIEW_OTHER_LOGIN_HISTORY,
            EDIT_OWN_USER,
        ],
        RoleType.MEMBER: [
            VIEW_OWN_USER,
            VIEW_OTHER_USER,
            VIEW_OWN_LOGIN_HISTORY,
            EDIT_OWN_USER,
        ],
        RoleType.SUBSCRIBER: [
            VIEW_OWN_USER,
            VIEW_OTHER_USER,
            VIEW_OWN_LOGIN_HISTORY,
            EDIT_OWN_USER,
        ],
    }
    async with async_session() as session:
        for role_type, permissions in role_permissions.items():
            role = (
                (
                    await session.execute(
                        select(Role).where(Role.name == role_type.value)
                    )
                )
                .unique()
                .scalar_one_or_none()
            )

            if role:
                for permission_name in permissions:
                    permission = (
                        (
                            await session.execute(
                                select(Permission).where(
                                    Permission.name == permission_name
                                )
                            )
                        )
                        .unique()
                        .scalar_one_or_none()
                    )

                    if permission:
                        role_permission_exists = (
                            (
                                await session.execute(
                                    select(RolePermission)
                                    .where(RolePermission.role_id == role.id)
                                    .where(
                                        RolePermission.permission_id == permission.id
                                    )
                                )
                            )
                            .unique()
                            .scalar_one_or_none()
                        )

                        if not role_permission_exists:
                            new_role_permission = RolePermission(
                                role_id=role.id, permission_id=permission.id
                            )
                            session.add(new_role_permission)

                await session.commit()


async def _create_admin(email: str, password: str, first_name: str, last_name: str):
    async with async_session() as session:
        admin_exists = (
            (await session.execute(select(User).where(User.email == email)))
            .unique()
            .scalar_one_or_none()
        )
        if admin_exists:
            print("Admin with this email already exists")
            return

        admin_role = (
            (
                await session.execute(
                    select(Role).where(Role.name == RoleType.ADMIN.value)
                )
            )
            .unique()
            .scalar_one_or_none()
        )
        if not admin_role:
            raise ValueError("Admin role is not defined")

        admin = User(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role_id=admin_role.id,
        )
        session.add(admin)
        await session.commit()


@app.command()
def create_permissions():
    asyncio.run(_create_permissions())


@app.command()
def create_roles():
    asyncio.run(_create_roles())


@app.command()
def assign_permissions_to_roles():
    asyncio.run(_assign_permissions_to_roles())


@app.command()
def create_admin(email: str, password: str, first_name: str, last_name: str):
    asyncio.run(_create_admin(email, password, first_name, last_name))


if __name__ == "__main__":
    app()
