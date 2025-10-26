import logging
import pandas as pd
from races.models import RaceFile, Season, Race, Runner, Result, Classification, ClassificationResult
from datetime import timedelta
from pathlib import Path

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

    result_objects = []
    for runner in runner_objects:
        logger.debug(f"Runner in add_results(): {runner}")
        runner_object = Runner.objects.get(pk=runner["runner_object"].pk)
        logger.debug(f"runner_object in add_results(): {runner_object}")
        time = runner["time"]
        if time == "DNF":
            time = None
        else:
            # hours, minutes, seconds = map(str, time.split(":"))
            time_elements = time.split(":")
            hours = time_elements[0]
            minutes = time_elements[1]
            seconds = 0
            milliseconds = 0

            if len(time_elements[2]) > 2:
                seconds_milliseconds = time_elements[2].split(' ')
                seconds = seconds_milliseconds[0]
                milliseconds = seconds_milliseconds[1]
            else:
                seconds = time_elements[2]

            time = timedelta(hours=int(hours), minutes=int(minutes),
                             seconds=int(seconds), milliseconds=int(milliseconds))

        result = Result.objects.create(
            race=race_object,
            runner=runner_object,
            time=time
        )
        result_objects.append(result)
    return result_objects


def add_classification(season, race_object):
    classification = Classification.objects.create(
        race=race_object,
        season=season
    )
    return classification


def add_classification_results(classification_object, runner_objects, result_objects, race_object):
    # Go through runner rows
    # For general points, sort by time and increment iteration
    results_with_points = []
    for i in range(len(result_objects)):
        logger.debug(
            f"result from result_objects in add_classification_results: {result_objects[i]}")
        results_with_points.append({
            'result_object': result_objects[i],
            'general_points': i+1
        })
    logger.debug(
        f"results_with_points: {results_with_points}")

    for result in results_with_points:
        ClassificationResult.objects.create(
            classification=classification_object,
            runner=result["result_object"].runner,
            general_points=result["general_points"]
        )

    add_gender_points(result_objects, classification_object, gender="M")
    add_gender_points(result_objects, classification_object, gender="F")
    add_gender_points(result_objects, classification_object, gender="NB")

    add_category_points(result_objects, classification_object)


def add_category_points(result_objects, classification_object):
    # Get the list of category choices
    categories = Runner.category.field.choices
    # Get the keys of the category choices
    category_values = [c[0] for c in Runner.category.field.choices]
    logger.debug(f"categories in add_category_points: {categories}")
    logger.debug(f"category_values in add_category_points: {category_values}")
    for category in category_values:
        category_results = []
        for i in range(len(result_objects)):
            logger.debug(
                f"result from result_objects in add_category_points for category {category}: {result_objects[i]}")
            if result_objects[i].runner.category == category:
                category_results.append({
                    'result_object': result_objects[i]
                })
        logger.debug(
            f"category_results: {category_results}")
        category_results_with_points = []
        for i in range(len(category_results)):
            logger.debug(
                f"result from category_results_with_points in add_category_points: {category_results[i]}")
            category_results_with_points.append({
                'result_object': category_results[i]["result_object"],
                'category_points': i+1
            })
        logger.debug(
            f"category_results_with_points: {category_results_with_points}")

        for result in category_results_with_points:
            classification_result = ClassificationResult.objects.get(
                runner=result["result_object"].runner, classification=classification_object)
            classification_result.category_points = result["category_points"]
            classification_result.save()


def add_gender_points(result_objects, classification_object, gender):
    gendered_results = []
    for i in range(len(result_objects)):
        logger.debug(
            f"result from result_objects in add_classification_results: {result_objects[i]}")
        if result_objects[i].runner.gender == gender:
            gendered_results.append({
                'result_object': result_objects[i]
            })
    logger.debug(
        f"gendered_results: {gendered_results}")

    gendered_results_with_points = []
    for i in range(len(gendered_results)):
        logger.debug(
            f"result from gendered_results_with_points in add_gender_points: {gendered_results[i]}")
        gendered_results_with_points.append({
            'result_object': gendered_results[i]["result_object"],
            'gender_points': i+1
        })
    logger.debug(
        f"gendered_results_with_points: {gendered_results_with_points}")

    for result in gendered_results_with_points:
        classification_result = ClassificationResult.objects.get(
            runner=result["result_object"].runner, classification=classification_object)
        classification_result.gender_points = result["gender_points"]
        classification_result.save()


def handle_race_file(file, season):
    logger.debug(f"Uploaded the following file: {file}")
    df = pd.read_excel(file)
    # Rename columns to remove spaces; otherwise, when itering over them,
    # the columns names will be replace by _{column index}
    df = df.rename(columns={"First Name": "FirstName", "Last Name": "LastName",
                            "Participant Number": "ParticipantNumber"})

    json_df = df.to_json()

    logger.debug(f"The file {file} has the following contents: \n {df}")
    # Handle both file paths (for tests) and uploaded file objects (for actual uploads)
    if hasattr(file, 'name'):
        # This is an uploaded file object
        race_name = Path(file.name).stem
    else:
        # This is a file path string
        race_name = Path(file).stem
    logger.debug(f"Variable race_name: {race_name}")

    file_runner_rows = []
    for row in df.itertuples():
        file_runner_rows.append(row)

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

        race_file_objects = RaceFile.objects.all()
        race_file_objects.delete()

        RaceFile.objects.create(
            excel_file=file,
            contents=json_df,
            race=race_object
        )

        runner_objects = add_runners(df, file_runner_rows)

        # Create results
        logger.debug(
            f"race_object before calling add_results(): {race_object}")
        result_objects = add_results(
            runner_objects, race_object, file_runner_rows)
    else:
        RaceFile.objects.create(
            excel_file=file,
            contents=json_df
        )
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
        result_objects = add_results(
            runner_objects, race_object, file_runner_rows)

        """
        Now, the classification. The rules are as follows:
        - There are six races. 
        - Participation in any five of them is required to be included
        in the classification. 
        - Let n be the number of races, if after the second race a runner 
        has taken part in fewer than n - 1 races (0 being for runners
        who join the series after the second race), they are excluded
        from the classification. 
        - After each race, a runner receives points. The number of points
        corresponds to the runner's position. 
        - For runners who are included in the classification, 
        points will change after each race. Not only because new points
        for the new race will be added, but also because points for previous
        races will need to be recalculated. 
        - In terms of how it could work in practice, I think it might be
        a good idea to create a copy of the results for each race 
        after the next race so that the runners that are no longer included
        in the classification are removed from the previous races and the
        points can be recalculated. 
        - Perhaps, there should be an immutable version of race result object
        that is used for race results and another mutable version that can be
        used for recalculation purposes. 
        """

    classification_object = add_classification(season, race_object)

    add_classification_results(
        classification_object, runner_objects, result_objects, race_object)
