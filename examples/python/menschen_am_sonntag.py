# -*- coding: utf-8 -*-

import os
import tempfile

from avefi_schema import model as efi
from linkml_runtime.dumpers import JSONDumper
from linkml_runtime.loaders import JSONLoader


def main():
    # Initialise helpers
    dumper = JSONDumper()
    loader = JSONLoader()

    # Instantiate moving image records
    work = sample_work()
    manifestation = sample_manifestation(work)
    item = sample_item(manifestation)

    # Create file in temp directory
    file_obj, json_file = tempfile.mkstemp(
        prefix='menschen_am_sonntag_', suffix='.json')
    os.close(file_obj)

    # Write data to file
    dumper.dump([work, manifestation, item], json_file, inject_type=False)

    # Read data back again
    records = loader.load_any(json_file, efi.MovingImageRecord)
    assert records[0] == work
    print(f"Wrote data to {json_file} and read it back again")


def sample_work():
    work = efi.WorkVariant(
        type=efi.WorkVariantTypeEnum.Monographic,
        has_primary_title=efi.Title(
            type=efi.TitleTypeEnum.PreferredTitle,
            has_name='Menschen am Sonntag – Das Dokument der Gegenwart'))
    event = efi.ProductionEvent(
        has_date='1929/1930',
        located_in=efi.GeographicName(
            has_name='Germany (German Reich)',
            same_as=efi.GNDResource(id='2008993-4')))
    work.has_event.append(event)
    directors = efi.DirectingActivity(
        type=efi.DirectingActivityTypeEnum.Director,
        has_agent=[
            efi.Agent(
                type=efi.AgentTypeEnum.Person,
                has_name='Siodmak, Robert',
                same_as=[efi.GNDResource(id='11861472X')]),
            efi.Agent(
                type=efi.AgentTypeEnum.Person,
                has_name='Ulmer, Edgar G.',
                same_as=[efi.GNDResource(id='124471196')]),
            efi.Agent(
                type=efi.AgentTypeEnum.Person,
                has_name='Gliese, Rochus',
                same_as=[efi.GNDResource(id='116663308')])
        ])
    event.has_activity.append(directors)
    event.has_activity.append(
        efi.WritingActivity(
            type=efi.WritingActivityTypeEnum.Writer,
            has_agent=efi.Agent(
                type=efi.AgentTypeEnum.Person,
                has_name='Wilder, Billy',
                same_as=[
                    efi.GNDResource(id='118632795')])))
    work.has_genre.append(
        efi.Genre(has_name='Fiction'))

    # If no EFI has been registered yet, assign arbitrary identifier,
    # e.g. from local database, with prefix "local:"
    work.has_identifier.append(efi.LocalResource(id='mams_1'))
    work.same_as.append(
        efi.FilmportalResource(id='f570e1abdad841dc8d5b25b0f7737065'))
    return work


def sample_manifestation(*works):
    manifestation = efi.Manifestation(
        has_identifier=[efi.LocalResource(id='mams_12')],
        is_manifestation_of=[
            efi.LocalResource(id=work.has_identifier[0].id) for work in works],
        has_primary_title=efi.Title(
            type=efi.TitleTypeEnum.TitleProper,
            has_name='Menschen am Sonntag')
    )
    kinemathek = efi.Agent(
        type=efi.AgentTypeEnum.CorporateBody,
        has_name='Deutsche Kinemathek - Museum für Film und Fernsehen',
        same_as=[efi.GNDResource(id='998208027')])
    restoration_activities = [
        efi.ManifestationActivity(
            type=efi.ManifestationActivityTypeEnum.AgentResponsibleForReproductionOrTransfer,
            has_agent=[kinemathek]),
        efi.ManifestationActivity(
            type=efi.ManifestationActivityTypeEnum.AgentResponsibleForTheArchivalAvailability,
            has_agent=[kinemathek]),
    ]
    manifestation.has_event.append(efi.PreservationEvent(
        type=efi.PreservationEventTypeEnum.RestorationEvent,
        has_date='2013/2014',
        has_activity=restoration_activities))
    manifestation.has_event.append(efi.PublicationEvent(
        type=efi.PublicationEventTypeEnum.ReleaseEvent,
        has_date='2014'))
    manifestation.in_language = [
        efi.Language(
            usage=efi.LanguageUsageEnum.Intertitles,
            code=efi.LanguageCodeEnum.deu),
        efi.Language(
            usage=efi.LanguageUsageEnum.Subtitles,
            code=efi.LanguageCodeEnum.eng),
        efi.Language(
            usage=efi.LanguageUsageEnum.Subtitles,
            code=efi.LanguageCodeEnum.fra)
    ]
    manifestation.has_colour_type = 'BlackAndWhite'
    manifestation.has_sound_type = 'Sound'
    return manifestation


def sample_item(manifestation):
    item = efi.Item(
        has_identifier=[efi.LocalResource(id='mams_123')],
        is_item_of=efi.LocalResource(id=manifestation.has_identifier[0].id),
        element_type=efi.ItemElementTypeEnum.DCP,
        has_primary_title=manifestation.has_primary_title,
        has_access_status=efi.ItemAccessStatusEnum.Distribution,
        has_extent=efi.Extent(has_unit=efi.UnitEnum.GigaByte, has_value=113),
        has_format=[
            efi.DigitalFile(type=efi.FormatDigitalFileTypeEnum.MXF),
        ],
    )
    return item


if __name__ == '__main__':
    main()
