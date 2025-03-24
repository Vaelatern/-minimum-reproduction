import pytest

from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker
from main import WaitAMinuteWorkflow

@pytest.mark.asyncio
async def test_wait_a_minute_workflow():
    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker(env.client, task_queue="tq2", workflows=[WaitAMinuteWorkflow]):
            assert "all done" == await env.client.execute_workflow(WaitAMinuteWorkflow.run, id="wf2", task_queue="tq2")
