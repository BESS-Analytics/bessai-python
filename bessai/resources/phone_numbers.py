"""Phone numbers resource."""
from typing import List

from bessai._client import SyncHTTPClient, AsyncHTTPClient
from bessai.types.phone_number import PhoneNumber, PhoneNumberCreate, PhoneNumberUpdate


class PhoneNumbersResource:
    """Sync phone numbers resource."""

    def __init__(self, client: SyncHTTPClient):
        self._client = client

    def create(self, **kwargs) -> PhoneNumber:
        """Create a phone number."""
        body = PhoneNumberCreate(**kwargs).model_dump(exclude_none=True)
        data = self._client.post("/v1/phone-numbers", json=body)
        return PhoneNumber(**data)

    def list(self, skip: int = 0, limit: int = 20) -> List[PhoneNumber]:
        """List phone numbers."""
        data = self._client.get("/v1/phone-numbers", params={"skip": skip, "limit": limit})
        items = data if isinstance(data, list) else data.get("items", [])
        return [PhoneNumber(**p) for p in items]

    def get(self, phone_number_id: str) -> PhoneNumber:
        """Get phone number by ID."""
        data = self._client.get(f"/v1/phone-numbers/{phone_number_id}")
        return PhoneNumber(**data)

    def update(self, phone_number_id: str, **kwargs) -> PhoneNumber:
        """Update a phone number."""
        body = PhoneNumberUpdate(**kwargs).model_dump(exclude_none=True)
        data = self._client.patch(f"/v1/phone-numbers/{phone_number_id}", json=body)
        return PhoneNumber(**data)

    def delete(self, phone_number_id: str) -> None:
        """Delete a phone number."""
        self._client.delete(f"/v1/phone-numbers/{phone_number_id}")


class AsyncPhoneNumbersResource:
    """Async phone numbers resource."""

    def __init__(self, client: AsyncHTTPClient):
        self._client = client

    async def create(self, **kwargs) -> PhoneNumber:
        body = PhoneNumberCreate(**kwargs).model_dump(exclude_none=True)
        data = await self._client.post("/v1/phone-numbers", json=body)
        return PhoneNumber(**data)

    async def list(self, skip: int = 0, limit: int = 20) -> List[PhoneNumber]:
        data = await self._client.get("/v1/phone-numbers", params={"skip": skip, "limit": limit})
        items = data if isinstance(data, list) else data.get("items", [])
        return [PhoneNumber(**p) for p in items]

    async def get(self, phone_number_id: str) -> PhoneNumber:
        data = await self._client.get(f"/v1/phone-numbers/{phone_number_id}")
        return PhoneNumber(**data)

    async def update(self, phone_number_id: str, **kwargs) -> PhoneNumber:
        body = PhoneNumberUpdate(**kwargs).model_dump(exclude_none=True)
        data = await self._client.patch(f"/v1/phone-numbers/{phone_number_id}", json=body)
        return PhoneNumber(**data)

    async def delete(self, phone_number_id: str) -> None:
        await self._client.delete(f"/v1/phone-numbers/{phone_number_id}")
