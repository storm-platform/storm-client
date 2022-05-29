# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import json

from storm_client import Storm
from storm_client.models.deposit import DepositJob
from storm_client.models.runner import ExecutionJob
from storm_client.models.project import Project
from storm_client.models.workflow import Workflow
from storm_client.models.compendium import CompendiumDraft

#
# 1. Defining a Storm Client instance.
#
service = Storm(
    url="<service-address>",
    access_token="<access-token>",
    # ... other http options (e.g., timeout)
)

# Checking the connection
print(service.is_connected)

#
# 2. Creating a new project.
#

# Project identifier
project_identifier = "my-example-project"

# Loading the project metadata from a JSON document.
project_metadata = json.load(open("data/project_metadata.json"))

# Defining the project object.
project = Project(id=project_identifier, metadata=project_metadata)

# Checking the object properties

#  > ID
print(project.id)

#  > Description
print(project.description)

#  > Complete JSON document.
print(project.data)

#
# 3. Saving the project in the Storm WS.
#

# Send it!
project_data = service.project.create(project)

# Now, we can see the created project
print(project_data)

# To finish, let's get the created project from the server
example_project = service.project.get(project_data.id)

#
# 4. Updating the project.
#
example_project_2 = example_project.copy()

# Change the title
example_project_2.data["metadata"].update({"title": "A new project here!"})

# Saving in the server
example_project_2 = service.project.save(example_project_2)

#
# 5. Search for a project.
#

#  > Searching for all projects available (for your user)
print(service.project.search())

#  > Using expressions to filter the data
#    (In this example, let's get the created project id)
print(service.project.search(q=f"id:{example_project_2.id}"))

#
# 6. Accessing the Project Context.
#

# Getting the Context
project_context = service.project(project_identifier)

# With the Context, we can access all related resource, such as:
#   > Compendia  (project_context.compendia)
#   > Workflows  (project_context.workflow)
#   > Deposits   (project_context.deposit)
#   > Jobs       (project_context.job)

# 6.1. Working with the compendia.

# To work with the compendia, we use the Compendium Context:
compendium_context = project_context.compendium

# In this context, we can search for available compendia:
print(project_context.compendium.search())

# (You can filter only the compendia that you create):
print(project_context.compendium.search(user_records=True))

# An compendium can be a Draft (development stage) or Record (Finalized).
# To use these different types of compendium, we can use the Compendium Context
# attributes. Let us look for the context attributes:

# compendium_context.draft  # To manipulate the Draft compendia.

# or
# compendium_context.record  # To manipulate the Record compendia.

# or
# compendium_context.files  # To manipulate the Compendia (Draft/Record) files.

# 6.1.1. Creating a Compendium Draft.

# To create a new compendium, the following flow must be used:
#  >  Compendium Draft -> Edit -> Publish -> Compendium Record

# Following this flow, the user first creates a Compendium Draft and then populates it (Using edit operations).
# Also, users can upload files to the Compendium Draft. After this edition process, the user can publish the Draft.
# Once a Draft is published, it is transformed into a Compendium Record that cannot be edited.

# To use this flow through the Storm Client, let's create and publish a Compendium. To do this, first,
# we create a Compendium Draft in the service. In the same way that we do
# in the Research Project above, in the Storm Client, this operation starts with a object
compendium_draft = CompendiumDraft()

# This object is empty, so let's populate it with the
# Compendium metadata and files.

# General metadata
compendium_draft.title = "Example Compendium (V1)"
compendium_draft.description = "Example Compendium (V1)"

# Descriptor specification
compendium_draft.environment_descriptor = dict(
    name="Storm Core",
    version="v1.0.0",
    uri="https://github.com/storm-platform/storm-core",
)

compendium_draft.environment_metadata = dict(
    repository="https://github.com/foo/bar", files={"key": "environment.package"}
)

# Compendium data files specification
compendium_draft.inputs.extend(["input_file.txt"])
compendium_draft.outputs.append("output_file.txt")

# Now, using the Compendium Context, let's add the
# created compendium draft in the Storm WS:

# Creating the Compendium Record in the service.
compendium_draft = compendium_context.draft.create(compendium_draft)

# Check the returned object:
print(compendium_draft)

# 6.1.2. Adding files to a Compendium Draft

# To add files in a Compendium Draft, we must do the following steps:
#  1. Declare files: Declare to the service what files will be available to download
#                    in the compendium.
#  2. Upload files: Upload the file content
#  3. Commit files: Confirm that the file is already to use.

# So, let's do these steps and add some files to the created
# Compendium Draft:

# For this example, we will add the following files to the compendium:
#   - input_file.txt
#   - output_file.txt

# > Declare files:
# We do not need files/content to declare files, only their names. So, using the
# Compendium Context, let us declare the files:
compendium_draft = compendium_context.files.define_files(
    compendium_draft, ["input_file.txt", "output_file.txt"]
)

# > Upload files
# Now, we can upload the files
# (Note that we need files with the same name defined in the **Definition step**)
compendium_draft = compendium_context.files.upload_files(
    compendium_draft,
    {
        "input_file.txt": "data/input_file.txt",
        "output_file.txt": "data/output_file.txt",
    },
    commit_files=False,  # We can use this flag to commit the uploaded files.
    define_files=False,  # We can use this flag to define the uploaded files.
)

# > Commit files
# To finish this files step, we need to commit the defined/uploaded files
compendium_draft = compendium_context.files.commit_defined_files(
    compendium_draft, ["input_file.txt", "output_file.txt"]
)

# 6.1.3. Editing a Compendium Draft.

# Before we publish a Compendium, we can edit it. For example, let us change
# the Compendium description. First, we change the local object:
compendium_draft.description = "Edited compendium description."

# Now, send the modification to the Storm WS:
compendium_draft = compendium_context.draft.save(compendium_draft)
print(compendium_draft)

# 6.1.4. Publishing a Compendium Draft.

# To finish, let us publish the Compendium Draft. After the publication, the Draft will
# be transformed into a Record.
compendium_record = compendium_context.draft.publish(compendium_draft)

# Now, the content of the Compendium Draft is made available as a Compendium Records
# to other users in the Project.
print(compendium_context.search(user_records=True, q=f"id:{compendium_record.id}"))

#
# 6.2. Accessing the Research Workflow Context.
#

# To work with the workflows, we use the Research Workflow Context:
workflow_context = project_context.workflow

# In this context, we can search for available workflows:
print(workflow_context.search())

# 6.2.1. Creating a Research Workflow.

# To create a new Research Workflow in the Storm WS service, first, we need
# to create a Workflow object and populate it with metadata:
workflow_id = "my-example-workflow"

workflow = Workflow(
    id=workflow_id,
    metadata={
        "title": "Workflow example",
        "description": "A very simple workflow",
        "version": "1.0",
    },
)

# Checking the object properties

#  > ID
print(workflow.id)

#  > Description
print(workflow.description)

#  > Complete JSON document.
print(workflow.data)

# With the local object created, let us save it in the Storm WS:
example_workflow = workflow_context.create(workflow)

# We can check the created Research Workflow:
print(example_workflow)

# To confirm the Research Workflow creation in the Storm WS,
# let us read it from the server:
example_workflow = workflow_context.get(example_workflow.id)

# 6.2.2. Editing a Research Workflow.

# After saving the Research Compendium in the Storm WS,
# we can edit its metadata. For example, let us update
# the workflow title created above.
example_workflow.title = "Workflow example (Updated)"

# Now, send the modification to the Storm WS:
example_workflow = workflow_context.save(example_workflow)
print(example_workflow)

# 6.2.3. Adding compendia to the Research Workflow.

# To compose an executable workflow, we need to add compendia
# to it. So, let us add the Compendium Record created above
# to our workflow:
example_workflow.compendia.append(compendium_record)

# (Other ways to add a Compendium Record in the Research Workflow)
# or
# example_workflow.compendia.append("<compendium-record-id>")

# or
# example_workflow.compendia.extent(["<compendium-record-id>"])

# or
# example_workflow.compendia.extent(["<compendium-record-id>", compendium-object])

# After we add the Compendium Record to the Research Workflow,
# we can synchronize the Research Workflow and save these changes in the Storm WS:
example_workflow = workflow_context.sync_compendia(example_workflow)
print(example_workflow)

# Note that we must synchronize any modification done
# into the Research Workflow (Compendium Additions and exclusions).

# 6.2.4. Finish the Research Workflow.

# After completing the Research Workflow and adding all required
# Compendium Records, we can finalize the Research Workflow.
# Any user cannot change a finalized Research Workflow. It will
# be frozen in the service.

# > Checking if the current workflow is finished:
print(example_workflow.is_finished)

# > Let us finish it
example_workflow = workflow_context.finalize(example_workflow)

# > Checking if the workflow was finished:
print(example_workflow.is_finished)

# 6.2.5. Delete a Research Workflow (Optional).

# We can also delete the Research workflow:
# workflow_context.delete(example_workflow)

# Note: A Research workflow finished cannot be deleted.

#
# 6.3. Accessing the Deposit Job Context.
#

# To work with the deposits jobs, we use the Deposit Job Context:
deposit_context = project_context.deposit

# In this context, we can search for available deposit jobs:
print(deposit_context.search())

# 6.3.1. Searching deposit job services.

# In the Storm WS, it is available multiple deposit jobs services. Each
# service is specialized to send the data to a different place (e.g., GEO Knowledge Hub, Zenodo).
# To get the list of available services, we can use the following context
# function:
print(deposit_context.list_services())

# 6.3.2. Creating a Deposit Job.

# To create a new Deposit Job in the Storm WS service, first, we need
# to create a DepositJob object and populate it with metadata:
deposit = DepositJob(
    workflows=[example_workflow],  # here, we can also declare workflows using their ID.
    service="deposit-gkhub",  # name retrieved from the `list_services` method result.
)

# Checking the object properties

#  > ID
print(deposit.id)  # filled after saving the deposit in the service.

#  > Associated workflows
print(deposit.workflows)

#  > Associated service
print(deposit.service)

#  > Associated project
print(deposit.project)  # filled after saving the deposit in the service.

#  > Complete JSON document.
print(deposit.data)

# With the local object created, let us save it in the Storm WS:
example_deposit = deposit_context.create(deposit)

# We can check the created Deposit:
print(example_deposit)

# To confirm the Deposit Job creation in the Storm WS,
# let us read it from the server:
example_deposit = deposit_context.get(example_deposit.id)

# 6.3.3. Editing a Deposit Job.

# After saving the Deposit Job in the Storm WS, we can edit its
# workflow and service:

#  > Service
example_deposit.service = "deposit-inveniordm"

#  > Workflow
example_deposit.workflows = [example_workflow]  # or [ "<workflow-id" ]

# After changes, we can save the modifications in the Storm WS:
example_deposit = deposit_context.save(example_deposit)
print(example_deposit)

# 6.3.3.1. Editing a Deposit (Customizations).

# Some services make a way to edit the Project metadata
# before sending it to the destination. If you need to use these customizations
# options, you can make the customizations (in the service-defined schema)
# and put the object in the field ``customizations.``.

# example_deposit.customizations = {"field_1": "..."}

# 6.3.4. Start a deposit job

# To start a deposit job, we can use:
# example_deposit = deposit_context.start_deposit(example_deposit)

# (Other way to start a Deposit Job)
# deposit_context.start_deposit("<deposit-id>")

# 6.3.5. Cancel a deposit job

# To cancel a started deposit, we can use:
# example_deposit = deposit_context.cancel_deposit(example_deposit)

# (Other way to cancel a Deposit Job)
# deposit_context.cancel_deposit("<deposit-id>")

# 6.3.6. Delete a Deposit Job (Optional).

# We can also delete the Deposit:
# deposit_context.delete(example_deposit)

#
# 6.4. Accessing the Runner Context.
#

# To work with the tasks, we can use the Runner Context:
runner_context = project_context.runner

# In this context, we can search for available execution tasks:
print(runner_context.search())

# 6.4.1. Searching run services.

# In the Storm WS, it is available multiple execution services. Each
# service is specialized to run the defined workflow in a different
# environment (e.g., REANA, o2r). To get the list of available services,
# we can use the following context function:
print(runner_context.list_services())

# 6.4.2. Creating a Job.

# To create a new workflow execution in the Storm WS, first, we need
# to create a Job object and populate it with metadata:
job = ExecutionJob(
    workflow_id=example_workflow,  # here, we can also declare the workflow using its ID.
    service="runner-reprozip-serial",  # name retrieved from the `list_services` method result.
)

# Checking the object properties

#  > ID
print(job.id) # filled after saving the job in the service.

#  > Associated workflow
print(job.workflow_id)

#  > Associated project
print(job.project_id)  # filled after saving the job in the service.

#  > Associated service
print(job.service)

#  > Complete JSON document.
print(job.data)

# With the local object created, let us save it in the Storm WS:
example_job = runner_context.create(job)

# We can check the created Job:
print(example_job)

# To confirm the Job creation in the Storm WS,
# let us read it from the server:
example_job = runner_context.get(example_job.id)

# 6.4.3. Editing a Job.

# After saving the Job in the Storm WS, we can edit its
# associated workflow and service:

#  > Service
example_job.service = "runner-reprozip-serial"

#  > Workflow
example_job.workflow_id = example_workflow

# After changes, we can save the modifications in the Storm WS:
example_job = runner_context.save(example_job)
print(example_job)

# 6.4.4. Start a job

# To start a Job process, we can use:
# example_job = job_context.start_job(example_job)

# (Other way to start a Job process)
# job_context.start_job("<job-id>")

# 6.4.5. Cancel a started job

# To cancel a started job process, we can use:
# example_job = job_context.cancel_job(example_job)

# (Other way to cancel a started Job process)
# job_context.cancel_job("<job-id>")

# 6.4.6. Delete a Job (Optional).

# We can also delete the Job:
# job_context.delete(example_job)

# (Other way to delete Job)
# job_context.delete("<job-id>")
