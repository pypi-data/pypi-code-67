# @Created Date: 2020-09-17 12:02:31 am
# @Filename: database.py
# @Email:  1730416009@stu.suda.edu.cn
# @Author: ZeFeng Zhu
# @Last Modified: 2020-09-27 03:18:19 pm
# @Copyright (c) 2020 MinghuiGroup, Soochow University
from asyncio import sleep as asyncio_sleep, Queue
from queue import Queue
import databases
import orm
import sqlalchemy
from sqlite3 import OperationalError
from unsync import unsync
from typing import Dict, Iterable
from pdb_profiling.log import Abclog


class SqliteDB(Abclog):

    def init_table_model(self):
        pass

    def __init__(self, url: str, drop_all: bool = False):
        self.metadata = sqlalchemy.MetaData()
        self.database = databases.Database(url)
        self.engine = sqlalchemy.create_engine(url)
        self.engine.execute("PRAGMA journal_mode=WAL")
        self.init_table_model()
        if drop_all:
            self.metadata.drop_all(self.engine, checkfirst=True)
        self.metadata.create_all(self.engine, checkfirst=True)
        # self.queue = Queue()

    def close(self):
        """TODO: make it real"""
        self.engine.dispose()

    def sync_insert(self, table, values: Iterable[Dict], prefix_with: str = "OR IGNORE"):
        self.engine.execute(
            table.__table__.insert().prefix_with(prefix_with),
            values)

    '''
    @unsync
    async def async_insert_queue(self, table, values: Iterable[Dict], prefix_with: str = "OR IGNORE", insert_sleep: float = 30.5):
        self.queue.put_nowait(self.database.execute(table.__table__.insert().values(values).prefix_with(prefix_with)))
        now_task = self.queue.get_nowait()
        while True:
            try:
                await now_task
                self.queue.task_done()
                break
            except OperationalError as e:
                self.logger.error(f"{e}, sleep {insert_sleep}s and try again")
                await asyncio_sleep(insert_sleep)
    '''

    @unsync
    async def async_insert(self, table, values: Iterable[Dict], prefix_with: str = "OR IGNORE", insert_sleep:float=30.5):
        while True:
            try:
                query = table.__table__.insert().values(values).prefix_with(prefix_with)
                await self.database.execute(query)
                break
            except OperationalError as e:
                self.logger.error(f"{e}, sleep {insert_sleep}s and try again")
                await asyncio_sleep(insert_sleep)
