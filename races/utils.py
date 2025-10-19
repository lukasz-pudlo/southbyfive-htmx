import logging
import pandas as pd
from races.models import Season, Race, Runner, Result

logger = logging.getLogger(__name__)


def handle_race_file(file, season):
    logger.debug(f"Uploaded the following file: {file}")
    df = pd.read_excel(file)
    # Rename columns to remove spaces; otherwise, when itering over them,
    # the columns names will be replace by _{column index}
    df = df.rename(columns={"First Name": "FirstName", "Last Name": "LastName",
                            "Participant Number": "ParticipantNumner"})
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

        gender_list = list(Runner.GENDER_CHOICES.keys())

        # Create or update runners
        file_runner_rows = []
        for row in df.itertuples():
            file_runner_rows.append(row)
            # logger.debug(f"Index: {row.Index}, Time: {row.Time}")
        # logger.debug(f"file_runner_rows: {file_runner_rows}")
        logger.debug(
            f"One entry from file_runner_rows: {file_runner_rows[0]}")
        logger.debug(
            f"One entry from file_runner_rows: {file_runner_rows[0].FirstName}")

        for runner in file_runner_rows:
            full_name = f"{runner.FirstName} {runner.LastName}"
            gender = list(runner.Category)[0]
            logger.debug(f"gender first letter: {gender}")
            if gender == "N":
                gender = "NB"
            Runner.objects.update_or_create(
                full_name=full_name,
                gender=gender
            )

        # Create results
