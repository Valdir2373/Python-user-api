import pytest
import httpx
from src.tests.config import API
from src.tests.keyPublicApi import GeneratePublicToken

created_user_id = None


@pytest.mark.asyncio
async def test_Route_CreateUser_ShouldReturn200():
    global created_user_id
    path = "/users"
    method = "POST"
    url = f"{API}{path}"
    payload = {
        "username": "valdir_controller",
        "email": "valdir.controller@dev.com",
        "password": "secure_password"
    }
    
    headers = GeneratePublicToken(path, method)
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers, timeout=5)
        assert response.status_code == 200
        data = response.json()
        created_user_id = data.get("id")


@pytest.mark.asyncio
async def test_Route_GetAllUsers_ShouldReturn200():
    path = "/users"
    method = "GET"
    url = f"{API}{path}"
    
    headers = GeneratePublicToken(path, method)
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, timeout=5)
        assert response.status_code == 200
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_Route_GetUserById_ShouldReturn200():
    path = f"/users/{created_user_id or 'test-id'}"
    method = "GET"
    url = f"{API}{path}"
    
    headers = GeneratePublicToken(path, method)
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, timeout=5)
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_Route_UpdateUser_ShouldReturn200():
    path = f"/users/{created_user_id or 'test-id'}"
    method = "PUT"
    url = f"{API}{path}"
    payload = {
        "username": "valdir_updated",
        "email": "valdir.updated@api.com",
        "password": "new_password"
    }
    
    headers = GeneratePublicToken(path, method)
    
    async with httpx.AsyncClient() as client:
        response = await client.put(url, json=payload, headers=headers, timeout=5)
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_Route_DeleteUser_ShouldReturn200():
    path = f"/users/{created_user_id or 'test-id'}"
    method = "DELETE"
    url = f"{API}{path}"
    
    headers = GeneratePublicToken(path, method)
    
    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=headers, timeout=5)
        assert response.status_code == 200
