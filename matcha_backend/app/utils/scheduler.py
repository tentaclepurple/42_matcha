# app/utils/scheduler.py
from flask_apscheduler import APScheduler
from datetime import datetime, timedelta
from ..models.user import UserModel
from ..config.database import mongo


scheduler = APScheduler()


def init_scheduler(app):
    """Inicializa y configura el scheduler"""
    # Configuración del scheduler
    app.config['SCHEDULER_API_ENABLED'] = True
    app.config['SCHEDULER_TIMEZONE'] = "UTC"
    
    scheduler.init_app(app)
    
    configure_scheduled_tasks()
    
    scheduler.start()


def configure_scheduled_tasks():
    scheduler.add_job(
        id='check_inactive_users',
        func=check_inactive_users,
        trigger='interval',
        seconds=10
    )


def check_inactive_users():
    try:
        inactive_threshold = datetime.utcnow() - timedelta(seconds=10)
        
        # Search for users that are online and have been inactive for more than the threshold
        result = mongo.db.users.update_many(
            {
                "online": True,
                "verified": True,
                "last_connection": {"$lt": inactive_threshold}
            },
            {
                "$set": {"online": False}
            }
        )

    except Exception as e:
        print(f"Error checking inactive users: {str(e)}", flush=True)