import pytest
import uuid
from src.application.User.useCase.CreateUser import CreateUser
from src.application.User.useCase.GetAllUsers import GetAllUsers
from src.application.User.useCase.GetUserById import GetUserById
from src.application.User.useCase.UpdateUser import UpdateUser
from src.application.User.useCase.DeleteUser import DeleteUser
from src.application.User.dtos.UserInput import UserInput
from src.tests.config import database


created_user_id = None


@pytest.mark.asyncio
async def test_CreateUser_Success():
    global created_user_id
    useCase = CreateUser(database)
    data = UserInput(
        username="valdir_dev",
        email="valdir@dev.com",
        password="secure_password"
    )
    
    result = await useCase.Execute(data, lambda: str(uuid.uuid4()))
    created_user_id = result.id
    assert result.username == data.username


@pytest.mark.asyncio
async def test_GetAllUsers_Success():
    useCase = GetAllUsers(database)
    result = await useCase.Execute()
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_GetUserById_Success():
    useCase = GetUserById(database)
    result = await useCase.Execute(created_user_id or "test-id")
    assert result.id is not None


@pytest.mark.asyncio
async def test_UpdateUser_Success():
    useCase = UpdateUser(database)
    data = UserInput(
        username="valdir_updated",
        email="valdir.updated@dev.com",
        password="new_password"
    )
    
    result = await useCase.Execute(created_user_id or "test-id", data)
    assert result.username == data.username


@pytest.mark.asyncio
async def test_DeleteUser_Success():
    useCase = DeleteUser(database)
    result = await useCase.Execute(created_user_id or "test-id")
    assert isinstance(result, bool)
