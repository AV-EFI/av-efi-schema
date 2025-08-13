# -*- coding: utf-8 -*-

"""Produce AVefi compliant JSON data using Python language bindings.

Demo code generating a schema compliant JSON file and reading it back
again. Install requirements in a virtualenv and run this demo code as
follows::

    $ python3 -m venv demo_venv
    $ . demo_venv/bin/activate
    (demo_venv) $ pip install "avefi_schema @ git+https://github.com/AV-EFI/av-efi-schema.git"
    (demo_venv) $ python menschen_am_sonntag.py

"""

import os
import pathlib
import tempfile
from typing import Annotated

from avefi_schema import model_pydantic_v2 as efi
from pydantic import Field, RootModel


class MovingImageRecords(RootModel):
    root: list[Annotated[
        efi.WorkVariant | efi.Manifestation | efi.Item,
        Field(discriminator='category'),
    ]]


def main():
    # Instantiate moving image records
    work = sample_work()
    manifestation = sample_manifestation(work)
    item = sample_item(manifestation)

    # Create file in temp directory
    file_obj, json_file = tempfile.mkstemp(
        prefix='menschen_am_sonntag_', suffix='.json')
    os.close(file_obj)

    # Write data to file
    records = MovingImageRecords([work, manifestation, item])
    with open(json_file, 'w') as f:
        f.write(records.model_dump_json(exclude_none=True, indent=2))

    # Read data back again
    with open(json_file) as f:
        records = MovingImageRecords.model_validate_json(f.read())
    assert records.root[0] == work
    print(f"Wrote data to {json_file} and read it back again")


def sample_work():
    work = efi.WorkVariant(
        type=efi.WorkVariantTypeEnum('Monographic'),
        has_primary_title=efi.Title(
            type=efi.TitleTypeEnum('PreferredTitle'),
            has_name='Menschen am Sonntag – Das Dokument der Gegenwart'))
    event = efi.ProductionEvent(
        has_date='1929/1930',
        located_in=[efi.GeographicName(
            has_name='Germany (German Reich)',
            same_as=[efi.GNDResource(id='2008993-4')])])
    work.has_event = [event]
    directors = efi.DirectingActivity(
        type=efi.DirectingActivityTypeEnum('Director'),
        has_agent=[
            efi.Agent(
                type=efi.AgentTypeEnum('Person'),
                has_name='Siodmak, Robert',
                same_as=[efi.GNDResource(id='11861472X')]),
            efi.Agent(
                type=efi.AgentTypeEnum('Person'),
                has_name='Ulmer, Edgar G.',
                same_as=[efi.GNDResource(id='124471196')]),
            efi.Agent(
                type=efi.AgentTypeEnum('Person'),
                has_name='Gliese, Rochus',
                same_as=[efi.GNDResource(id='116663308')])
        ])
    event.has_activity = [directors]
    event.has_activity.append(
        efi.WritingActivity(
            type=efi.WritingActivityTypeEnum('Writer'),
            has_agent=[efi.Agent(
                type=efi.AgentTypeEnum('Person'),
                has_name='Wilder, Billy',
                same_as=[
                    efi.GNDResource(id='118632795')])]))
    work.has_genre = [efi.Genre(has_name='Fiction')]

    # If no EFI has been registered yet, assign arbitrary identifier,
    # e.g. from local database, with prefix "local:"
    work.has_identifier = [efi.LocalResource(id='mams_1')]
    work.same_as = [
        efi.FilmportalResource(id='f570e1abdad841dc8d5b25b0f7737065')]
    return work


def sample_manifestation(*works):
    manifestation = efi.Manifestation(
        has_identifier=[efi.LocalResource(id='mams_12')],
        is_manifestation_of=[
            efi.LocalResource(id=work.has_identifier[0].id) for work in works],
        has_primary_title=efi.Title(
            type=efi.TitleTypeEnum('TitleProper'),
            has_name='Menschen am Sonntag')
    )
    kinemathek = efi.Agent(
        type=efi.AgentTypeEnum('CorporateBody'),
        has_name='Deutsche Kinemathek - Museum für Film und Fernsehen',
        same_as=[efi.GNDResource(id='998208027')])
    restoration_activities = [
        efi.ManifestationActivity(
            type=efi.ManifestationActivityTypeEnum(
                'AgentResponsibleForReproductionOrTransfer'),
            has_agent=[kinemathek]),
        efi.ManifestationActivity(
            type=efi.ManifestationActivityTypeEnum(
                'AgentResponsibleForTheArchivalAvailability'),
            has_agent=[kinemathek]),
    ]
    manifestation.has_event = [efi.PreservationEvent(
        type=efi.PreservationEventTypeEnum('RestorationEvent'),
        has_date='2013/2014',
        has_activity=restoration_activities)]
    manifestation.has_event.append(efi.PublicationEvent(
        type=efi.PublicationEventTypeEnum('ReleaseEvent'),
        has_date='2014'))
    manifestation.in_language = [
        efi.Language(
            usage=[efi.LanguageUsageEnum('Intertitles')],
            code=efi.LanguageCodeEnum('deu')),
        efi.Language(
            usage=[efi.LanguageUsageEnum('Subtitles')],
            code=efi.LanguageCodeEnum('eng')),
        efi.Language(
            usage=[efi.LanguageUsageEnum('Subtitles')],
            code=efi.LanguageCodeEnum('fra'))
    ]
    manifestation.has_colour_type = efi.ColourTypeEnum('BlackAndWhite')
    manifestation.has_sound_type = efi.SoundTypeEnum('Sound')
    return manifestation


def sample_item(manifestation):
    item = efi.Item(
        has_identifier=[efi.LocalResource(id='mams_123')],
        is_item_of=efi.LocalResource(id=manifestation.has_identifier[0].id),
        element_type=efi.ItemElementTypeEnum('DCP'),
        has_primary_title=manifestation.has_primary_title,
        has_access_status=efi.ItemAccessStatusEnum('Distribution'),
        has_extent=efi.Extent(has_unit=efi.UnitEnum('GigaByte'), has_value=113),
        has_format=[
            efi.DigitalFile(type=efi.FormatDigitalFileTypeEnum('MXF')),
        ],
    )
    return item


if __name__ == '__main__':
    main()
