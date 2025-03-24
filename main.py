import asyncio
from temporalio import workflow
from datetime import timedelta

@workflow.defn
class WaitADayWorkflow:
    @workflow.run
    async def run(self) -> str:
        await asyncio.sleep(24 * 60 * 60)
        return "all done"

@workflow.defn
class WaitAMinuteWorkflow:
    @workflow.run
    async def run(self) -> str:
        self.is_poked = False
        await workflow.wait_condition(lambda: self.is_poked, timeout=timedelta(minutes=1))
        return "all done"

    @workflow.signal
    async def poke(self) -> None:
        self.is_poked = True
