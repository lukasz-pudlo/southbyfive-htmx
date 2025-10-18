import logging
import pandas as pd
from races.models import Season, Race, Runner, Result

logger = logging.getLogger(__name__)


def handle_race_file(file, season):
    logger.debug(f"Uploaded the following file: {file}")
    df = pd.read_excel(file)
    logger.debug(f"The file {file} has the following contents: \n {df}")
    season = Season.objects.get(pk=season.pk)
    logger.debug(f"Retrieved the following season from the database: {season}")
    # Retrieve all races from that season
    races = Race.objects.filter(season=season)
    logger.debug(f"Retrieved the following season {season} races: {races}")
    # Retrieve the race corresponding to the file
    race_name = str(file).split('.')[0]
    logger.debug(f"Variable race_name: {race_name}")

    # Always delete all races, and results in the current season when uploading.
    # Uploads will always have to start with King's Park.
    # Runners don't have to be deleted, as they only hold immutable data. They can be updated,
    # for example, when there has been a name or club correction.
    if race_name == 'kings':
        Race.objects.filter(season=season).delete()
    # For now, let's assume that the user knows to upload the races in the following order:
    # kings, linn, rouken, pollok, bellahouston, queens

        # Create King's Park race
        logger.debug(f"Creating the {race_name} race for season {season}")
        race_object = Race.objects.create(
            park='KP',
            season=season
        )

        for row in df.itertuples():
            logger.debug(f"Index: {row.Index}, Time: {row.Time}")

    # Create or updated runners

    # Create results
