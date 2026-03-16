import asyncpg
from typing import Any, Dict, List, Optional, Sequence, Union
from src.infra.config.ConfigDB import ConfigDB, IVariablesPostgres
from src.domain.database.IDataAcess import IDataAccess


class PostgresDataAccess(IDataAccess):
    def __init__(self, dbConfig: 'ConfigDB'):
        vars: IVariablesPostgres = dbConfig.get_variables_postgresql()
        self.host = vars.host
        self.port = vars.port
        self.user = vars.user
        self.password = vars.password
        self.database = vars.database
        self.pool = None

    async def connect(self) -> None:
        if not self.pool:
            self.pool = await asyncpg.create_pool(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )

    async def disconnect(self) -> None:
        if self.pool:
            await self.pool.close()

    async def find_many(
        self,
        collectionName: str,
        query: Optional[Dict[str, Any]] = None,
        selectFields: Optional[Sequence[str]] = None
    ) -> List[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            sql = self._buildSelectQuery(collectionName, selectFields)
            whereClause, params = self._buildWhereClause(query)
            rows = await conn.fetch(sql + whereClause, *params)
            return [dict(row) for row in rows]

    async def find_one(
        self,
        collectionName: str,
        query: Dict[str, Any],
        selectFields: Optional[Sequence[str]] = None
    ) -> Optional[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            sql = self._buildSelectQuery(collectionName, selectFields)
            whereClause, params = self._buildWhereClause(query)
            row = await conn.fetchrow(sql + whereClause, *params)
            return dict(row) if row else None

    async def create(
        self,
        collectionName: str,
        data: Dict[str, Any]
    ) -> Union[str, int, None]:
        async with self.pool.acquire() as conn:
            sql, params = self._buildInsertQuery(collectionName, data)
            result = await conn.fetchval(sql, *params)
            return result

    async def update(
        self,
        collectionName: str,
        query: Dict[str, Any],
        data: Dict[str, Any]
    ) -> int:
        async with self.pool.acquire() as conn:
            sql, params = self._buildUpdateQuery(collectionName, data, query)
            result = await conn.execute(sql, *params)
            return self._parseAffectedRows(result)

    async def remove(
        self,
        collectionName: str,
        query: Dict[str, Any]
    ) -> int:
        async with self.pool.acquire() as conn:
            whereClause, params = self._buildWhereClause(query)
            sql = f"DELETE FROM {collectionName} " + whereClause
            result = await conn.execute(sql, *params)
            return self._parseAffectedRows(result)

    def _buildSelectQuery(self, table: str, fields: Optional[Sequence[str]]) -> str:
        columns = ", ".join(fields) if fields else "*"
        return f"SELECT {columns} FROM {table} "

    def _buildWhereClause(self, query: Optional[Dict[str, Any]]) -> tuple:
        if not query:
            return "", []
        
        conditions = [f"{key} = $" for key in query.keys()]
        where = "WHERE " + " AND ".join(conditions)
        return self._addParamPlaceholders(where), list(query.values())

    def _addParamPlaceholders(self, clause: str) -> str:
        counter = iter(range(1, clause.count("$") + 1))
        return "".join(f"${next(counter)}" if c == "$" else c for c in clause)

    def _buildInsertQuery(self, table: str, data: Dict[str, Any]) -> tuple:
        columns = ", ".join(data.keys())
        placeholders = ", ".join([f"${i+1}" for i in range(len(data))])
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING id"
        return sql, list(data.values())

    def _buildUpdateQuery(self, table: str, data: Dict[str, Any], query: Dict[str, Any]) -> tuple:
        setClause = self._buildSetClause(data)
        offset = len(data)
        whereClause, whereParams = self._buildWhereClauseWithOffset(query, offset)
        sql = f"UPDATE {table} SET {setClause} " + whereClause
        return sql, list(data.values()) + whereParams

    def _buildWhereClauseWithOffset(self, query: Optional[Dict[str, Any]], offset: int = 0) -> tuple:
        if not query:
            return "", []
        
        conditions = [f"{key} = ${offset + i + 1}" for i, key in enumerate(query.keys())]
        where = "WHERE " + " AND ".join(conditions)
        return where, list(query.values())

    def _buildSetClause(self, data: Dict[str, Any]) -> str:
        clauses = [f"{key} = ${i+1}" for i, key in enumerate(data.keys())]
        return ", ".join(clauses)

    def _parseAffectedRows(self, result: str) -> int:
        return int(result.split()[-1]) if result else 0
