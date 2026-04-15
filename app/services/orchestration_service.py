import uuid
import asyncio
import logging
from sqlmodel import Session, select
from app.core.database import SessionLocal
from app.models.schemas import Worker, Policy, EventLog
from app.services.eligibility_service import EligibilityService
from app.services.claims import ClaimService
from app.services.trigger_service import TriggerService

logger = logging.getLogger(__name__)

class OrchestrationEngine:
    """
    The central coordination engine for autonomous insurance execution.
    Implements a production-grade, event-driven pipeline.
    """
    
    @staticmethod
    async def run_automation_cycle(session: Session, event_data: dict):
        """
        Executes the full insurance lifecycle for a single disruption event.
        Trigger -> Event -> Eligibility -> Claim -> Fraud -> Payout -> Ledger -> Notify
        """
        event_type = event_data.get("type", "GENERAL")
        event_id = event_data.get("id", str(uuid.uuid4()))
        
        logger.info(f"[ORCHESTRATOR] Starting cycle for event {event_id} ({event_type})")
        
        # Log the event
        event_log = EventLog(
            event_id=event_id,
            event_type=event_type,
            status="STARTED",
            details=f"Automation cycle started for {event_type}"
        )
        session.add(event_log)
        session.commit()

        try:
            # 1. Fetch potential workers (In production, filter by Zone/Location)
            workers = session.exec(select(Worker).where(Worker.is_active == True)).all()
            impacted_count = 0
            
            for worker in workers:
                # 2. Check Eligibility (Multi-step: opt-in, activity, etc.)
                eligibility = EligibilityService.check_eligibility(session, worker.id)
                if not eligibility["eligible"]:
                    logger.debug(f"[ORCHESTRATOR] Worker {worker.id} not eligible: {eligibility.get('reason')}")
                    continue
                    
                # 3. Process Auto-Claim (Integrated Risk + Fraud + Payout + Ledger + Notification)
                # We decouple the claim processing to ensure one worker's failure doesn't stop the cycle
                try:
                    claim = ClaimService.process_auto_claim(
                        session, 
                        worker.id, 
                        event_type, 
                        amount=500.0 # Standard disruption payout
                    )
                    if claim and claim.status == "APPROVED":
                        impacted_count += 1
                except Exception as e:
                    logger.error(f"[ORCHESTRATOR] Error processing claim for worker {worker.id}: {str(e)}")
                    continue
            
            # Update event log
            event_log.status = "COMPLETED"
            event_log.details = f"Automation cycle finished. Impacted workers: {impacted_count}"
            session.add(event_log)
            session.commit()
            
            logger.info(f"[ORCHESTRATOR] Cycle {event_id} complete. Impacted: {impacted_count}")
            return impacted_count

        except Exception as e:
            logger.error(f"[ORCHESTRATOR CRITICAL] Cycle {event_id} failed: {str(e)}")
            event_log.status = "FAILED"
            event_log.details = f"Error: {str(e)}"
            session.add(event_log)
            session.commit()
            raise e

    @staticmethod
    async def background_monitor():
        """
        The continuous background process that polls for disruptions.
        Includes exponential backoff and robust connection handling.
        """
        logger.info("[ORCHESTRATOR] Autonomous monitoring started...")
        retry_delay = 5
        
        while True:
            try:
                with SessionLocal() as session:
                    # 1. Poll for disruptions (Simulated/Real Weather & Platform)
                    disruption = await TriggerService.check_weather_disruption(0.0, 0.0)
                    
                    if disruption:
                        logger.info(f"[ORCHESTRATOR] Real-time disruption detected: {disruption['type']}")
                        await OrchestrationEngine.run_automation_cycle(session, disruption)
                
                # Reset retry delay on success
                retry_delay = 5
                # Poll interval (simulated production: 60s)
                await asyncio.sleep(60)
                
            except Exception as e:
                logger.error(f"[ORCHESTRATOR MONITOR ERROR] {str(e)}. Retrying in {retry_delay}s...")
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 300) # Exponential backoff up to 5 mins
