from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from datetime import datetime
import asyncio

from app.services.like_service import LikeService
from app.models.database import SessionLocal

# 设置日志
logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

# 运行异步任务的辅助函数
def run_async(coro):
    asyncio.create_task(coro)

async def recalculate_all_user_likes():
    """
    重新计算所有用户的获赞总数
    """
    logger.info(f"开始执行定时任务：重新计算所有用户的获赞总数 - {datetime.now()}")
    db = SessionLocal()
    
    try:
        like_service = LikeService(db)
        result = await like_service.recalculate_user_likes()
        logger.info(f"定时任务执行结果：{result}")
    except Exception as e:
        logger.error(f"定时任务执行失败：{str(e)}")
    finally:
        db.close()
    
    logger.info(f"定时任务执行完成：重新计算所有用户的获赞总数 - {datetime.now()}")

def setup_scheduler():
    """
    设置并启动定时任务调度器
    """
    # 添加定时任务：每天凌晨3点重新计算所有用户的获赞总数
    scheduler.add_job(
        lambda: asyncio.run(recalculate_all_user_likes()),
        trigger=CronTrigger(hour=3, minute=0),  # 每天凌晨3点
        id="recalculate_likes",
        replace_existing=True
    )
    
    # 启动调度器
    scheduler.start()
    logger.info("定时任务调度器已启动")

def shutdown_scheduler():
    """
    关闭定时任务调度器
    """
    scheduler.shutdown()
    logger.info("定时任务调度器已关闭") 