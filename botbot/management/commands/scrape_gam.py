from django.core.management.base import BaseCommand
from botbot.views import GamScraper
from botbot.models import GamUser
from concurrent.futures import ThreadPoolExecutor
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Scrape GAM letters for all active users'

    def handle(self, *args, **options):
        users = GamUser.objects.filter(is_active=True)
        scraper = GamScraper()

        with ThreadPoolExecutor(max_workers=3) as executor:
            results = list(executor.map(
                lambda user: scraper.scrape_user_letters(
                    user.username,
                    user.password,
                    user.id
                ),
                users
            ))

        logger.info(f"Scraping completed. Results: {results}")