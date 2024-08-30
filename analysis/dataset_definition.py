# Dataset will filter from 01/04/2024, for male or female, adults, who are not dead on the index date, who were registered
# We will get information on their age, sex, ethnicity, imd quintile,
# number of inhaler meds they have had, and date of first admission

from ehrql import (
    case,
    codelist_from_csv,
    create_dataset,
    days,
    when,
)

# Check out the TPP Schema for more information on these tables
# https://docs.opensafely.org/ehrql/reference/schemas/tpp/
from ehrql.tables.tpp import (
    addresses,
    clinical_events,
    apcs,
    medications,
    patients,
    practice_registrations,
)

# The start date we are going to filter from
# Form is YYYY-MM-DD
index_date = "2024-04-01"

# Initialise the dataset
dataset = create_dataset()

# If you don't set this, it'll default to 10
# The higher the population size, the longer the script will take to run
dataset.configure_dummy_data(population_size=10000)

# Codelists define the codes we are going to be searching for
# In order to import a codelist, you must add it to the file codelists.txt - found in the codelists folder
# Search for a codelist on: https://www.opencodelists.org/
# Once you have found your codelist, copy the end of the web address into the codelists file
# opencodelists.org/codelist/COPY/THIS/PART
# Type into your command line: opensafely codelists update
# This will fetch the version of the codelist you have given
# It will upload the .csv to the codelist folder and add it to the .json
# And the lines below are how you will reference it for your dataset

asthma_inhaler_codelist = codelist_from_csv(
    "codelists/opensafely-asthma-inhaler-salbutamol-medication.csv",
    column="code",
)

ethnicity_codelist = codelist_from_csv(
    "codelists/opensafely-ethnicity.csv",
    column="Code",
    category_column="Grouping_6",
)



# population variables
# This is how we will filter our population
is_female_or_male = patients.sex.is_in(["female", "male"])

was_adult = (patients.age_on(index_date) >= 18) & (
    patients.age_on(index_date) <= 110
)

was_alive = (
    patients.date_of_death.is_after(index_date)
    | patients.date_of_death.is_null()
)

was_registered = practice_registrations.for_patient_on(
    index_date
).exists_for_patient()


# This pulls together the filters we have defined above to define the population
dataset.define_population(
    is_female_or_male
    & was_adult
    & was_alive
    & was_registered
)



# The code below will not filter your population, but is for pulling out the 
# information about your already filtered population that you are interested in
# These are the variables that you will create your graphs on. 
# They will be accessible to the code on "report.py"
# The word after the . will be the name of the column

# Get the age of the patient (we have filtered to 18-110)
dataset.age = patients.age_on(index_date)

# Get the sex of the patient (we have filtered to male/female)
dataset.sex = patients.sex

# Get the most recent ethnicity for the patient
# The ethnicity code from the codelist is assigned to one of six categories (1: White, 2: Mixed, 3: South Asian, 4: Black, 5: Other, 6: Not stated)
# This finds the patients ethnicity based on the ctv3 code (more descriptive than the 6 categories)
# Sorts by date and takes the most recent one
# changes the code the label in the category_column (from when the codelist was imported)
dataset.ethnicity = (
    clinical_events.where(
        clinical_events.ctv3_code.is_in(ethnicity_codelist)
    )
    .sort_by(clinical_events.date)
    .last_for_patient()
    .ctv3_code.to_category(ethnicity_codelist)
)


# Get the index of multiple deprivation quintile (1: Most Deprived, 5: Least Deprived)
imd_rounded = addresses.for_patient_on(
    index_date
).imd_rounded
max_imd = 32844
dataset.imd_quintile = case(
    when(imd_rounded < int(max_imd * 1 / 5)).then(1),
    when(imd_rounded < int(max_imd * 2 / 5)).then(2),
    when(imd_rounded < int(max_imd * 3 / 5)).then(3),
    when(imd_rounded < int(max_imd * 4 / 5)).then(4),
    when(imd_rounded <= max_imd).then(5),
)


# Get the number of times a code from the asthma_inhaler_codelist is present
# for a patient between the index date and 30 days previous
dataset.num_asthma_inhaler_medications = medications.where(
    medications.dmd_code.is_in(asthma_inhaler_codelist)
    & medications.date.is_on_or_between(
        index_date - days(30), index_date
    )
).count_for_patient()



# Get the date of the admission for patient
# Sort by the date and then return the first date
dataset.date_of_first_admission = (
    apcs.where(
        apcs.admission_date.is_after(
            index_date
        )
    )
    .sort_by(apcs.admission_date)
    .first_for_patient()
    .admission_date
)


# Notice we don't need to return anything here
# This file only has one output called "dataset"
# To obtain it we need to look at project.yaml