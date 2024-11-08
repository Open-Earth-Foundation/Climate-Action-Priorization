import os
import json
from utils.data_loader import load_datafile_into_df
from utils.extraction_functions import (
    extract_ActionType,
    extract_ActionName,
    extract_AdaptationCategory,
    extract_Hazard,
    extract_Sector,
    extract_Subsector,
    extract_PrimaryPurpose,
    extract_InterventionType,
    extract_Description,
    extract_BehavioralChangeTargeted,
    extract_CoBenefits,
    extract_EquityAndInclusionConsiderations,
    extract_GHGReductionPotential,
    extract_AdaptionEffectiveness,
    extract_CostInvestmentNeeded,
    extract_TimelineForImplementation,
    extract_Dependencies,
    extract_KeyPerformanceIndicators,
    extract_Impacts,
)

# Read the JSON schema from the file
with open("generic_output_schema.json", "r") as schema_file:
    json_template = json.load(schema_file)

# Load the data into a DataFrame
df = load_datafile_into_df("files/climate_action_library_original.csv")

# Prepare a list to hold all mapped data
mapped_data = []

# Define a list of extraction functions and corresponding JSON fields
extraction_functions = {
    # "ActionID": extract_ActionID, -> not in the mapping because it is already set in the main script as incremental index
    "ActionName": extract_ActionName,
    # "ActionType": extract_ActionType, -> not in the mapping because it is already extracted in the main script as first step
    "AdaptationCategory": extract_AdaptationCategory,
    "Hazard": extract_Hazard,
    "Sector": extract_Sector,
    "Subsector": extract_Subsector,
    "PrimaryPurpose": extract_PrimaryPurpose,
    "InterventionType": extract_InterventionType,
    "Description": extract_Description,
    "BehavioralChangeTargeted": extract_BehavioralChangeTargeted,
    "CoBenefits": extract_CoBenefits,
    "EquityAndInclusionConsiderations": extract_EquityAndInclusionConsiderations,
    "GHGReductionPotential": extract_GHGReductionPotential,
    "AdaptionEffectiveness": extract_AdaptionEffectiveness,
    "CostInvestmentNeeded": extract_CostInvestmentNeeded,
    "TimelineForImplementation": extract_TimelineForImplementation,
    "Dependencies": extract_Dependencies,
    "KeyPerformanceIndicators": extract_KeyPerformanceIndicators,
    "Impacts": extract_Impacts,
}

# For testing, only process x rows
df_subset = df  # .tail(50)

# Incremental counter for ActionID
action_id = 1

# Iterate over DataFrame rows
for index, df_row in df_subset.iterrows():
    print(f"Processing row {index}...\n")
    mapped_row = {}

    # Assign an incremental value to ActionID
    mapped_row["ActionID"] = f"{action_id:04d}"

    # Extract 'ActionType' first
    action_type = extract_ActionType(df_row)
    mapped_row["ActionType"] = action_type

    # iterate over extraction functions and apply them to the row
    for attribute_name, function in extraction_functions.items():
        dict_attribute = function(df_row, action_type["value"])
        mapped_row[attribute_name] = dict_attribute

    mapped_data.append(mapped_row)
    action_id += 1
    print(f"\nRow {index} processed successfully.\n\n")


output_dir = "./output"
os.makedirs(output_dir, exist_ok=True)

# Optionally, save the mapped data to a JSON file
with open(os.path.join(output_dir, "output.json"), "w") as f:
    json.dump(mapped_data, f, indent=4)

print("JSON data has been written to output.json")
