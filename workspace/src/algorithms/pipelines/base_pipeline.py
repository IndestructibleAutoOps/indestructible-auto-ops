"""
GL40-49: Algorithm Layer
GL41: Pipelines Module - Base Pipeline
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


class PipelineStep(ABC):
    """Base class for pipeline steps"""

    def __init__(self, step_config: dict[str, Any]):
        self.step_config = step_config
        self.step_name = step_config.get('name', 'unnamed_step')
        self.step_id = f"STEP-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    @abstractmethod
    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        """Execute the pipeline step"""
        pass

    def get_step_info(self) -> dict[str, Any]:
        """Get step information"""
        return {
            'step_id': self.step_id,
            'step_name': self.step_name,
            'config': self.step_config
        }


class Pipeline:
    """ML pipeline for orchestrating model training and inference"""

    def __init__(self, pipeline_config: dict[str, Any]):
        self.pipeline_config = pipeline_config
        self.pipeline_id = f"PIPELINE-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.steps = []
        self.pipeline_state = {
            'status': 'INITIALIZED',
            'current_step': 0,
            'completed_steps': [],
            'failed_steps': [],
            'start_time': None,
            'end_time': None
        }

    def add_step(self, step: PipelineStep) -> None:
        """Add a step to the pipeline"""
        self.steps.append(step)

    def execute(self, initial_context: dict[str, Any]) -> dict[str, Any]:
        """Execute the pipeline"""

        self.pipeline_state['start_time'] = datetime.now().isoformat()
        self.pipeline_state['status'] = 'RUNNING'

        context = initial_context.copy()
        pipeline_result = {
            'pipeline_id': self.pipeline_id,
            'status': 'RUNNING',
            'steps': [],
            'final_context': None
        }

        for i, step in enumerate(self.steps):
            self.pipeline_state['current_step'] = i

            try:
                step_result = step.execute(context)

                # Merge step result into context
                if 'output' in step_result:
                    context.update(step_result['output'])

                self.pipeline_state['completed_steps'].append(step.step_name)

                pipeline_result['steps'].append({
                    'step_name': step.step_name,
                    'status': 'SUCCESS',
                    'result': step_result
                })

            except Exception as e:
                self.pipeline_state['status'] = 'FAILED'
                self.pipeline_state['failed_steps'].append({
                    'step_name': step.step_name,
                    'error': str(e)
                })

                pipeline_result['steps'].append({
                    'step_name': step.step_name,
                    'status': 'FAILED',
                    'error': str(e)
                })

                pipeline_result['status'] = 'FAILED'
                break

        self.pipeline_state['end_time'] = datetime.now().isoformat()

        if self.pipeline_state['status'] == 'RUNNING':
            self.pipeline_state['status'] = 'COMPLETED'
            pipeline_result['status'] = 'SUCCESS'

        pipeline_result['final_context'] = context
        pipeline_result['pipeline_state'] = self.pipeline_state

        return pipeline_result

    def get_state(self) -> dict[str, Any]:
        """Get current pipeline state"""
        return self.pipeline_state


class PipelineOrchestrator:
    """Orchestrates multiple pipelines"""

    def __init__(self):
        self.pipelines = {}
        self.active_runs = {}

    def register_pipeline(self, pipeline_name: str, pipeline: Pipeline) -> None:
        """Register a pipeline"""
        self.pipelines[pipeline_name] = pipeline

    def execute_pipeline(self, pipeline_name: str, context: dict[str, Any]) -> dict[str, Any]:
        """Execute a registered pipeline"""

        if pipeline_name not in self.pipelines:
            return {
                'status': 'FAILED',
                'error': f'Pipeline {pipeline_name} not found'
            }

        return self.pipelines[pipeline_name].execute(context)

    def get_pipeline_status(self, pipeline_name: str) -> dict[str, Any] | None:
        """Get status of a pipeline"""
        if pipeline_name in self.pipelines:
            return self.pipelines[pipeline_name].get_state()
        return None


# Export module info
__all__ = ['PipelineStep', 'Pipeline', 'PipelineOrchestrator']
