"""
Unit tests for Disaster Recovery Manager
"""

import pytest
import asyncio
from datetime import datetime, timedelta

import sys
sys.path.insert(0, '/workspace/machine-native-ops')

from adk.plugins.deployment.infrastructure.disaster_recovery import (
    DisasterRecoveryManager,
    DisasterRecoveryConfig,
    BackupConfig,
    FailoverConfig,
    RecoveryPointObjective,
    RecoveryTimeObjective,
    BackupResult,
    FailoverResult,
    RestoreResult,
    DisasterType,
    BackupType as DRBackupType,
    FailoverStrategy,
    RecoveryTier
)


class TestDisasterRecoveryConfig:
    """Test DisasterRecoveryConfig dataclass"""
    
    def test_default_config(self):
        """Test default configuration"""
        config = DisasterRecoveryConfig()
        
        assert config.recovery_tier == RecoveryTier.TIER_3
        assert config.rpo.target_rpo_minutes == 60
        assert config.rto.target_rto_minutes == 240
        assert config.backup.enabled is True
        assert config.failover.enabled is True
        assert config.testing_enabled is True
    
    def test_custom_config(self):
        """Test custom configuration"""
        config = DisasterRecoveryConfig(
            recovery_tier=RecoveryTier.TIER_1,
            rpo=RecoveryPointObjective(target_rpo_minutes=5),
            rto=RecoveryTimeObjective(target_rto_minutes=15),
            backup=BackupConfig(retention_days=90),
            failover=FailoverConfig(auto_failover=True)
        )
        
        assert config.recovery_tier == RecoveryTier.TIER_1
        assert config.rpo.target_rpo_minutes == 5
        assert config.rto.target_rto_minutes == 15
        assert config.backup.retention_days == 90


class TestBackupResult:
    """Test BackupResult dataclass"""
    
    def test_backup_result_creation(self):
        """Test creating backup result"""
        start = datetime.now()
        end = start + timedelta(minutes=5)
        
        result = BackupResult(
            success=True,
            backup_id="backup-20240101",
            backup_type=DRBackupType.FULL,
            start_time=start,
            end_time=end,
            duration_seconds=300,
            size_bytes=1024000,
            location="s3://backups/backup-20240101",
            checksum="abc123"
        )
        
        assert result.success is True
        assert result.backup_id == "backup-20240101"
        assert result.duration_seconds == 300
        assert result.size_bytes == 1024000


class TestDisasterRecoveryManager:
    """Test DisasterRecoveryManager class"""
    
    @pytest.fixture
    def config(self):
        """Create test configuration"""
        return DisasterRecoveryConfig()
    
    @pytest.fixture
    def manager(self, config):
        """Create disaster recovery manager instance"""
        return DisasterRecoveryManager(config)
    
    def test_manager_initialization(self, manager):
        """Test manager initialization"""
        assert manager.config is not None
        assert manager._backups == {}
        assert manager._failovers == {}
        assert manager._restores == {}
        assert manager._health_status == {}
        assert manager._active_region == manager.config.failover.primary_region
    
    @pytest.mark.asyncio
    async def test_create_backup(self, manager):
        """Test creating backup"""
        result = await manager.create_backup(DRBackupType.FULL)
        
        assert isinstance(result, BackupResult)
        assert result.success is True
        assert result.backup_id.startswith("backup-")
        assert result.duration_seconds > 0
        assert result.size_bytes > 0
        assert result.checksum is not None
    
    @pytest.mark.asyncio
    async def test_create_backup_disabled(self):
        """Test creating backup when disabled"""
        config = DisasterRecoveryConfig(
            backup=BackupConfig(enabled=False)
        )
        manager = DisasterRecoveryManager(config)
        
        result = await manager.create_backup()
        
        assert result.success is False
        assert len(result.errors) > 0
        assert "not enabled" in result.errors[0].lower()
    
    @pytest.mark.asyncio
    async def test_create_incremental_backup(self, manager):
        """Test creating incremental backup"""
        result = await manager.create_backup(DRBackupType.INCREMENTAL)
        
        assert result.success is True
        assert result.backup_type == DRBackupType.INCREMENTAL
    
    @pytest.mark.asyncio
    async def test_create_snapshot_backup(self, manager):
        """Test creating snapshot backup"""
        result = await manager.create_backup(DRBackupType.SNAPSHOT)
        
        assert result.success is True
        assert result.backup_type == DRBackupType.SNAPSHOT
    
    @pytest.mark.asyncio
    async def test_restore_backup(self, manager):
        """Test restoring from backup"""
        # First create backup
        backup_result = await manager.create_backup(DRBackupType.FULL)
        
        # Then restore
        restore_result = await manager.restore_backup(backup_result.backup_id)
        
        assert isinstance(restore_result, RestoreResult)
        assert restore_result.success is True
        assert restore_result.restore_id.startswith("restore-")
        assert restore_result.backup_id == backup_result.backup_id
    
    @pytest.mark.asyncio
    async def test_restore_nonexistent_backup(self, manager):
        """Test restoring nonexistent backup"""
        result = await manager.restore_backup("nonexistent-backup-id")
        
        assert result.success is False
        assert len(result.errors) > 0
        assert "not found" in result.errors[0].lower()
    
    @pytest.mark.asyncio
    async def test_restore_validate_only(self, manager):
        """Test restore with validate_only=True"""
        # Create backup
        backup_result = await manager.create_backup(DRBackupType.FULL)
        
        # Validate only
        restore_result = await manager.restore_backup(
            backup_result.backup_id,
            validate_only=True
        )
        
        assert restore_result.success is True
        # No items should be restored in validate-only mode
        assert restore_result.items_restored == 0
    
    @pytest.mark.asyncio
    async def test_initiate_failover(self, manager):
        """Test initiating failover"""
        result = await manager.initiate_failover(trigger_type="manual")
        
        assert isinstance(result, FailoverResult)
        assert result.success is True
        assert result.failover_id.startswith("failover-")
        assert result.from_region == manager.config.failover.primary_region
        assert result.to_region == manager.config.failover.secondary_region
        assert len(result.services_affected) > 0
    
    @pytest.mark.asyncio
    async def test_initiate_failover_disabled(self):
        """Test failover when disabled"""
        config = DisasterRecoveryConfig(
            failover=FailoverConfig(enabled=False)
        )
        manager = DisasterRecoveryManager(config)
        
        result = await manager.initiate_failover()
        
        assert result.success is False
        assert len(result.errors) > 0
        assert "not enabled" in result.errors[0].lower()
    
    @pytest.mark.asyncio
    async def test_initiate_failover_to_custom_region(self, manager):
        """Test failover to custom region"""
        target_region = "eu-west-1"
        result = await manager.initiate_failover(target_region=target_region)
        
        assert result.success is True
        assert result.to_region == target_region
    
    @pytest.mark.asyncio
    async def test_initiate_failback(self, manager):
        """Test initiating failback"""
        # First failover
        await manager.initiate_failover(trigger_type="manual")
        
        # Then failback
        result = await manager.initiate_failback(trigger_type="manual")
        
        assert isinstance(result, FailoverResult)
        assert result.success is True
        assert result.failover_id.startswith("failback-")
        assert result.to_region == manager.config.failover.primary_region
    
    @pytest.mark.asyncio
    async def test_failback_when_not_failed_over(self, manager):
        """Test failback when not failed over"""
        result = await manager.initiate_failback()
        
        # Should succeed as we're already in primary region
        assert result.success is True
    
    @pytest.mark.asyncio
    async def test_run_dr_drill(self, manager):
        """Test running disaster recovery drill"""
        result = await manager.run_dr_drill(
            drill_type="full",
            test_failover=True,
            test_restore=True
        )
        
        assert isinstance(result, dict)
        assert result["drill_type"] == "full"
        assert result["test_failover"] is True
        assert result["test_restore"] is True
        assert "results" in result
        assert "backup" in result["results"]
    
    @pytest.mark.asyncio
    async def test_run_dr_drill_simulation(self, manager):
        """Test DR drill simulation"""
        result = await manager.run_dr_drill(
            drill_type="simulation",
            test_failover=False,
            test_restore=False
        )
        
        assert result["drill_type"] == "simulation"
        assert result["test_failover"] is False
        assert result["test_restore"] is False
    
    @pytest.mark.asyncio
    async def test_get_statistics(self, manager):
        """Test getting DR statistics"""
        # Create some backups
        await manager.create_backup(DRBackupType.FULL)
        await manager.create_backup(DRBackupType.INCREMENTAL)
        
        # Get statistics
        stats = await manager.get_statistics()
        
        assert stats["active_region"] == manager.config.failover.primary_region
        assert stats["total_backups"] >= 2
        assert stats["backup_enabled"] is True
        assert stats["failover_enabled"] is True
        assert stats["testing_enabled"] is True
    
    @pytest.mark.asyncio
    async def test_generate_compliance_report(self, manager):
        """Test generating compliance report"""
        # Create some data
        await manager.create_backup(DRBackupType.FULL)
        
        # Generate report
        report = await manager.generate_compliance_report()
        
        assert isinstance(report, dict)
        assert "generated_at" in report
        assert "recovery_tier" in report
        assert "rpo_target_minutes" in report
        assert "rto_target_minutes" in report
        assert "total_backups" in report
        assert "compliance_status" in report
    
    def test_calculate_checksum(self, manager):
        """Test checksum calculation"""
        data1 = {"key": "value"}
        data2 = {"key": "value"}
        data3 = {"key": "different"}
        
        checksum1 = manager._calculate_checksum(data1)
        checksum2 = manager._calculate_checksum(data2)
        checksum3 = manager._calculate_checksum(data3)
        
        assert checksum1 == checksum2
        assert checksum1 != checksum3
    
    @pytest.mark.asyncio
    async def test_determine_backup_scope(self, manager):
        """Test determining backup scope"""
        scope = await manager._determine_backup_scope(DRBackupType.FULL)
        
        assert scope["type"] == "full"
        assert scope["include_databases"] is True
        assert scope["include_configurations"] is True
    
    @pytest.mark.asyncio
    async def test_replicate_backup(self, manager):
        """Test backup replication"""
        # Create backup
        backup_result = await manager.create_backup(DRBackupType.FULL)
        
        # Replicate
        await manager._replicate_backup(backup_result.backup_id, backup_result.location)
        
        # Verify replication happened
        # This is a mock test, so we just verify it doesn't error
        assert True
    
    @pytest.mark.asyncio
    async def test_validate_backup(self, manager):
        """Test backup validation"""
        # Create backup
        backup_result = await manager.create_backup(DRBackupType.FULL)
        
        # Validate
        result = await manager._validate_backup(backup_result.backup_id)
        
        assert result["success"] is True
        assert "warnings" in result
    
    @pytest.mark.asyncio
    async def test_multiple_backups_and_restores(self, manager):
        """Test creating multiple backups and restores"""
        # Create multiple backups
        backup1 = await manager.create_backup(DRBackupType.FULL)
        await asyncio.sleep(0.1)
        backup2 = await manager.create_backup(DRBackupType.INCREMENTAL)
        await asyncio.sleep(0.1)
        backup3 = await manager.create_backup(DRBackupType.INCREMENTAL)
        
        # Restore from each
        restore1 = await manager.restore_backup(backup1.backup_id)
        restore2 = await manager.restore_backup(backup2.backup_id)
        restore3 = await manager.restore_backup(backup3.backup_id)
        
        assert all([restore1.success, restore2.success, restore3.success])
        assert len(manager._backups) == 3
        assert len(manager._restores) == 3
    
    @pytest.mark.asyncio
    async def test_failover_failback_cycle(self, manager):
        """Test complete failover-failback cycle"""
        # Initial state
        initial_region = manager._active_region
        assert initial_region == manager.config.failover.primary_region
        
        # Failover
        failover_result = await manager.initiate_failover(trigger_type="manual")
        assert failover_result.success is True
        assert manager._active_region == manager.config.failover.secondary_region
        
        # Failback
        failback_result = await manager.initiate_failback(trigger_type="manual")
        assert failback_result.success is True
        assert manager._active_region == manager.config.failover.primary_region


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])