"""
GL20-29: Data Science / Data Access Layer
GL20: Data Ingestion Module - Data Pipeline
"""

from collections.abc import Callable
from datetime import datetime
from typing import Any


class DataPipeline:
    """Orchestrates data ingestion and processing pipeline"""

    def __init__(self, pipeline_config: dict[str, Any]):
        self.pipeline_config = pipeline_config
        self.pipeline_id = f"PIPELINE-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.steps = []
        self.metrics = {
            'records_processed': 0,
            'records_failed': 0,
            'start_time': None,
            'end_time': None
        }

    def add_step(self, step: Callable, step_name: str) -> None:
        """Add a processing step to the pipeline"""
        self.steps.append({
            'name': step_name,
            'function': step,
            'status': 'PENDING'
        })

    def execute(self, ingestor: DataIngestor) -> dict[str, Any]:
        """Execute the data pipeline"""

        self.metrics['start_time'] = datetime.now().isoformat()
        pipeline_result = {
            'pipeline_id': self.pipeline_id,
            'status': 'RUNNING',
            'steps_completed': [],
            'steps_failed': [],
            'final_status': None
        }

        try:
            # Ingest data
            ingestion_result = ingestor.ingest()

            if ingestion_result['status'] != 'SUCCESS':
                pipeline_result['status'] = 'FAILED'
                pipeline_result['final_status'] = 'INGESTION_FAILED'
                return pipeline_result

            self.metrics['records_processed'] = ingestion_result.get('record_count', 0)

            # Execute pipeline steps
            for step in self.steps:
                try:
                    step['function'](ingestor.ingestion_metadata)
                    step['status'] = 'COMPLETED'
                    pipeline_result['steps_completed'].append(step['name'])
                except Exception as e:
                    step['status'] = 'FAILED'
                    step['error'] = str(e)
                    pipeline_result['steps_failed'].append({
                        'step': step['name'],
                        'error': str(e)
                    })

            self.metrics['end_time'] = datetime.now().isoformat()

            # Determine final status
            if pipeline_result['steps_failed']:
                pipeline_result['status'] = 'PARTIAL_SUCCESS'
                pipeline_result['final_status'] = 'SOME_STEPS_FAILED'
            else:
                pipeline_result['status'] = 'SUCCESS'
                pipeline_result['final_status'] = 'COMPLETED'

        except Exception as e:
            pipeline_result['status'] = 'FAILED'
            pipeline_result['error'] = str(e)
            pipeline_result['final_status'] = 'PIPELINE_ERROR'

        return pipeline_result


class IngestionOrchestrator:
    """Orchestrates multiple ingestion pipelines"""

    def __init__(self):
        self.pipelines = {}
        self.active_jobs = {}

    def register_pipeline(self, pipeline_name: str, pipeline: DataPipeline) -> None:
        """Register a pipeline"""
        self.pipelines[pipeline_name] = pipeline

    def execute_pipeline(self, pipeline_name: str, ingestor: DataIngestor) -> dict[str, Any]:
        """Execute a registered pipeline"""

        if pipeline_name not in self.pipelines:
            return {
                'status': 'FAILED',
                'error': f'Pipeline {pipeline_name} not found'
            }

        return self.pipelines[pipeline_name].execute(ingestor)

    def get_pipeline_status(self, pipeline_name: str) -> dict[str, Any] | None:
        """Get status of a pipeline"""
        return self.pipelines.get(pipeline_name)


# Export module info
__all__ = ['DataPipeline', 'IngestionOrchestrator']
