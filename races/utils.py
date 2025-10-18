import logging
import pandas as pd
from races.models import Season, Race, Runner, Result

logger = logging.getLogger(__name__)


def handle_race_file(file, season):
    logger.debug(f"Uploaded the following file: {file}")
    df = pd.read_excel(file)
    logger.debug(f"The file {file} has the following contents: \n {df}")
    # For now, when uploading a race file, we will delete the corresponding race if it exists
    season = Season.objects.get(pk=season.pk)
    logger.debug(f"Retrieved the following season from the database: {season}")
    # Retrieve all races from that season
    races = Race.objects.filter(season=season)
    logger.debug(f"Retrieved the following season {season} races: {races}")
    # Retrieve the race corresponding to the file
