import logging
from django.core.management.base import BaseCommand
from letters.services.gam_scraper import GamLetterScraper
from letters.models import SummaryLetter

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Scrape letters from the GAM system and store them in the database."

    def handle(self, *args, **options):
        self.stdout.write("Starting GAM letter scraping...")
        try:
            scraper = GamLetterScraper()
            letters = scraper.run()

            for letter in letters:
                SummaryLetter.objects.get_or_create(
                    letter_id=letter["letter_id"],
                    defaults={
                        "sender": letter["sender"],
                        "receiver": letter["receiver"],
                        "sent_time": letter["time_sent"],
                        "subject": letter["subject"],
                    }
                )
            self.stdout.write(self.style.SUCCESS(f"Successfully scraped and saved {len(letters)} letters."))
        except Exception as e:
            logger.exception("Failed to scrape GAM letters.")
            self.stderr.write(self.style.ERROR(f"Error: {e}"))
