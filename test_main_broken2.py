import uuid
import pytest
from temporalio import workflow
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker
from dataclasses import dataclass
from datetime import timedelta

@dataclass
class SayHelloArgs:
    name: str = ""

@workflow.defn
class SayHello:
    @workflow.run
    async def run(self, args: SayHelloArgs) -> str:
        self.signal_received = False
        try:
            await workflow.wait_condition(lambda: self.signal_received, timeout=timedelta(minutes=1))
        except asyncio.TimeoutError as e:
            pass
        return "Hello"

    @workflow.signal
    async def does_nothing(self):
        self.signal_received = True


@pytest.mark.asyncio
async def test_empty_event_workflow():
    task_queue_name = str(uuid.uuid4())
    async with await WorkflowEnvironment.start_time_skipping() as env:

        async with Worker(
                env.client,
                task_queue=task_queue_name,
                workflows=[SayHello],
                ):
            handle = await env.client.execute_workflow(
                    SayHello,
                    SayHelloArgs(),
                    id=str(uuid.uuid4()),
                    task_queue=task_queue_name,
                    )

            assert "Hello" == handle
            return
            assert "Hello" == await handle.result()

