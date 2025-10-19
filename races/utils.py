import logging
import pandas as pd
from races.models import Season, Race, Runner, Result

logger = logging.getLogger(__name__)


def add_runners(df, runners):
    """
    Takes a Pandas dataframe and a list containing tuples 
    with runner data to create a Runner object
    """
    logger.debug(f"runners at the start of add_runners(): {runners}")
    gender_list = list(Runner.GENDER_CHOICES.keys())

    runner_objects = []

    # Create or update runners
    for runner in runners:
        gender = list(runner.Category)[0]
        logger.debug(f"gender first letter: {gender}")
        if gender == "N":
            gender = "NB"
        runner_object, created = Runner.objects.update_or_create(
            first_name=runner.FirstName,
            last_name=runner.LastName,
            gender=gender,
            participant_number=runner.ParticipantNumber,
            category=runner.Category,
            club=runner.Club
        )
        # Pass time result to runner_object so that it's accessible in add_results()
        runner_objects.append({
            'runner_object': runner_object,
            'time': runner.Time
        })
    logger.debug(f"runners after add_runners(): {runners}")
    return runner_objects


def add_results(runner_objects, race_object, file_runner_rows):
    logger.debug(f"race_object in add_results(): {race_object}")
    logger.debug(f"pk of race_object: {race_object.pk}")
    logger.debug(f"file_runner_rows in add_results(): {file_runner_rows}")
    try:
        results = Result.objects.get(race=race_object)
    except Result.DoesNotExist:
        results = None
    if results:
        logger.debug(f"results in add_results(): {results}")
        logger.debug(f"Deleting results from race {race_object}")
        results.delete()

    for runner in runner_objects:
        logger.debug(f"Runner in add_results(): {runner}")
        runner_object = Runner.objects.get(pk=runner["runner_object"].pk)
        logger.debug(f"runner_object in add_results(): {runner_object}")
        time = runner["time"]
        if time == "DNF":
            time = None
        Result.objects.create(
            race=race_object,
            runner=runner_object,
            time=time
        )


def handle_race_file(file, season):
    logger.debug(f"Uploaded the following file: {file}")
    df = pd.read_excel(file)
    # Rename columns to remove spaces; otherwise, when itering over them,
    # the columns names will be replace by _{column index}
    df = df.rename(columns={"First Name": "FirstName", "Last Name": "LastName",
                            "Participant Number": "ParticipantNumber"})
    logger.debug(f"The file {file} has the following contents: \n {df}")
    season = Season.objects.get(pk=season.pk)
    logger.debug(f"Retrieved the following season from the database: {season}")
    # Retrieve all races from that season
    races = Race.objects.filter(season=season)
    logger.debug(f"Retrieved the following season {season} races: {races}")
    # Retrieve the race corresponding to the file
    race_name = str(file).split('.')[0]
    logger.debug(f"Variable race_name: {race_name}")

    file_runner_rows = []
    for row in df.itertuples():
        file_runner_rows.append(row)
        # logger.debug(f"Index: {row.Index}, Time: {row.Time}")
    logger.debug(f"file_runner_rows: {file_runner_rows}")
    logger.debug(
        f"One entry from file_runner_rows: {file_runner_rows[0]}")
    logger.debug(
        f"One entry from file_runner_rows: {file_runner_rows[0].FirstName}")

    # Always delete all races, and results in the current season when uploading.
    # Uploads will always have to start with King's Park.
    # Runners don't have to be deleted, as they only hold immutable data. They can be updated,
    # for example, when there has been a name or club correction.
    if race_name == 'kings':
        try:
            logger.debug(f"About to delete all races for season {season}")
            race_delete_result = Race.objects.filter(season=season).delete()
            logger.debug(f"Deleted races. Result: {race_delete_result}")
        except Exception as e:
            logger.error(f"Error deleting races: {e}")
            raise
        # For now, let's assume that the user knows to upload the races in the following order:
        # kings, linn, rouken, pollok, bellahouston, queens

        # While developing this feature, remove all runners each time King's Park is uplaoded
        try:
            logger.debug(f"About to delete all runners")
            runners = Runner.objects.all()
            logger.debug(f"Found {runners.count()} runners to delete")
            delete_result = runners.delete()
            logger.debug(f"Deleted all runners. Result: {delete_result}")
        except Exception as e:
            logger.error(f"Error deleting runners: {e}")
            raise

        # Create King's Park race
        logger.debug(f"Creating the {race_name} race for season {season}")
        race_object = Race.objects.create(
            park='KP',
            season=season
        )

        runner_objects = add_runners(df, file_runner_rows)

        # Create results
        logger.debug(
            f"race_object before calling add_results(): {race_object}")
        add_results(runner_objects, race_object, file_runner_rows)
    else:
        park = ""
        match race_name:
            case "linn":
                park = "LP"
            case "rouken":
                park = "RG"
            case "pollok":
                park = "PP"
            case "bellahouston":
                park = "BP"
            case "queens":
                park = "QP"
        race_object, created = Race.objects.update_or_create(
            park=park,
            season=season
        )

        runner_objects = add_runners(df, file_runner_rows)

        # Create results
        logger.debug(
            f"race_object before calling add_results(): {race_object}")
        add_results(runner_objects, race_object, file_runner_rows)
