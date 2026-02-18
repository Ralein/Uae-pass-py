from app.models.schemas.risk import AuthContext, RiskScore, RiskAction
from app.core.redis import redis_client

class RiskService:
    async def assess_risk(self, context: AuthContext) -> RiskScore:
        score = 0
        factors = []

        # 1. IP Reputation / New IP Check
        # Key: "user:{id}:known_ips" (Set)
        if context.user_id:
            is_known_ip = await redis_client.sismember(f"user:{context.user_id}:known_ips", context.ip_address)
            if not is_known_ip:
                score += 30
                factors.append("new_ip")
        
        # 2. Velocity Check (Global or Per User)
        # Key: "risk:velocity:{ip}"
        velocity_key = f"risk:velocity:{context.ip_address}"
        attempts = await redis_client.incr(velocity_key)
        if attempts == 1:
            await redis_client.expire(velocity_key, 3600) # 1 hour
        
        if attempts > 100: # High velocity
            score += 50
            factors.append("high_velocity")
        elif attempts > 20:
            score += 10
            factors.append("medium_velocity")

        # 3. Determine Action
        action = RiskAction.ALLOW
        if score > 80:
            action = RiskAction.BLOCK
        elif score > 40:
            action = RiskAction.STEP_UP
            
        # Post-process: Add IP to known list if success (This usually happens after successful auth, not during assess)
        # We'll expose a separate method for 'record_success'
            
        return RiskScore(total_score=score, action=action, factors=factors)

    async def record_success(self, context: AuthContext):
        if context.user_id:
            await redis_client.sadd(f"user:{context.user_id}:known_ips", context.ip_address)
