"""
Cost Management Agent
Purpose: Track API and processing costs with $10 cap and alerts
- API cost tracking
- $10 cap with alerts
- Processing cost monitoring
- Budget management
- Cost optimization

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import logging
import smtplib
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from agents.orchestrator import AgentState

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

try:
    from supabase import create_client, Client
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    if SUPABASE_URL and SUPABASE_KEY:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        HAS_SUPABASE = True
    else:
        HAS_SUPABASE = False
        supabase = None
except Exception:
    HAS_SUPABASE = False
    supabase = None

logger = logging.getLogger(__name__)

# Cost configuration
COST_CAP = 10.0  # $10 cap
COST_ALERT_THRESHOLD = 8.0  # Alert at $8
COST_ALERT_EMAIL = os.getenv('COST_ALERT_EMAIL', '')


class CostManagerAgent:
    """
    Cost Management Agent - Tracks and manages API/processing costs
    """
    
    def __init__(self):
        """Initialize cost manager agent"""
        self.name = "cost_manager_agent"
        self.supabase = supabase if HAS_SUPABASE else None
        self.cost_cap = COST_CAP
        self.alert_threshold = COST_ALERT_THRESHOLD
        self.alert_email = COST_ALERT_EMAIL
        logger.info(f"Initialized {self.name} with ${self.cost_cap} cap")
    
    def track_cost(self, cost_type: str, api_name: str, operation: str, 
                   cost_amount: float, metadata: Optional[Dict] = None) -> bool:
        """
        Track a cost.
        
        Args:
            cost_type: Type of cost ('api', 'processing', 'storage', etc.)
            api_name: API name (e.g., 'grok', 'perplexity', 'openai')
            operation: Operation name (e.g., 'chat_completion', 'search')
            cost_amount: Cost amount in USD
            metadata: Additional metadata
            
        Returns:
            True if tracked successfully, False otherwise
        """
        if not self.supabase:
            logger.warning("Supabase not available, cost not tracked")
            return False
        
        try:
            cost_data = {
                'cost_type': cost_type,
                'api_name': api_name,
                'operation': operation,
                'cost_amount': cost_amount,
                'currency': 'USD',
                'metadata': metadata or {},
                'tracked_at': datetime.utcnow().isoformat()
            }
            
            result = self.supabase.table('cost_tracking').insert(cost_data).execute()
            
            if result.data:
                logger.info(f"Tracked cost: ${cost_amount:.4f} for {api_name} {operation}")
                
                # Check if we need to alert
                self.check_and_alert()
                
                return True
            
            return False
        except Exception as e:
            logger.error(f"Error tracking cost: {e}")
            return False
    
    def get_total_cost(self, period: str = 'today') -> float:
        """
        Get total cost for a period.
        
        Args:
            period: Period ('today', 'week', 'month', 'all')
            
        Returns:
            Total cost in USD
        """
        if not self.supabase:
            return 0.0
        
        try:
            # Calculate date range
            now = datetime.utcnow()
            if period == 'today':
                start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            elif period == 'week':
                start_date = now - timedelta(days=7)
            elif period == 'month':
                start_date = now - timedelta(days=30)
            else:  # all
                start_date = datetime(1970, 1, 1)
            
            # Query costs
            result = self.supabase.table('cost_tracking')\
                .select('cost_amount')\
                .gte('tracked_at', start_date.isoformat())\
                .execute()
            
            if result.data:
                total = sum(item.get('cost_amount', 0.0) for item in result.data)
                return total
            
            return 0.0
        except Exception as e:
            logger.error(f"Error getting total cost: {e}")
            return 0.0
    
    def get_cost_by_api(self, period: str = 'today') -> Dict[str, float]:
        """
        Get cost breakdown by API.
        
        Args:
            period: Period ('today', 'week', 'month', 'all')
            
        Returns:
            Dictionary with API costs
        """
        if not self.supabase:
            return {}
        
        try:
            # Calculate date range
            now = datetime.utcnow()
            if period == 'today':
                start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            elif period == 'week':
                start_date = now - timedelta(days=7)
            elif period == 'month':
                start_date = now - timedelta(days=30)
            else:  # all
                start_date = datetime(1970, 1, 1)
            
            # Query costs
            result = self.supabase.table('cost_tracking')\
                .select('api_name', 'cost_amount')\
                .gte('tracked_at', start_date.isoformat())\
                .execute()
            
            if result.data:
                api_costs = {}
                for item in result.data:
                    api_name = item.get('api_name', 'unknown')
                    cost = item.get('cost_amount', 0.0)
                    api_costs[api_name] = api_costs.get(api_name, 0.0) + cost
                return api_costs
            
            return {}
        except Exception as e:
            logger.error(f"Error getting cost by API: {e}")
            return {}
    
    def check_and_alert(self):
        """
        Check cost and send alert if needed.
        """
        total_cost = self.get_total_cost('today')
        
        # Check if we've exceeded the cap
        if total_cost >= self.cost_cap:
            logger.error(f"🚨 COST CAP EXCEEDED: ${total_cost:.2f} >= ${self.cost_cap}")
            self.send_alert(f"Cost cap exceeded: ${total_cost:.2f} >= ${self.cost_cap}")
            return
        
        # Check if we're approaching the threshold
        if total_cost >= self.alert_threshold:
            logger.warning(f"⚠️ COST ALERT: ${total_cost:.2f} >= ${self.alert_threshold}")
            self.send_alert(f"Cost approaching cap: ${total_cost:.2f} / ${self.cost_cap}")
            return
    
    def send_alert(self, message: str):
        """
        Send cost alert.
        
        Args:
            message: Alert message
        """
        if not self.alert_email:
            logger.warning(f"Cost alert (no email configured): {message}")
            return
        
        try:
            # Get cost breakdown
            cost_by_api = self.get_cost_by_api('today')
            total_cost = self.get_total_cost('today')
            
            # Create email
            email_body = f"""
Cost Alert: {message}

Total Cost Today: ${total_cost:.2f}
Cost Cap: ${self.cost_cap}

Cost Breakdown by API:
"""
            for api_name, cost in cost_by_api.items():
                email_body += f"  {api_name}: ${cost:.2f}\n"
            
            email_body += f"\nTime: {datetime.utcnow().isoformat()}\n"
            
            # Send email via SMTP
            smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = int(os.getenv('SMTP_PORT', '587'))
            smtp_user = os.getenv('SMTP_USER', '')
            smtp_password = os.getenv('SMTP_PASSWORD', '')
            
            if smtp_server and smtp_user and smtp_password:
                try:
                    # Create message
                    msg = MIMEMultipart()
                    msg['From'] = smtp_user
                    msg['To'] = self.alert_email
                    msg['Subject'] = f"Gematria Hive Cost Alert: {message}"
                    msg.attach(MIMEText(email_body, 'plain'))
                    
                    # Send email
                    server = smtplib.SMTP(smtp_server, smtp_port)
                    server.starttls()
                    server.login(smtp_user, smtp_password)
                    server.send_message(msg)
                    server.quit()
                    
                    logger.info(f"✅ Cost alert email sent to {self.alert_email}")
                except Exception as e:
                    logger.error(f"Error sending email via SMTP: {e}")
                    logger.info(f"Cost alert (email failed): {message}")
                    logger.info(f"Email body:\n{email_body}")
            else:
                # Fallback: log the alert if SMTP not configured
                logger.info(f"Cost alert (SMTP not configured): {message}")
                logger.info(f"Email body:\n{email_body}")
                logger.info("Configure SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD to enable email alerts")
            
        except Exception as e:
            logger.error(f"Error sending cost alert: {e}")
    
    def can_proceed(self, estimated_cost: float = 0.0) -> Tuple[bool, str]:
        """
        Check if operation can proceed based on cost cap.
        
        Args:
            estimated_cost: Estimated cost for the operation
            
        Returns:
            Tuple of (can_proceed, message)
        """
        total_cost = self.get_total_cost('today')
        
        if total_cost >= self.cost_cap:
            return (False, f"Cost cap exceeded: ${total_cost:.2f} >= ${self.cost_cap}")
        
        if total_cost + estimated_cost >= self.cost_cap:
            return (False, f"Operation would exceed cost cap: ${total_cost + estimated_cost:.2f} >= ${self.cost_cap}")
        
        if total_cost + estimated_cost >= self.alert_threshold:
            return (True, f"Warning: Cost approaching cap: ${total_cost + estimated_cost:.2f} / ${self.cost_cap}")
        
        return (True, f"Cost OK: ${total_cost + estimated_cost:.2f} / ${self.cost_cap}")
    
    def get_cost_summary(self) -> Dict:
        """
        Get cost summary.
        
        Returns:
            Dictionary with cost summary
        """
        total_today = self.get_total_cost('today')
        total_week = self.get_total_cost('week')
        total_month = self.get_total_cost('month')
        cost_by_api = self.get_cost_by_api('today')
        
        return {
            'total_today': total_today,
            'total_week': total_week,
            'total_month': total_month,
            'cost_cap': self.cost_cap,
            'alert_threshold': self.alert_threshold,
            'remaining_budget': self.cost_cap - total_today,
            'cost_by_api': cost_by_api,
            'status': 'ok' if total_today < self.alert_threshold else 'warning' if total_today < self.cost_cap else 'exceeded'
        }
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute cost management task.
        
        Args:
            state: Agent state with cost information
            
        Returns:
            Updated state with cost tracking
        """
        task = state.get("task", {})
        cost_info = task.get("cost_info", {})
        
        if cost_info:
            cost_type = cost_info.get('cost_type', 'api')
            api_name = cost_info.get('api_name', 'unknown')
            operation = cost_info.get('operation', 'unknown')
            cost_amount = cost_info.get('cost_amount', 0.0)
            metadata = cost_info.get('metadata', {})
            
            # Track cost
            self.track_cost(cost_type, api_name, operation, cost_amount, metadata)
        
        # Get cost summary
        cost_summary = self.get_cost_summary()
        
        # Update state
        state["context"]["cost_summary"] = cost_summary
        state["context"]["total_cost_today"] = cost_summary['total_today']
        state["context"]["remaining_budget"] = cost_summary['remaining_budget']
        state["context"]["cost_status"] = cost_summary['status']
        state["results"].append({
            "agent": self.name,
            "action": "track_cost",
            "total_cost_today": cost_summary['total_today'],
            "remaining_budget": cost_summary['remaining_budget'],
            "status": cost_summary['status']
        })
        
        # Check if we can proceed
        can_proceed, message = self.can_proceed()
        if not can_proceed:
            logger.error(f"Cost cap exceeded: {message}")
            state["status"] = "failed"
            state["error"] = message
        
        return state

