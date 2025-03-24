import pytest

from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker
from main import WaitADayWorkflow

@pytest.mark.asyncio
async def test_wait_a_day_workflow():
    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker(env.client, task_queue="tq1", workflows=[WaitADayWorkflow]):
            assert "all done" == await env.client.execute_workflow(WaitADayWorkflow.run, id="wf1", task_queue="tq1")
