"""
GL40-49: Algorithm Layer
GL42: Feature Engineering Module - Base Feature Engineering
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


class BaseFeatureExtractor(ABC):
    """Base class for feature extraction"""

    def __init__(self, feature_config: dict[str, Any]):
        self.feature_config = feature_config
        self.feature_metadata = {
            'extractor_id': f"FE-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'feature_type': feature_config.get('feature_type', 'unknown'),
            'created_at': datetime.now().isoformat()
        }

    @abstractmethod
    def extract(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Extract features from raw data"""
        pass

    @abstractmethod
    def validate(self, features: dict[str, Any]) -> bool:
        """Validate extracted features"""
        pass

    def transform(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Transform raw data to features"""

        try:
            features = self.extract(raw_data)

            if not self.validate(features):
                raise ValueError("Feature validation failed")

            return features

        except Exception as e:
            raise Exception(f"Feature transformation failed: {e}")


class NumericalFeatureExtractor(BaseFeatureExtractor):
    """Extract numerical features"""

    def extract(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Extract numerical features"""

        features = {}

        for key, value in raw_data.items():
            if isinstance(value, (int, float)):
                features[f"num_{key}"] = value

        # Add statistical features
        numerical_values = [v for v in raw_data.values() if isinstance(v, (int, float))]
        if numerical_values:
            features['num_mean'] = sum(numerical_values) / len(numerical_values)
            features['num_sum'] = sum(numerical_values)
            features['num_count'] = len(numerical_values)

        return features

    def validate(self, features: dict[str, Any]) -> bool:
        """Validate numerical features"""
        return all(isinstance(v, (int, float)) for v in features.values())


class CategoricalFeatureExtractor(BaseFeatureExtractor):
    """Extract categorical features"""

    def __init__(self, feature_config: dict[str, Any]):
        super().__init__(feature_config)
        self.categories = feature_config.get('categories', {})

    def extract(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Extract categorical features"""

        features = {}

        for key, value in raw_data.items():
            if key in self.categories:
                # One-hot encoding
                category_value = str(value)
                features[f"cat_{key}_{category_value}"] = 1

        return features

    def validate(self, features: dict[str, Any]) -> bool:
        """Validate categorical features"""
        return all(v in [0, 1] for v in features.values())


class FeatureStore:
    """Store and manage features"""

    def __init__(self):
        self.features = {}
        self.feature_groups = {}

    def store_features(self, feature_id: str, features: dict[str, Any]) -> None:
        """Store features"""
        self.features[feature_id] = {
            'features': features,
            'stored_at': datetime.now().isoformat()
        }

    def get_features(self, feature_id: str) -> dict[str, Any] | None:
        """Get stored features"""
        return self.features.get(feature_id)

    def create_feature_group(self, group_name: str, feature_ids: list[str]) -> None:
        """Create a feature group"""
        self.feature_groups[group_name] = {
            'feature_ids': feature_ids,
            'created_at': datetime.now().isoformat()
        }

    def get_feature_group(self, group_name: str) -> dict[str, Any] | None:
        """Get feature group"""
        if group_name in self.feature_groups:
            group = self.feature_groups[group_name]
            features = {}

            for feature_id in group['feature_ids']:
                if feature_id in self.features:
                    features.update(self.features[feature_id]['features'])

            return {
                'group_name': group_name,
                'features': features,
                'feature_count': len(features)
            }

        return None


class FeaturePipeline:
    """Orchestrates feature engineering pipeline"""

    def __init__(self, pipeline_config: dict[str, Any]):
        self.pipeline_config = pipeline_config
        self.pipeline_id = f"FE-PIPELINE-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.extractors = []

    def add_extractor(self, extractor: BaseFeatureExtractor) -> None:
        """Add a feature extractor"""
        self.extractors.append(extractor)

    def execute(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Execute feature engineering pipeline"""

        all_features = {}

        for extractor in self.extractors:
            try:
                features = extractor.transform(raw_data)
                all_features.update(features)
            except Exception as e:
                raise Exception(f"Extractor {extractor.__class__.__name__} failed: {e}")

        return {
            'pipeline_id': self.pipeline_id,
            'status': 'SUCCESS',
            'features': all_features,
            'feature_count': len(all_features)
        }


# Export module info
__all__ = [
    'BaseFeatureExtractor',
    'NumericalFeatureExtractor',
    'CategoricalFeatureExtractor',
    'FeatureStore',
    'FeaturePipeline'
]
