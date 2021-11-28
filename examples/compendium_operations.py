# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Example for SpatioTemporal Open Research Manager Python client."""

from uuid import uuid4

from storm_client import Storm
from storm_client.models.project import Project
from storm_client.models.compendium import (
    CompendiumRecord,
    CompendiumDraft,
    ExecutionDescriptor,
)

#
# Execution metadata
#
project_id = f"example-project-{str(uuid4())}"

#
# 1. Creating a Storm Client instance.
#
service = Storm("http://127.0.0.1:5000/api", "")

#
# 2. List user available projects.
#
print(service.project.search())
print(len(service.project.search()))

#
# 3. Create a new project.
#

# Project model definition
example_project = Project(
    id=project_id,
    metadata=dict(
        title="Example Project (V1)",
        description="Description for the example project in the first version",
        subjects=["Example 1"],
        rights=[
            {
                "title": "MIT License",
                "description": "MIT License",
                "link": "https://opensource.org/licenses/MIT",
            }
        ],
        contributors=[
            {
                "person_or_org": {
                    "name": "Carlos, Felipe",
                    "type": "personal",
                    "given_name": "Menino Carlos",
                    "family_name": "Felipe",
                }
            }
        ],
        creators=[
            {
                "person_or_org": {
                    "name": "Carlos, Felipe",
                    "type": "personal",
                    "given_name": "Menino Carlos",
                    "family_name": "Felipe",
                }
            }
        ],
        dates=[{"date": "2020/2021", "type": {"id": "available"}}],
        locations={
            "features": [
                {
                    "geometry": {"type": "Point", "coordinates": [-45.85, -23.20]},
                    "place": "ADC INPE",
                    "description": "INPE ADC place.",
                }
            ]
        },
    ),
)

# Creating the project in the Storm WS.
example_project = service.project.create(example_project)
print(example_project)

#
# 4. Retrieve project metadata from Storm WS.
#
example_project = service.project.resolve(project_id)
print(example_project)

#
# 4.1 Get project metadatas
#
# Title
print(example_project.title)

# Description
print(example_project.description)

#
# 5. Create a Compendium
#

# 5. Create draft
compendium_draft = CompendiumDraft()

# 5.1. Draft files and metadata

# General metadata
compendium_draft.title = "Example Compendium (V1)"
compendium_draft.description = "Example Compendium (V1)"

# Descriptor especification
compendium_draft.descriptor = ExecutionDescriptor(
    name="Storm Core",
    version="v1.0.0",
    uri="https://github.com/storm-platform/storm-core",
)

compendium_draft.metadata = dict(
    repository="https://github.com/foo/bar", files={"key": "environment.package"}
)

# Compendium data specification
compendium_draft.inputs.extend(["input_file.txt"])
compendium_draft.outputs.append("output_file.txt")

# Create the compendium inside the current project.
created_draft = service.compendium.draft(project_id).create(compendium_draft)

# Edit the created compendium draft.
created_draft.title = "Example Compendium (V1) - Edited"
edited_draft = service.compendium.draft(project_id).save(created_draft)

# Upload the associated files
updated_draft = service.compendium.files(created_draft).upload_files(
    {
        "input_file.txt": "data/input_file.txt",
        "output_file.txt": "data/output_file.txt",
    },
    commit=True,
)

#
# 6. Publish draft compendium
#
published_compendium = service.compendium.draft(project_id).publish(updated_draft)
published_compendium.to_json()

# 6.1 Create a new compendium version (from the published compendium above)
print("Current ID: ", end=" ")
print(published_compendium.id)

# Create a new version (Draft from published compendium)
new_version_draft = service.compendium.draft(project_id).new_version(
    published_compendium
)

# Upload new files
updated_draft = service.compendium.files(new_version_draft).upload_files(
    {
        "input_file.txt": "data/input_file.txt",
        "output_file.txt": "data/output_file.txt",
    },
    commit=True,
)

# Publish a new version!
published_compendium_versioned = service.compendium.draft(project_id).publish(
    new_version_draft
)

print("New ID: ", end=" ")
print(published_compendium_versioned.id)

#
# 7. Search Draft and Records
#
print(service.compendium.search(project_id).query(q="is_published: true"))

# Search only for user specific records
user_records = service.compendium.search(project_id, user_records=True).query()
for record in user_records:
    if type(record) == CompendiumRecord:
        print("CompendiumRecord")
        print(type(record))
        print(record.links.draft)

    elif type(record) == CompendiumDraft:
        print("CompendiumDraft")
        print(type(record))
        print(record.links.draft)
