import pytest
from app.services.risk_service import RiskService, RiskAction
from app.models.schemas.risk import AuthContext

@pytest.mark.asyncio
async def test_risk_scoring():
    service = RiskService()
    ctx = AuthContext(
        ip_address="1.2.3.4", 
        user_agent="TestAgent", 
        fingerprint="fp1",
        user_id="user_risk_test"
    )
    
    # First attempt: New IP -> Medium Risk
    score = await service.assess_risk(ctx)
    assert score.total_score >= 30
    assert "new_ip" in score.factors
    
    # Record Success (Learn IP)
    await service.record_success(ctx)
    
    # Second attempt: Known IP -> Low Risk
    score2 = await service.assess_risk(ctx)
    assert "new_ip" not in score2.factors
    
@pytest.mark.asyncio
async def test_risk_velocity():
    service = RiskService()
    ctx = AuthContext(
        ip_address="10.0.0.1", 
        user_agent="Bot", 
        fingerprint="fp_bot",
        user_id="bot_user"
    )
    
    # Spam calls
    for _ in range(30):
        await service.assess_risk(ctx)
        
    # Should be elevated velocity
    score = await service.assess_risk(ctx)
    assert "medium_velocity" in score.factors or "high_velocity" in score.factors
